import ast
import os
import mimetypes
from itertools import chain

from datetime import datetime
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import render
from icalendar import Calendar
from taggit.models import Tag
from wagtail.contrib.forms.views import SubmissionsListView as BaseSubmissionsListView
from wagtail.core.models import Page
from wagtail.core.utils import resolve_model_string
from wagtail.search.backends import db, get_search_backend
from wagtail.search.models import Query

from coderedcms import utils
from coderedcms.forms import SearchForm
from coderedcms.models import CoderedPage, CoderedEventPage, get_page_models, GeneralSettings


def search(request):
    """
    Searches pages across the entire site.
    """
    search_form = SearchForm(request.GET)
    pagetypes = []
    results = None
    results_paginated = None

    if search_form.is_valid():
        search_query = search_form.cleaned_data['s']
        search_model = search_form.cleaned_data['t']

        # get all codered models
        pagemodels = sorted(get_page_models(), key=lambda k: k.search_name)
        # get filterable models
        for model in pagemodels:
            if model.search_filterable:
                pagetypes.append(model)

        # get backend
        backend = get_search_backend()

        # DB search. Since this backend can't handle inheritance or scoring,
        # search specified page types in the desired order and chain the results together.
        # This provides better search results than simply searching limited fields on CoderedPage.
        db_models = []
        if backend.__class__ == db.SearchBackend:
            for model in get_page_models():
                if model.search_db_include:
                    db_models.append(model)
            db_models = sorted(db_models, reverse=True, key=lambda k: k.search_db_boost)

        if backend.__class__ == db.SearchBackend and db_models:
            for model in db_models:
                # if search_model is provided, only search on that model
                if not search_model or search_model == ContentType.objects.get_for_model(model).model:
                    curr_results = model.objects.live().search(search_query)
                    if results:
                        results = list(chain(results, curr_results))
                    else:
                        results = curr_results

        # Fallback for any other search backend
        else:
            if search_model:
                try:
                    model = ContentType.objects.get(model=search_model).model_class()
                    results = model.objects.live().search(search_query)
                except:
                    results = None
            else:
                results = CoderedPage.objects.live().search(search_query)

        # paginate results
        if results:
            paginator = Paginator(results, GeneralSettings.for_site(request.site).search_num_results)
            page = request.GET.get('p', 1)
            try:
                results_paginated = paginator.page(page)
            except:
                results_paginated = paginator.page(1)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()

    # Render template
    return render(request, 'coderedcms/pages/search.html', {
        'request': request,
        'pagetypes': pagetypes,
        'form': search_form,
        'results': results,
        'results_paginated': results_paginated
    })

@login_required
def serve_protected_file(request, path):
    """
    Function that serves protected files uploaded from forms.
    """
    fullpath = os.path.join(cr_settings['PROTECTED_MEDIA_ROOT'], path)
    if os.path.isfile(fullpath):
        mimetype, encoding = mimetypes.guess_type(fullpath)
        with open(fullpath, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mimetype)
        if encoding:
            response["Content-Encoding"] = encoding

        return response
    else:
        raise Http404()

@login_required
def clear_cache(request):
    utils.clear_cache()
    return HttpResponse("Cache has been cleared.")

def robots(request):
    robots = GeneralSettings.for_site(request.site).robots
    return render(
        request,
        'robots.txt',
        {'robots': robots},
        content_type='text/plain'
    )

def generate_single_ical_for_event(request):
    if request.method == "POST":
        event_pk = request.POST['event_pk']
        event_page_models = CoderedEventPage.__subclasses__()
        dt_start_str = utils.fix_ical_datetime_format(request.POST['datetime_start'])
        dt_end_str = utils.fix_ical_datetime_format(request.POST['datetime_end'])

        dt_start = datetime.strptime(dt_start_str, "%Y-%m-%dT%H:%M:%S%z") if dt_start_str else None
        dt_end = datetime.strptime(dt_end_str, "%Y-%m-%dT%H:%M:%S%z") if dt_end_str else None
        for event_page_model in event_page_models:
            try:
                event = event_page_model.objects.get(pk=event_pk)
                break
            except ObjectDoesNotExist:
                pass
        ical = Calendar()
        ical.add_component(event.create_single_ical(dt_start=dt_start, dt_end=dt_end))
        response = HttpResponse(ical.to_ical(), content_type="text/calendar")
        response['Filename'] = "{0}.ics".format(event.slug)
        response['Content-Disposition'] = 'attachment; filename={0}.ics'.format(event.slug)
        return response
    raise Http404()

def generate_recurring_ical_for_event(request):
    if request.method == "POST":
        event_pk = request.POST['event_pk']
        event_page_models = CoderedEventPage.__subclasses__()
        for event_page_model in event_page_models:
            try:
                event = event_page_model.objects.get(pk=event_pk)
                break
            except ObjectDoesNotExist:
                pass
        ical = Calendar()
        for e in event.create_recurring_ical():
            ical.add_component(e)
        response = HttpResponse(ical.to_ical(), content_type="text/calendar")
        response['Filename'] = "{0}.ics".format(event.slug)
        response['Content-Disposition'] = 'attachment; filename={0}.ics'.format(event.slug)
        return response
    raise Http404()

def generate_ical_for_calendar(request):
    if request.method == "POST":
        tag_pks = request.POST.getlist('tag_pks')
        event_page_models = CoderedEventPage.__subclasses__()
        event_pages = []
        if tag_pks:
            for event_page_model in event_page_models:
                event_pages += list(event_page_model.objects.filter(tags__pk__in=tag_pks).distinct())
        else:
            for event_page_model in event_page_models:
                event_pages += list(event_page_model.objects.all())
        
        ical = Calendar()
        for event_page in event_pages:
            for e in event_page.specific.create_recurring_ical():
                ical.add_component(e)
        response = HttpResponse(ical.to_ical(), content_type="text/calendar")
        response['Filename'] = "calendar.ics"
        response['Content-Disposition'] = 'attachment; filename=calendar.ics'
        return response
    raise Http404()

def get_calendar_events(request):
    if request.is_ajax():
        try:
            tags = ast.literal_eval(request.POST.get('tags'))
        except ValueError:
            tags = None
        start_str = request.POST.get('start')
        start = datetime.strptime(start_str[:10], "%Y-%m-%d") if start_str else None
        end_str = request.POST.get('end')
        end = datetime.strptime(end_str[:10], "%Y-%m-%d") if end_str else None
        return JsonResponse(CoderedEventPage.get_calendar_events(tags=tags, start=start, end=end), safe=False)
    raise Http404()