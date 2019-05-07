from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory
from wagtail.core.models import Site
from unittest import skip

from coderedcms.models.page_models import (
    CoderedArticleIndexPage,
    CoderedArticlePage,
    CoderedEventIndexPage,
    CoderedEventPage,
    CoderedFormPage,
    CoderedPage,
    CoderedWebPage,
    CoderedLocationIndexPage,
    CoderedLocationPage,
    get_page_models
)
from coderedcms.tests.testapp.models import (
    ArticlePage,
    ArticleIndexPage,
    FormPage,
    WebPage,
    EventPage,
    EventIndexPage,
    LocationPage,
    LocationIndexPage
)


class BasicPageTestCase():
    class Meta:
        abstract=True

    def setUp(self):
        self.request_factory = RequestFactory()
        self.basic_page = self.model(
            title=str(self.model._meta.verbose_name)
        )
        self.homepage = WebPage.objects.get(url_path='/home/')
        self.homepage.add_child(instance=self.basic_page)

    def test_get(self):
        request = self.request_factory.get(self.basic_page.url)
        request.user = AnonymousUser()
        request.site = Site.objects.all()[0]
        response = self.basic_page.serve(request)
        self.assertEqual(response.status_code, 200)

class AbstractPageTestCase():
    class Meta:
        abstract=True

    def test_not_available(self):
        self.assertFalse(self.model.is_creatable)
        self.assertFalse(self.model in get_page_models())


class ConcretePageTestCase():
    class Meta:
        abstract=True

    def test_is_available(self):
        self.assertTrue(self.model.is_creatable)
        self.assertTrue(self.model in get_page_models())


class ConcreteBasicPageTestCase(ConcretePageTestCase, BasicPageTestCase):
    class Meta:
        abstract=True

class CoderedArticleIndexPageTestCase(AbstractPageTestCase, TestCase):
    model = CoderedArticleIndexPage


class CoderedArticlePageTestCase(AbstractPageTestCase, TestCase):
    model = CoderedArticlePage


class CoderedFormPageTestCase(AbstractPageTestCase, TestCase):
    model = CoderedFormPage


class CoderedPageTestCase(TestCase):
    model = CoderedPage

    def test_not_available(self):
        self.assertFalse(self.model.is_creatable)
        self.assertTrue(self.model in get_page_models())


class CoderedWebPageTestCase(AbstractPageTestCase, TestCase):
    model = CoderedWebPage


class CoderedLocationIndexPageTestCase(AbstractPageTestCase, TestCase):
    model = CoderedLocationIndexPage


class CoderedLocationPageTestCase(AbstractPageTestCase, TestCase):
    model = CoderedLocationPage


class CoderedEventIndexPageTestCase(AbstractPageTestCase, TestCase):
    model = CoderedEventIndexPage


class CoderedEventPageTestCase(AbstractPageTestCase, TestCase):
    model = CoderedEventPage


class ArticlePageTestCase(ConcreteBasicPageTestCase, TestCase):
    model = ArticlePage


class ArticleIndexPageTestCase(ConcreteBasicPageTestCase, TestCase):
    model = ArticleIndexPage


class FormPageTestCase(ConcreteBasicPageTestCase, TestCase):
    model = FormPage


class WebPageTestCase(ConcreteBasicPageTestCase, TestCase):
    model = WebPage


class EventIndexPageTestCase(ConcreteBasicPageTestCase, TestCase):
    model = EventIndexPage


class EventPageTestCase(ConcreteBasicPageTestCase, TestCase):
    model = EventPage


class LocationIndexPageTestCase(ConcreteBasicPageTestCase, TestCase):
    model = LocationIndexPage


class LocationPageTestCase(ConcreteBasicPageTestCase, TestCase):
    model = LocationPage
