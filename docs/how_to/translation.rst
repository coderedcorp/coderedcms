Translation & Multi-Language Support
====================================


Translate the UI
----------------

CodeRed CMS provides all text throughout the UI and templates as translatable
strings using Django's internationalization system (often abbreviated "i18n").
To learn more about how translation works, read Wagtail's official `documentation
<http://docs.wagtail.io/en/latest/advanced_topics/i18n/>`_ on the topic.


Translate Page Content
----------------------

Translation of model fields can be most efficiently and safely achieved via the
well-known `Wagtail Model Translation <https://github.com/infoportugal/wagtail-modeltranslation>`_
package.

Please note that, due to CodeRed CMS architecture, some model fields are not exposed
to the translation package by default, but you can expose these fields in your ``models.py``.

See below how that would be done for the ``body`` field for a specific ``WebPage``
model in ``website/models.py``:

.. code-block:: python

    class WebPage(CoderedWebPage):
        body_content_panels = []
        content_panels = CodredWebPage.content_panels + [
            StreamFieldPanel('body'),
        ]


Changing Language of the Admin Dashboard
----------------------------------------

See Wagtail's `translation documentation <http://docs.wagtail.io/en/latest/advanced_topics/i18n/>`_,
to enable a default language in the administration panel.


Supported Languages
-------------------

CodeRed CMS is currently provided in English (US). However, it supports translation.
If you use CodeRed CMS in a different language, please consider contributing
your translations!
