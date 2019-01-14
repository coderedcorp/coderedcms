Integrations
=============

Information about various integrations with 3rd party services can be found here.


Mailchimp
---------

Implementations of the abstract `CoderedFormPage` can add their form submissions to a Mailchimp list.
When this functionality is enabled, you can map form submission variables to merge variables and add 
form submissions to specific interest groups.

Implmenetation
~~~~~~~~~~~~~~

By default, when you generate a website, you will get an implementation of `CoderedFormPage`.
To get the functionality working, you need to do the following:

- Implmenet the abstract `MailchimpSubscriberIntegration` class with a `ParentalKey` that points to your `FormPage`
- Add an `integrations_panels` variable to `FormPage` that holds an `InlinePanel` for your implemented `MailchimpSubscriberIntegration` class

Here is what the resulting code will look like in ``website/models.py``::

    from modelcluster.fields import ParentalKey
    from coderedcms.models import CoderedFormPage, MailchimpSubscriberIntegration
    from wagtail.admin.edit_handlers import InlinePanel

    class FormPageMailchimpSubscriberIntegration(MailchimpSubscriberIntegration):
        page = ParentalKey('FormPage', related_name='mailchimp_subscriber_integrations', on_delete=models.CASCADE)


    class FormPage(CoderedFormPage):
        """
        A page with an html <form>.
        """
        class Meta:
            verbose_name = 'Form'

        template = 'coderedcms/pages/form_page.html'

        integration_panels = [
            InlinePanel('mailchimp_subscriber_integrations',
                heading="Mailchimp Subscriber Integrations",
            )
        ]


Next run ``python manage.py makemigrations website`` and ``python manage.py migrate`` to
make the changes to your project.  You will also need to add your api key to the Mailchimp API settings in the CMS.

How to Use
~~~~~~~~~~
When you make or edit a `FormPage`, you will now see an "Integrations" tab.  Clicking the plus icon will instantiate an integration. 
You can add as many of these integraitons objects as you need.  This is useful if you want to send a submission to more than one list.
When you select a list, the instance will load in the merge variables and interest categories.  The interest categories are straightforward.
You just select the interests you want the submission to have.

The merge variables are a bit more complex.  They work similarly to the emails that are sent after a form submission.  
You can decide what values from your form are put into which merge variables.  These values will get rendered by the Django renderer, as such
they use the same syntax.  The context for the render will be your form submission fields.  For example, if you have fields named "Email Address",
"First Name", "Phone", the context variables will be `email_address`, `first_name`, `phone`.  So if you have a merge variable, FIRSTNAME, you would want
to input `{{ first_name }}` into that field.

That's it.  Whenever a user fills out the form on the front end, they will be subscribed to your Mailchimp list with the merge fields and interest categories that you configure.
