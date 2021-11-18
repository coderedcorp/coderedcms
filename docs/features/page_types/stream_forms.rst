Stream Forms
============

Wagtail CRX integrates with ``wagtail_flexible_forms`` (https://github.com/noripyt/wagtail-flexible-forms).
A Stream Form enables forms built from StreamFields for advanced functionality such as multi-step forms,
mixed content and form fields, and conditional logic.

.. note::
    Underlying functionality of Stream Forms may change in future versions as ``wagtail_flexible_forms``
    is planned to be merged directly into Wagtail. We recommend using the simpler ``CoderedFormPage``
    for forms that do not require advanced functionality (such as contact forms, etc.).


Usage
-----

First start by creating a "Stream Form" (may be named differently on your specific website).
Add content to this page as you would for a normal Form. By and large the editing experience
is similar between a Form and a Stream Form.


Conditional Logic
~~~~~~~~~~~~~~~~~

To enable conditional logic, click **Advanced Settings** and enter a "Custom ID" on a field.
Then on a second field, enter that same ID for "Condition Trigger ID" and a desired value for
"Condition Trigger Value". The second field will only then show if the trigger value is selected
in the first field. For example:

.. code-block:: text

    Field One (checkbox field):
      Custom ID: swallows-or-coconuts

      [ ] African Swallow
      [x] Coconut


    Field Two (text field):
      Condition Trigger ID: swallows-or-coconuts
      Condition Trigger Value: Coconut

In this scenario, Field Two will be shown because the user selected "Coconut" in Field One
(identified by: "swallows-or-coconuts"). If the user unchecks "Coconut", Field Two will
then be hidden.

.. note::
    As of version 0.15, fields with a Condition Trigger ID should NOT be marked required.


Content Tab
~~~~~~~~~~~

**Form Fields**: This field is a bit different from its normal Form counterpart.
Instead of the normal Form's form field process, form fields are generated via a StreamField.
This is nice because it allows you to mix content into your form, in between form elements.
At the top level of the StreamField, you are able to create a step block. Each step block represents
a piece of the form that will be loaded one at a time. In each step block is an additional
StreamField that contains a mix of form fields and content blocks.


Implementation
--------------

The stream form functionality is built-in to Wagtail CRX but is not enabled by default.
To implement, add the following to your ``website/models.py``

.. code-block:: python

    from coderedcms.models import CoderedEmail, CoderedStreamFormPage

    class StreamFormPage(CoderedStreamFormPage):
        class Meta:
            verbose_name = 'Stream Form'

        template = 'coderedcms/pages/stream_form_page.html'

    class StreamFormConfirmEmail(CoderedEmail):
        page = ParentalKey('StreamFormPage', related_name='confirmation_emails')


Next run ``python manage.py makemigrations website`` and ``python manage.py migrate`` to create
the new pages in your project.
