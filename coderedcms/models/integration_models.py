from django.db import models
from django.forms.widgets import Input
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import hooks

from coderedcms.api.mailchimp import MailchimpApi

import json


class MailchimpSubscriberIntegrationWidget(Input):
    template_name = 'coderedcms/formfields/mailchimp/subscriber_integration_widget.html'
    js_template_name = 'coderedcms/formfields/mailchimp/subscriber_integration_js.html'

    def get_context(self, name, value, attrs):
        ctx = super(MailchimpSubscriberIntegrationWidget, self).get_context(name, value, attrs)

        json_value = self.get_json_value(value)
        list_library = self.build_list_library()
        ctx['widget']['value'] = json.dumps(json_value)
        ctx['widget']['extra_js'] = self.render_js(name, list_library, json_value)
        ctx['widget']['selectable_mailchimp_lists'] = self.get_selectable_mailchimp_lists(
            list_library)
        ctx['widget']['stored_mailchimp_list'] = self.get_stored_mailchimp_list(json_value)

        return ctx

    def render_js(self, name, list_library, json_value):
        ctx = {
            'widget_name': name,
            'widget_js_name': name.replace('-', '_'),
            'list_library': list_library,
            'stored_mailchimp_list': self.get_stored_mailchimp_list(json_value),
            'stored_merge_fields': self.get_stored_merge_fields(json_value),
        }

        return render_to_string(self.js_template_name, ctx)

    def get_json_value(self, value):
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
        if 'interest_categories' not in json_value:
            json_value['interest_categories'] = {}
        return json_value

    def get_stored_mailchimp_list(self, value):
        if 'list_id' in value:
            return str(value['list_id'])

    def get_stored_merge_fields(self, value):
        if 'merge_fields' in value:
            return json.dumps(value['merge_fields'])
        return json.dumps({})

    def get_selectable_mailchimp_lists(self, library):
        selectable_lists = [('', '--- Select a Mailchimp List ---')]
        for k, v in library.items():
            selectable_lists.append((k, v['name']))

        return selectable_lists

    def build_list_library(self):
        mailchimp = MailchimpApi()
        list_library = {}
        if mailchimp.is_active:
            lists = mailchimp.get_lists()
            for mlist in lists['lists']:
                list_library[mlist['id']] = {
                    'name': mlist['name'],
                    'merge_fields': {},
                    'interest_categories': {}
                }

                list_library[mlist['id']]['merge_fields'] = \
                    mailchimp.get_merge_fields_for_list(mlist['id'])['merge_fields']
                list_library[mlist['id']]['interest_categories'] = \
                    mailchimp.get_interest_categories_for_list(mlist['id'])['categories']

                for category in list_library[mlist['id']]['interest_categories']:
                    category['interests'] = mailchimp.get_interests_for_interest_category(
                        mlist['id'],
                        category['id']
                    )['interests']

        return list_library


class MailchimpSubscriberIntegration(models.Model):
    class Meta:
        abstract = True

    subscriber_json_data = models.TextField(
        blank=True,
        verbose_name=_("List")
    )

    def integration_operation(self, instance, **kwargs):
        mailchimp = MailchimpApi()
        if mailchimp.is_active:
            submission_dict = kwargs['form_submission'].get_data()
            rendered_dictionary = self.render_dictionary(submission_dict)
            mailchimp.add_user_to_list(list_id=self.get_list_id(), data=rendered_dictionary)

    def get_data(self):
        return json.loads(self.subscriber_json_data)

    def get_merge_fields(self):
        if 'merge_fields' in self.get_data():
            return self.get_data()['merge_fields']
        return {}

    def get_list_id(self):
        if 'list_id' in self.get_data():
            return self.get_data()['list_id']

    def combine_interest_categories(self):
        interest_dict = {}
        for category_id, value in self.get_data()['interest_categories'].items():
            interest_dict.update(value['interests'])

        return interest_dict

    def render_dictionary(self, form_submission):
        rendered_dictionary_template = json.dumps({
            'members': [
                {
                    'email_address': self.get_data()['email_field'],
                    'merge_fields': self.get_data()['merge_fields'],
                    'interests': self.combine_interest_categories(),
                    'status': 'subscribed',
                }
            ],
            'update_existing': True
        })

        rendered_dictionary = Template(
            rendered_dictionary_template).render(Context(form_submission))
        return rendered_dictionary

    panels = [
        FieldPanel('subscriber_json_data', widget=MailchimpSubscriberIntegrationWidget)
    ]


@hooks.register('form_page_submit')
def run_mailchimp_subscriber_integrations(instance, **kwargs):
    if hasattr(instance, 'integration_panels'):
        for panel in instance.integration_panels:
            for integration in getattr(instance, panel.relation_name).all():
                integration.integration_operation(instance, **kwargs)
