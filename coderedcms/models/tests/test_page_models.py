from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from django.http import HttpRequest
from wagtail.core.models import Site

from coderedcms.models.page_models import (
    CoderedArticleIndexPage,
    CoderedArticlePage,
    CoderedFormPage,
    CoderedPage,
    CoderedWebPage,
    get_page_models
)
from coderedcms.tests.testapp.models import (
    ArticlePage,
    ArticleIndexPage,
    FormPage,
    WebPage
)


class NotCreatablePageTestCase():

    def test_not_available(self):
        self.assertFalse(self.model.is_creatable)
        self.assertFalse(self.model in get_page_models())


class CreatablePageTestCase():

    def test_is_available(self):
        self.assertTrue(self.model.is_creatable)
        self.assertTrue(self.model in get_page_models())

    def setUp(self):
        self.request_factory = RequestFactory()
        self.basic_page = self.model(
            title=str(self.model._meta.verbose_name)
        )
        self.homepage = WebPage.objects.get(url_path='/home/')
        self.homepage.add_child(instance=self.basic_page)

    def test_request(self):
        request = self.request_factory.post(self.basic_page.url)
        response = self.basic_page.serve(request)
        self.assertEqual(response.status_code, 200)


class CoderedArticleIndexPageTestCase(NotCreatablePageTestCase, TestCase):
    model = CoderedArticleIndexPage


class CoderedArticlePageTestCase(NotCreatablePageTestCase, TestCase):
    model = CoderedArticlePage


class CoderedFormPageTestCase(NotCreatablePageTestCase, TestCase):
    model = CoderedFormPage


class CoderedPageTestCase(NotCreatablePageTestCase, TestCase):
    model = CoderedPage

    def test_not_available(self):
        self.assertFalse(self.model.is_creatable)
        self.assertTrue(self.model in get_page_models())


class CoderedWebPageTestCase(NotCreatablePageTestCase, TestCase):
    model = CoderedWebPage


class ArticlePageTestCase(CreatablePageTestCase, TestCase):
    model = ArticlePage


class ArticleIndexPageTestCase(CreatablePageTestCase, TestCase):
    model = ArticleIndexPage


class FormPageTestCase(CreatablePageTestCase, TestCase):
    model = FormPage


class WebPageTestCase(CreatablePageTestCase, TestCase):
    model = WebPage
