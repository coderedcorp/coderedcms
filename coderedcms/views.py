import mimetypes
import os
from datetime import datetime
from django.http import (
    Http404,
    HttpResponse,
    HttpResponsePermanentRedirect,
    JsonResponse,
)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import (
    Paginator,
    InvalidPage,
    EmptyPage,
    PageNotAnInteger,
)
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import ngettext, gettext_lazy as _
from django.views.decorators.http import require_POST
from icalendar import Calendar
from wagtail.admin import messages
from wagtail.models import Page, get_page_models
from wagtail.search.backends import get_search_backend
from wagtail.search.backends.database.mysql.mysql import MySQLSearchBackend
from coderedcms import utils
from coderedcms.forms import SearchForm
from coderedcms.models import CoderedPage, LayoutSettings
from coderedcms.importexport import (
    convert_csv_to_json,
    import_pages,
    ImportPagesFromCSVFileForm,
)
from coderedcms.settings import crx_settings
from coderedcms.templatetags.coderedcms_tags import get_name_of_class


def search(request):
    """
    Searches pages across the entire site.
    """
    search_form = SearchForm(request.GET)
    pagetypes = []
    results = None
    results_paginated = None

    if search_form.is_valid():
        search_query = search_form.cleaned_data["s"]
        search_model = search_form.cleaned_data["t"]

        # get all page models
        pagemodels = sorted(get_page_models(), key=get_name_of_class)
        # filter based on is search_filterable
        for model in pagemodels:
            if hasattr(model, "search_filterable") and model.search_filterable:
                pagetypes.append(model)

        results = Page.objects.live()
        if search_model:
            try:
                # If provided a model name, try to get it
                model = ContentType.objects.get(
                    model=search_model
                ).model_class()
                # Workaround for Wagtail MySQL search bug.
                # See: https://github.com/wagtail/wagtail/issues/11273
                backend = get_search_backend()
                if type(backend) is MySQLSearchBackend:
                    results = model.objects.live()
                else:
                    results = results.type(model)
            except ContentType.DoesNotExist:
                # Maintain existing behavior of only returning objects if the page type is real
                results = None

        # get and paginate results
        if results:
            results = results.search(search_query)
            paginator = Paginator(
                results, LayoutSettings.for_request(request).search_num_results
            )
            page = request.GET.get("p", 1)
            try:
                results_paginated = paginator.page(page)
            except PageNotAnInteger:
                results_paginated = paginator.page(1)
            except EmptyPage:
                results_paginated = paginator.page(1)
            except InvalidPage:
                results_paginated = paginator.page(1)

    # Render template
    return render(
        request,
        "coderedcms/pages/search.html",
        {
            "request": request,
            "pagetypes": pagetypes,
            "form": search_form,
            "results": results,
            "results_paginated": results_paginated,
        },
    )


@login_required
def serve_protected_file(request, path):
    """
    Function that serves protected files uploaded from forms.
    """
    # Fully resolve all provided paths.
    mediapath = os.path.abspath(crx_settings.CRX_PROTECTED_MEDIA_ROOT)
    fullpath = os.path.abspath(os.path.join(mediapath, path))

    # Path must be a sub-path of the PROTECTED_MEDIA_ROOT, and exist.
    if fullpath.startswith(mediapath) and os.path.isfile(fullpath):
        mimetype, encoding = mimetypes.guess_type(fullpath)
        with open(fullpath, "rb") as f:
            response = HttpResponse(f.read(), content_type=mimetype)
        if encoding:
            response["Content-Encoding"] = encoding

        return response
    raise Http404()


def favicon(request):
    icon = LayoutSettings.for_request(request).favicon
    if icon:
        # Try to convert to webp, otherwise pass original file format
        # This will happen mainly if the file is an SVG
        try:
            return HttpResponsePermanentRedirect(
                icon.get_rendition("fill-256x256|format-webp").url
            )
        except AttributeError:
            return HttpResponsePermanentRedirect(
                icon.get_rendition("fill-256x256").url
            )
    raise Http404()


def robots(request):
    return render(request, "robots.txt", content_type="text/plain")


@require_POST
def event_generate_single_ical_for_event(request):
    # Parse input.
    try:
        event_pk = request.POST["event_pk"]
    except KeyError:
        return HttpResponse("event_pk required", status=400)

    try:
        dt_start_str = utils.fix_ical_datetime_format(
            request.POST["datetime_start"]
        )
        dt_end_str = utils.fix_ical_datetime_format(
            request.POST["datetime_end"]
        )
        dt_start = None
        dt_end = None
        if dt_start_str:
            dt_start = datetime.strptime(dt_start_str, "%Y-%m-%dT%H:%M:%S%z")
        if dt_end_str:
            dt_end = datetime.strptime(dt_end_str, "%Y-%m-%dT%H:%M:%S%z")
    except KeyError:
        return HttpResponse(
            "datetime_start and datetime_end required.",
            status=400,
        )
    except ValueError:
        return HttpResponse(
            "datetime_start and datetime_end must be valid datetimes.",
            status=400,
        )

    # Get the page.
    try:
        event = CoderedPage.objects.get(pk=event_pk).specific
    except (CoderedPage.DoesNotExist, ValueError):
        raise Http404("Event does not exist")

    # Generate the ical file.
    ical = Calendar()
    ical.add("prodid", "-//Wagtail CRX//")
    ical.add("version", "2.0")
    ical.add_component(
        event.create_single_ical(dt_start=dt_start, dt_end=dt_end)
    )
    response = HttpResponse(ical.to_ical(), content_type="text/calendar")
    response["Filename"] = "{0}.ics".format(event.slug)
    response["Content-Disposition"] = "attachment; filename={0}.ics".format(
        event.slug
    )
    return response


@require_POST
def event_generate_recurring_ical_for_event(request):
    # Parse input.
    try:
        event_pk = request.POST["event_pk"]
    except KeyError:
        return HttpResponse("event_pk required", status=400)

    # Get the page.
    try:
        event = CoderedPage.objects.get(pk=event_pk).specific
    except (CoderedPage.DoesNotExist, ValueError):
        raise Http404("Event does not exist")

    # Generate the ical file.
    ical = Calendar()
    ical.add("prodid", "-//Wagtail CRX//")
    ical.add("version", "2.0")
    for e in event.create_recurring_ical():
        ical.add_component(e)
    response = HttpResponse(ical.to_ical(), content_type="text/calendar")
    response["Filename"] = "{0}.ics".format(event.slug)
    response["Content-Disposition"] = "attachment; filename={0}.ics".format(
        event.slug
    )
    return response


@require_POST
def event_generate_ical_for_calendar(request):
    # Parse input.
    try:
        page_id = request.POST["page_id"]
    except KeyError:
        return HttpResponse("page_id required", status=400)

    # Get the page.
    try:
        page = CoderedPage.objects.get(pk=page_id).specific
    except (CoderedPage.DoesNotExist, ValueError):
        raise Http404("Page does not exist")

    # Generate the ical file.
    ical = Calendar()
    ical.add("prodid", "-//Wagtail CRX//")
    ical.add("version", "2.0")
    for event_page in page.get_index_children():
        for e in event_page.specific.create_recurring_ical():
            ical.add_component(e)
    response = HttpResponse(ical.to_ical(), content_type="text/calendar")
    response["Filename"] = "calendar.ics"
    response["Content-Disposition"] = "attachment; filename=calendar.ics"
    return response


def event_get_calendar_events(request):
    """
    JSON list of events compatible with fullcalendar.js
    """
    # Parse input.
    try:
        page_id = request.GET["pid"]
    except KeyError:
        return HttpResponse("pid required", status=400)

    start = None
    end = None
    start_str = request.GET.get("start", None)
    end_str = request.GET.get("end", None)
    try:
        if start_str:
            start = timezone.make_aware(
                datetime.strptime(start_str[:10], "%Y-%m-%d"),
            )
        if end_str:
            end = timezone.make_aware(
                datetime.strptime(end_str[:10], "%Y-%m-%d"),
            )
    except ValueError:
        return HttpResponse(
            "start and end must be valid datetimes.", status=400
        )

    # Get the page.
    try:
        page = CoderedPage.objects.get(pk=page_id).specific
    except (CoderedPage.DoesNotExist, ValueError):
        raise Http404("Page does not exist")

    return JsonResponse(
        page.get_calendar_events(start=start, end=end), safe=False
    )


@login_required
@permission_required(
    "wagtailadmin.access_admin",
    login_url="wagtailadmin_login",
)
def import_index(request):
    """
    Landing page to replace wagtailimportexport.
    """
    return render(request, "wagtailimportexport/index.html")


@login_required
@permission_required(
    "wagtailadmin.access_admin",
    login_url="wagtailadmin_login",
)
def import_pages_from_csv_file(request):
    """
    Overwrite of the `import_pages` view from wagtailimportexport.  By default, the `import_pages`
    view expects a json file to be uploaded.  This view converts the uploaded csv into the json
    format that the importer expects.
    """

    if request.method == "POST":
        form = ImportPagesFromCSVFileForm(request.POST, request.FILES)
        if form.is_valid():
            import_data = convert_csv_to_json(
                form.cleaned_data["file"].read().decode("utf-8").splitlines(),
                form.cleaned_data["page_type"],
            )
            parent_page = form.cleaned_data["parent_page"]
            try:
                page_count = import_pages(import_data, parent_page)
            except LookupError as e:
                messages.error(
                    request, _("Import failed: %(reason)s") % {"reason": e}
                )
            else:
                messages.success(
                    request,
                    ngettext(
                        "%(count)s page imported.",
                        "%(count)s pages imported.",
                        page_count,
                    )
                    % {"count": page_count},
                )
            return redirect("wagtailadmin_explore", parent_page.pk)
    else:
        form = ImportPagesFromCSVFileForm()

    return render(
        request,
        "wagtailimportexport/import_from_csv.html",
        {
            "form": form,
        },
    )
