import copy
import csv
import mimetypes
import os
import re

from itertools import chain

from django import forms
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import ungettext, ugettext_lazy as _

from wagtailimportexport.forms import ImportFromFileForm
from wagtailimportexport.importing import update_page_references
from wagtail.admin import messages
from wagtail.core.models import Page
from wagtail.search.backends import db, get_search_backend
from wagtail.search.models import Query

from coderedcms import utils
from coderedcms.forms import SearchForm
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

@transaction.atomic()
def import_pages(import_data, parent_page):
    """
    Overwrite of the wagtailimportexport `import_page` function to handle generic csvs.
    The standard `import_pages` assumes that your pages will have a pk from the exported
    json files.  It does not facilitate the idea that the pages you import will be
    new pages.
    """

    pages_by_original_id = {}

    # First create the base Page records; these contain no foreign keys, so this allows us to
    # build a complete mapping from old IDs to new IDs before we go on to importing the
    # specific page models, which may require us to rewrite page IDs within foreign keys / rich
    # text / streamfields.
    page_content_type = ContentType.objects.get_for_model(Page)

    for (i, page_record) in enumerate(import_data['pages']):
        # build a base Page instance from the exported content (so that we pick up its title and other
        # core attributes)
        page = Page.from_serializable_data(page_record['content'])
        original_path = page.path
        original_id = page.id

        # clear id and treebeard-related fields so that they get reassigned when we save via add_child
        page.id = None
        page.path = None
        page.depth = None
        page.numchild = 0
        page.url_path = None
        page.content_type = page_content_type
        parent_page.add_child(instance=page)

        # Custom Code to add the new pk back into the original page record.
        page_record['content']['pk'] = page.pk

        pages_by_original_id[page.id] = page

    for (i, page_record) in enumerate(import_data['pages']):
        # Get the page model of the source page by app_label and model name
        # The content type ID of the source page is not in general the same
        # between the source and destination sites but the page model needs
        # to exist on both.
        # Raises LookupError exception if there is no matching model
        model = apps.get_model(page_record['app_label'], page_record['model'])

        specific_page = model.from_serializable_data(page_record['content'], check_fks=False, strict_fks=False)
        base_page = pages_by_original_id[specific_page.id]
        specific_page.page_ptr = base_page
        specific_page.__dict__.update(base_page.__dict__)
        specific_page.content_type = ContentType.objects.get_for_model(model)
        update_page_references(specific_page, pages_by_original_id)
        specific_page.save()

    return len(import_data['pages'])


def get_page_model_choices():
    return (
        (page.__name__, re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', page.__name__)) for page in get_page_models() if page.is_creatable
    )

class ImportPagesFromCSVFileForm(ImportFromFileForm):
    page_type = forms.ChoiceField(choices=get_page_model_choices)

def import_pages_from_csv_file(request):
    """
    Overwrite of the `import_pages` view from wagtailimportexport.  By default, the `import_pages` view
    expects a json file to be uploaded.  This view converts the uploaded csv into the json format that
    the importer expects.
    """

    def convert_csv_to_json(csv_file, page_type):
        pages_json = {
            "pages": [
            ]
        }
        default_page_data = {
          "app_label": "website",
          "content": {
            "pk": None,
          },
          "model": page_type
        }

        pages_csv_dict = csv.DictReader(csv_file)
        for row in pages_csv_dict:
            page_dict = copy.deepcopy(default_page_data)
            page_dict['content'].update(row)
            pages_json['pages'].append(page_dict)
        return pages_json

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
