from wagtail.core.models import Site
from coderedcms.models.wagtailsettings_models import MailchimpApiSettings

import requests


class MailchimpApi:
    user_string = "Website"
    proto_base_url = "https://{0}.api.mailchimp.com/3.0/"

    def __init__(self, site=None):
        self.set_access_token(site=None)

    def set_access_token(self, site=None):
        site = site or Site.objects.get(is_default_site=True)
        self.access_token = MailchimpApiSettings.for_site(site).mailchimp_api_key
        if self.access_token:
            self.set_base_url()
            self.is_active = True
        else:
            self.is_active = False

    def set_base_url(self):
        """
        The base url for the mailchimip api is dependent on the api key.
        """
        key, datacenter = self.access_token.split('-')
        self.base_url = self.proto_base_url.format(datacenter)

    def default_headers(self):
        return {
            "Content-Type": "application/json",
        }

    def default_auth(self):
        return (self.user_string, self.access_token)

    def get_lists(self):
        endpoint = "lists?fields=lists.name,lists.id"
        json_response = self._get(endpoint)
        return json_response

    def get_merge_fields_for_list(self, list_id):
        endpoint = "lists/{0}/merge-fields?fields=merge_fields.tag,merge_fields.merge_id,merge_fields.name".format(list_id)  # noqa
        json_response = self._get(endpoint)
        return json_response

    def get_interest_categories_for_list(self, list_id):
        endpoint = "lists/{0}/interest-categories?fields=categories.id,categories.title".format(
            list_id)
        json_response = self._get(endpoint)
        return json_response

    def get_interests_for_interest_category(self, list_id, interest_category_id):
        endpoint = "lists/{0}/interest-categories/{1}/interests?fields=interests.id,interests.name".format(list_id, interest_category_id)  # noqa
        json_response = self._get(endpoint)
        return json_response

    def add_user_to_list(self, list_id, data):
        endpoint = "lists/{0}".format(list_id)
        json_response = self._post(endpoint, data=data)
        return json_response

    def _get(self, endpoint, data={}, auth=None, headers=None, **kwargs):
        auth = auth or self.default_auth()
        headers = headers or self.default_headers()
        full_url = "{0}{1}".format(self.base_url, endpoint)
        r = requests.get(full_url, auth=auth, headers=headers, data=data, **kwargs)
        return r.json()

    def _post(self, endpoint, data={}, auth=None, headers=None, **kwargs):
        auth = auth or self.default_auth()
        headers = headers or self.default_headers()
        full_url = "{0}{1}".format(self.base_url, endpoint)
        r = requests.post(full_url, auth=auth, headers=headers, data=data, **kwargs)
        return r.json()
