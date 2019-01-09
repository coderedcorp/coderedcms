from django.db import models
from django.forms.widgets import Select, Input
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Orderable, Page
from modelcluster.fields import ParentalKey

from coderedcms.api.mailchimp import MailchimpApi

from ast import literal_eval
import json

class MailchimpSubscriberIntegrationWidget(Input):
    template_name = 'coderedcms/formfields/mailchimp/subscriber_integration_widget.html'

    def get_context(self, name, value, attrs):
        ctx = super(MailchimpSubscriberIntegrationWidget, self).get_context(name, value, attrs)

        json_value = self.get_json_value(value)
        selectable_lists = self.get_selectable_mailchimp_lists()
        ctx['widget']['value'] = json.dumps(json_value)
        ctx['widget']['stored_mailchimp_list'] = self.get_stored_mailchimp_list(json_value)
        ctx['widget']['stored_merge_fields'] = self.get_stored_merge_fields(json_value)
        ctx['widget']['merge_fields_library'] = self.get_merge_fields_library(selectable_lists)
        ctx['widget']['selectable_mailchimp_lists'] = [("", "Please select one of your Mailchimp Lists")] + selectable_lists
        return ctx

    def get_json_value(self, value):
        initial_value = '{"list_id": "", "merge_fields": {}, "email_field": ""}'
        if value:
            json_value = json.loads(value)
        else:
            json_value = json.loads('{}')
        if 'list_id' not in json_value:
            json_value['list_id'] = ""
        if 'merge_fields' not in json_value:
            json_value['merge_fields'] = {}
        if 'email_field' not in json_value:
            json_value['email_field'] = ""
        return json_value

    def get_stored_mailchimp_list(self, value):
        if 'list_id' in value:
            return str(value['list_id'])

    def get_stored_merge_fields(self, value):
        if 'merge_fields' in value:
            return json.dumps(value['merge_fields'])
        return json.dumps({})

    def get_selectable_mailchimp_lists(self):
        mailchimp = MailchimpApi()
        if mailchimp.is_active:
            lists = mailchimp.get_lists()
            return [(l['id'], l['name']) for l in lists['lists']]
        return [("", "Please add a Mailchimp API key in your settings to enable the Mailchimp integrations.")]  

    def get_merge_fields_library(self, mailchimp_list_tuples):
        mailchimp = MailchimpApi()
        if mailchimp.is_active:
            merge_fields_library = {}
            for tup in mailchimp_list_tuples:
                merge_fields_library[tup[0]] = []
                for merge_field in mailchimp.get_list_merge_fields(tup[0])['merge_fields']:
                    merge_fields_library[tup[0]].append(merge_field['tag'])
            return merge_fields_library
        return {}

class MailchimpSubscriberIntegration(models.Model):
    class Meta:
        abstract=True

    subscriber_json_data = models.TextField(
        blank=True,
        verbose_name=_("List")
    )

    def integration_signal_operation(self, instance, **kwargs):
        mailchimp = MailchimpApi()
        rendered_dictionary = self.render_dictionary(self.format_form_submission(kwargs['form_submission']))

        if mailchimp.is_active:
            mailchimp.add_user_to_list(list_id=self.get_list_id(), data=rendered_dictionary)

    def format_form_submission(self, form_submission):
        formatted_form_data = {}
        for k, v in literal_eval(form_submission.form_data).items():
            formatted_form_data[k.replace('-', '_')] = v
        return formatted_form_data

    def get_data(self):
        return json.loads(self.subscriber_json_data)

    def get_merge_fields(self):
        if 'merge_fields' in self.get_data():
            return self.get_data()['merge_fields']
        return {}

    def get_list_id(self):
        if 'list_id' in self.get_data():
            return self.get_data()['list_id']

    def render_dictionary(self, form_submission):
        rendered_dictionary_template = json.dumps({
            'members': [
                {
                    'email_address': self.get_data()['email_field'],
                    'merge_fields': self.get_data()['merge_fields'],
                    'status': 'subscribed',
                }
            ]
        })

        rendered_dictionary = Template(rendered_dictionary_template).render(Context(form_submission))
        return rendered_dictionary

    panels = [
        FieldPanel('subscriber_json_data', widget=MailchimpSubscriberIntegrationWidget)
    ]
