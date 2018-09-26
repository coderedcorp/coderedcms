from itertools import chain

from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.shortcuts import render
from wagtail.search.backends import db, get_search_backend
from wagtail.search.models import Query

from coderedcms.core.models import CoderedPage, get_page_models, GeneralSettings
from coderedcms.search.forms import SearchForm


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
    return render(request, 'search/search.html', {
        'request': request,
        'pagetypes': pagetypes,
        'form': search_form,
        'results': results,
        'results_paginated': results_paginated
    })