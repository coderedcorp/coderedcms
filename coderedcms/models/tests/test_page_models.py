from django.contrib.auth.models import AnonymousUser
from wagtail.tests.utils import WagtailPageTests
from django.test.client import RequestFactory
from wagtail.core.models import Site

from django.core.paginator import InvalidPage, EmptyPage, PageNotAnInteger

from coderedcms.models.page_models import (
    CoderedArticleIndexPage,
    CoderedArticlePage,
    CoderedEventIndexPage,
    CoderedEventPage,
    CoderedFormPage,
    CoderedLocationIndexPage,
    CoderedLocationPage,
    CoderedPage,
    CoderedStreamFormPage,
    CoderedWebPage,
    get_page_models
)
from coderedcms.tests.testapp.models import (
    ArticleIndexPage,
    ArticlePage,
    EventIndexPage,
    EventPage,
    FormPage,
    LocationIndexPage,
    LocationPage,
    StreamFormPage,
    WebPage
)


class BasicPageTestCase():
    """
    This is a testing mixin used to run common tests for basic versions of page types.
    """
    class Meta:
        abstract = True

    def setUp(self):
        self.request_factory = RequestFactory()
        self.basic_page = self.model(
            title=str(self.model._meta.verbose_name)
        )
        self.homepage = WebPage.objects.get(url_path='/home/')
        self.homepage.add_child(instance=self.basic_page)

    def test_get(self):
        """
        Tests to make sure a basic version of the page serves a 200 from a GET request.
        """
        request = self.request_factory.get(self.basic_page.url)
        request.session = self.client.session
        request.user = AnonymousUser()
        request.site = Site.objects.all()[0]
        response = self.basic_page.serve(request)
        self.assertEqual(response.status_code, 200)

    def test_amp(self):
        request = self.request_factory.get(self.basic_page.url)
        self.assertTrue(hasattr(self.model, "amp_template"))

    def test_preview(self):
        self.assertTrue(self.model.body_preview is not None)

    def test_paginator_not_an_integer(self):
        request = self.request_factory.get(self.basic_page.url, {"p": "A"})
        self.assertTrue(isinstance(self.basic_page.get_context(request), dict))

    def test_paginator_empty_page(self):
        request = self.request_factory.get(self.basic_page.url, {"p": ""})
        self.assertTrue(isinstance(self.basic_page.get_context(request), dict))

    def test_paginator_invalid_page(self):
        request = self.request_factory.get(self.basic_page.url, {"p": range(0, 5)})
        self.assertTrue(isinstance(self.basic_page.get_context(request), dict))


class AbstractPageTestCase():
    """
    This is a testing mixin used to run common tests for abstract page types.
    """
    class Meta:
        abstract = True

    def test_not_available(self):
        """
        Tests to make sure the page is not creatable and not in CodeRed CMS's global list of page models.
        """
        self.assertFalse(self.model.is_creatable)
        self.assertFalse(self.model in get_page_models())


class ConcretePageTestCase():
    """
    This is a testing mixin used to run common tests for concrete page types.
    """
    class Meta:
        abstract = True

    def test_is_available(self):
        """
        Tests to make sure the page is creatable and in CodeRed CMS's global list of page models.
        """
        self.assertTrue(self.model.is_creatable)
        self.assertTrue(self.model in get_page_models())


class ConcreteBasicPageTestCase(ConcretePageTestCase, BasicPageTestCase):
    class Meta:
        abstract = True


class ConcreteFormPageTestCase(ConcreteBasicPageTestCase):
    class Meta:
        abstract = True

    def test_post(self):
        """
        Tests to make sure a basic version of the page serves a 200 from a POST request.
        """
        request = self.request_factory.post(self.basic_page.url)
        request.session = self.client.session
        request.user = AnonymousUser()
        request.site = Site.objects.all()[0]
        response = self.basic_page.serve(request)
        self.assertEqual(response.status_code, 200)


class CoderedArticleIndexPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedArticleIndexPage


class CoderedArticlePageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedArticlePage

    def test_get_author_name(self):
        pass


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

    def test_most_recent_occurence(self):
        pass


class CoderedStreamFormPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedStreamFormPage


class ArticlePageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = ArticlePage


class ArticleIndexPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = ArticleIndexPage


class FormPageTestCase(ConcreteFormPageTestCase, WagtailPageTests):
    model = FormPage


class WebPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = WebPage


class EventIndexPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = EventIndexPage

    def test_get_index_children(self):
        pass


class EventPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = EventPage


class LocationIndexPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = LocationIndexPage


class LocationPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = LocationPage


# Does this page cause an error, or is it a test problem?
class StreamFormPageTestCase(ConcreteFormPageTestCase, WagtailPageTests):
   model = StreamFormPage
