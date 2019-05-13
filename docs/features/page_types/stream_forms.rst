Stream Forms
=============
CodeRed CMS integrates with ``wagtail_flexible_forms`` (https://github.com/noripyt/wagtail-flexible-forms).  This integration allows the creation of
a ``StreamForm``.  This page allows you to construct step-based advanced forms with streamfields.  Additionally, the form submission is tied to a session, so your users can fill out part of a form and pick it back up later.

Usage
-----

First start by creating a "Stream Form" (may be named differently on your specific website).  Add content to this page as you would for a normal Form.  By and large the editing experience is similar between a Form and a Stream Form.

Content Tab
~~~~~~~~~~~

**Form Fields**: This field is a bit different from its normal Form counterpart.  Instead of the normal Form's form field process, form fields are generated via a streamfield.  This is nice because it allows you to mix content into your form, in between form elements.  At the top level of the streamfield, you are able to create a step block.  Each step block represents a piece of the form that will be loaded one at a time.  In each step block is an additional streamfield that contains a mix of form fields and content blocks.

Implementation
--------------

The stream form functionality is built-in to CodeRed CMS but is not enabled by default. To implement, add
the following to your ``website/models.py``::

    from coderedcms.models import CoderedEmail, CoderedStreamFormPage

    class StreamFormPage(CoderedStreamFormPage):
        class Meta:
            verbose_name = 'Stream Form'

        template = 'coderedcms/pages/stream_form_page.html'

    class StreamFormConfirmEmail(CoderedEmail):
        page = ParentalKey('StreamFormPage', related_name='confirmation_emails')


Next run ``python manage.py makemigrations website`` and ``python manage.py migrate`` to create
the new pages in your project.