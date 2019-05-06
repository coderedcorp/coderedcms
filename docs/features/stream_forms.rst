Stream Forms
=============

Codered CMS integrates with ``wagtail_flexible_forms`` (https://github.com/noripyt/wagtail-flexible-forms).  This integration allows the creation of
a ``StreamFormPage``.  This page allows you to construct step-based advanced forms with streamfields.  Additionally, the form submission is tied to a session, so your users can fill out part of a form and pick it back up later.


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