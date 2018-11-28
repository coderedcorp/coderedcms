import mimetypes
import os

from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import ungettext, ugettext_lazy as _

from wagtail.admin import messages
from wagtail.search.backends import db, get_search_backend
from wagtail.search.models import Query

from coderedcms import utils
from coderedcms.forms import SearchForm
from coderedcms.importexport import convert_csv_to_json, import_pages, ImportPagesFromCSVFileForm
from coderedcms.models import CoderedPage, get_page_models, GeneralSettings
from coderedcms.settings import cr_settings

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

@login_required
def import_pages_from_csv_file(request):
    """
    Overwrite of the `import_pages` view from wagtailimportexport.  By default, the `import_pages` view
    expects a json file to be uploaded.  This view converts the uploaded csv into the json format that
    the importer expects.
    """

    if request.method == 'POST':
        form = ImportPagesFromCSVFileForm(request.POST, request.FILES)
        if form.is_valid():
            import_data = convert_csv_to_json(form.cleaned_data['file'].read().decode('utf-8').splitlines(), form.cleaned_data['page_type'])
            parent_page = form.cleaned_data['parent_page']
            try:
                page_count = import_pages(import_data, parent_page)
            except LookupError as e:
                messages.error(request, _(
                    "Import failed: %(reason)s") % {'reason': e}
                )
            else:
                messages.success(request, ungettext(
                    "%(count)s page imported.",
                    "%(count)s pages imported.",
                    page_count) % {'count': page_count}
                )
            return redirect('wagtailadmin_explore', parent_page.pk)
    else:
        form = ImportPagesFromCSVFileForm()

    return render(request, 'wagtailimportexport/import_from_csv.html', {
        'form': form,
    })
