Translation & Multi-Language Support
====================================


Default Language
----------------

To adjust the default language of a project, navigate to
``projectname/settings/base.py``. Change both the ``LANGUAGE_CODE`` setting and
the ``LANGUAGES`` setting. For example:

.. code-block:: python

    LANGUAGE_CODE = 'es'

    LANGUAGES = [
        ('es', _('Spanish'))
    ]

Note that these settings are both in use to communicate to the users' browser
about the default language of the project. This ensures that users requiring
assistive technology have a smooth experience using the site. These settings do
not, on their own, translate or enable multiple languages on the project.

`See a full list of language codes from W3.
<https://www.w3docs.com/learn-html/html-language-codes.html>`_


Translate the UI
----------------

Wagtail CRX provides all text throughout the UI and templates as translatable
strings using Django's internationalization system (often abbreviated "i18n").
To learn more about how translation works, read Wagtail's official `documentation
<http://docs.wagtail.io/en/latest/advanced_topics/i18n/>`_ on the topic.


Translate Page Content
----------------------

Translation of model fields can be most efficiently and safely achieved via the
well-known `Wagtail Model Translation <https://github.com/infoportugal/wagtail-modeltranslation>`_
package.

Please note that, due to Wagtail CRX architecture, some model fields are not exposed
to the translation package by default, but you can expose these fields in your ``models.py``.

See below how that would be done for the ``body`` field for a specific ``WebPage``
model in ``website/models.py``:

.. code-block:: python

    class WebPage(CoderedWebPage):
        body_content_panels = []
        content_panels = CodredWebPage.content_panels + [
            'body',
        ]


Changing Language of the Admin Dashboard
----------------------------------------

See Wagtail's `translation documentation <http://docs.wagtail.io/en/latest/advanced_topics/i18n/>`_,
to enable a default language in the administration panel.


Supported Languages
-------------------

Wagtail CRX is currently provided in English (US). However, it supports translation.
If you use Wagtail CRX in a different language, please consider contributing
your translations!
