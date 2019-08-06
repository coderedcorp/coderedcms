Translation
===========

Static content
----------------------

Due to CoderedCMS being heavily based on Wagtail, PO (Portable Objects) files translation follows Django's ``i18n`` pattern system. You are therefore encouraged to read Wagtail's official `documentation <http://docs.wagtail.io/en/latest/advanced_topics/i18n/>`_ on the topic.

Models
------

Translation of model fields can be most efficiently and safely achieved via the well-known `Wagtail Model Translation <https://github.com/infoportugal/wagtail-modeltranslation>`_ package.

Please note that, due to CoderedCMS' specific architecture, some fields are not exposed to the translation package by default, but it is required to do so inside ``models.py``.

See below how that would be done for the ``body`` field for a specific ``MyPageModel``:

.. code-block:: python

    class MyPageModel(ParentModel):
        body_content_panels = []
        content_panels = ParentModel.content_panels + [
            StreamFieldPanel('body'),
        ]

Admin panel
-----------
As explained in the Wagtail's official `documentation <http://docs.wagtail.io/en/latest/advanced_topics/i18n/>`_, you can easily enable a default language in the administration panel. You are encouraged to contribute to the project with translations.
