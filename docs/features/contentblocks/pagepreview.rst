Page Preview Block
==================

Shows a miniview (a condensed version) of a selected Page.

Field Reference
---------------

**Page to Preview** - Select the page that you want to display a preview

.. figure:: images/page_preview_editor.jpeg
    :alt: A Page Preview block and its settings

    A Page Preview block and its settings

The selected page is rendered using the page model's "miniview" template.
The template can be overridden per model with the ``miniview_template`` attribute, the default of which is `coderedcms/pages/page.mini.html <https://github.com/coderedcorp/coderedcms/blob/main/coderedcms/templates/coderedcms/pages/pages.mini.html>`_.

.. figure:: images/page_preview_card.jpeg
    :alt: A Page Preview block using the card template

    Most pages use the built-in card miniview.

.. figure:: images/page_preview_form.jpeg
    :alt: A Page Preview block using the form inputs template

    Forms use the built-in form miniview.

.. versionadded:: 2.1

   Miniview templates were added in Wagtail CRX 2.1
