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
By default, search results can be filtered by the page type to allow for a more specific search.


To all filtering only by specific page types, add ``search_filterable = True`` to the page model.
The ``verbose_name`` and ``verbose_name_plural`` fields are then used to display the labels for
these filters.
For example, to specify search filtering only by Blog or by Products in addition to All Results::

    class BlogPage(CoderedArticlePage):
        search_filterable = True

    class Product(CoderedWebPage):
        search_filterable = True

Would enable the following filter options on the search page: All Results, Blog, Products.
