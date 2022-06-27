Searching
=========

A search page is available by default at the ``/search/`` URL, which can be customized in the
``urls.py`` file in your project. To enable a search bar in the navigation bar, check
Settings > Layout > Search box. Search results are paginated; to specify the number of results
per page, edit the value in Settings > General > Search Settings.

Search result formatting
------------------------

Each search result is rendered using the template at ``coderedcms/pages/search_result.html``.
The template can be overridden per model with the ``search_template`` attribute.

Search result filtering
-----------------------

To enable additional filtering by page type, add ``search_filterable = True`` to the page model.
The ``search_name`` and ``search_name_plural`` fields are then used to display the labels for
these filters (defaults to ``verbose_name`` and ``verbose_name_plural`` if not specified).
For example, to enable search filtering by Blog or by Products in addition to All Results::

    class BlogPage(CoderedArticlePage):
        search_filterable = True
        search_name = 'Blog Post'
        search_name_plural = 'Blog'

    class Product(CoderedWebPage):
        search_filterable = True
        search_name = 'Product'
        search_name_plural = 'Products'

Would enable the following filter options on the search page: All Results, Blog, Products.


Search fields
-------------

.. deprecated:: 0.25
    Use the `Wagtail search parameters <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html#module-wagtail.contrib.search_promotions>`_ instead.

If using the Wagtail DatabaseSearch backend (default), only page Title and Search Description
fields are searched upon. This is due to a limitation in the DatabaseSearch backend;
other backends such as PostgreSQL and Elasticsearch will search on additional specific fields
such as body, article captions, etc. To enable more specific searching while still using the
database backend, the specific models can be flagged for inclusion in search by setting
``search_db_include = True`` on the page model. Note that this must be set on every type of page
model you wish to include in search. When setting this flag, search is performed independently on
each page type, and the results are combined. So you may want to also specify ``search_db_boost`` (int)
to control the order in which the pages are searched. Pages with a higher ``search_db_boost``
are searched first, and results are shown higher in the list. For example::

    class Article(CoderedArticlePage):
        search_db_include = True
        search_db_boost = 10
        ...

    class WebPage(CoderedWebPage):
        search_db_include = True
        search_db_boost = 9
        ...

    class FormPage(CoderedFormPage):
        ...

In this example, Article search results will be shown before WebPage results when using the
DatabaseSearch backend. FormPage results will not be shown at all, due to the absence
``search_db_include``. If no models have ``search_db_include = True``, All CoderedPages
will be searched by title and description. When using any search backend other than database,
``search_db_*`` variables are ignored.
