Latest Pages Block
==================

Creates a list of the most recently published pages with a specified length.

Field Reference
---------------

Fields and purposes:

* **Parent Page** - Shows a preview of pages that are children of the selected page. Uses ordering specified in the page’s LAYOUT tab.

* **Classified By** - Filters which pages are displayed by the classifier that you selected.

* **Number of Pages to Show** - Limits how many pages are displayed to the number that you selected.

Each page is rendered using the page model's "miniview" template.
The template can be overridden per model with the ``miniview_template`` attribute, the default of which is `coderedcms/pages/page.mini.html <https://github.com/coderedcorp/coderedcms/blob/main/coderedcms/templates/coderedcms/pages/pages.mini.html>`_.

.. figure:: img/latestpages1.png
    :alt: The Latest Pages block and its settings.

    The Latest Pages block and its settings.

.. figure:: img/latestpages2.png
    :alt: The Latest Pages block as displayed on the website.

    The Latest Pages block as displayed on the website.

.. versionadded:: 2.1

   Miniview templates were added in Wagtail CRX 2.1

.. deprecated:: 2.1

   * "Show Body Preview" field was deprecated in 2.1 and will be removed in 3.0.

   * The additional built-in templates under this block's **Advanced Settings** are deprecated as of 2.1 and will be removed in 3.0. These have been replaced with identical miniview templates for Article and Form pages.
