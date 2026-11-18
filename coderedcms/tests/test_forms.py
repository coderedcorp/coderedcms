import unittest

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from wagtail.models import Page

from coderedcms.tests.testapp.models import FormPage
from coderedcms.tests.testapp.models import FormPageField
from coderedcms.tests.testapp.models import StreamFormPage


@pytest.mark.django_db
class TestFormSubmissionsAdmin(unittest.TestCase):
    """The Wagtail admin "Forms" area must list and show submissions for
    CodeRed form pages.

    Regression test for the 404 introduced when Wagtail 7.x began guarding its
    admin submissions view with ``isinstance(page, FormMixin)`` (and calling
    ``page.get_submissions()``), which CodeRed form pages did not satisfy.
    See https://github.com/coderedcorp/coderedcms/issues/710
    """

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(self.user)
        self.root_page = Page.get_root_nodes()[0]

    def _make_form_page(self):
        form_page = FormPage(title="Contact", slug="contact")
        self.root_page.add_child(instance=form_page)
        FormPageField.objects.create(
            page=form_page,
            sort_order=0,
            label="Your name",
            field_type="singleline",
            required=True,
        )
        return form_page

    def test_form_index_lists_codered_form(self):
        self._make_form_page()
        response = self.client.get(reverse("wagtailforms:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Contact", response.content)

    def test_codered_form_submissions_view(self):
        form_page = self._make_form_page()
        response = self.client.get(
            reverse("wagtailforms:list_submissions", args=[form_page.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_codered_stream_form_submissions_view(self):
        stream_page = StreamFormPage(title="Survey", slug="survey")
        self.root_page.add_child(instance=stream_page)
        response = self.client.get(
            reverse("wagtailforms:list_submissions", args=[stream_page.pk])
        )
        self.assertEqual(response.status_code, 200)
