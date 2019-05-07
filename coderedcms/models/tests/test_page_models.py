from django.contrib.auth.models import AnonymousUser
from wagtail.tests.utils import WagtailPageTests
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

class CoderedArticleIndexPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedArticleIndexPage


class CoderedArticlePageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedArticlePage


class CoderedFormPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedFormPage


class CoderedPageTestCase(WagtailPageTests):
    model = CoderedPage

    def test_not_available(self):
        self.assertFalse(self.model.is_creatable)
        self.assertTrue(self.model in get_page_models())


class CoderedWebPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedWebPage


class CoderedLocationIndexPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedLocationIndexPage


class CoderedLocationPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedLocationPage


class CoderedEventIndexPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedEventIndexPage


class CoderedEventPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedEventPage


class ArticlePageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = ArticlePage


class ArticleIndexPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = ArticleIndexPage


class FormPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = FormPage

    def test_post(self):
        request = self.request_factory.post(self.basic_page.url)
        request.user = AnonymousUser()
        request.site = Site.objects.all()[0]
        response = self.basic_page.serve(request)
        self.assertEqual(response.status_code, 200)


class WebPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = WebPage


class EventIndexPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = EventIndexPage


class EventPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = EventPage


class LocationIndexPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = LocationIndexPage


class LocationPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = LocationPage
