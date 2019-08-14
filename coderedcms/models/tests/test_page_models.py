from django.test import Client
from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Site

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
from coderedcms.models.wagtailsettings_models import (
    SeoSettings
)


class BasicPageTestCase():
    """
    This is a testing mixin used to run common tests for basic versions of page types.
    """
    class Meta:
        abstract = True

    def setUp(self):
        self.client = Client()
        self.basic_page = self.model(
            title=str(self.model._meta.verbose_name)
        )
        self.homepage = WebPage.objects.get(url_path='/home/')
        self.homepage.add_child(instance=self.basic_page)

    def test_get(self):
        """
        Tests to make sure a basic version of the page serves a 200 from a GET request.
        """

        response = self.client.get(self.basic_page.url, follow=True)
        self.assertEqual(response.status_code, 200)


class AbstractPageTestCase():
    """
    This is a testing mixin used to run common tests for abstract page types.
    """
    class Meta:
        abstract = True

    def test_not_available(self):
        """
        Tests to make sure the page is not creatable and not in CodeRed CMS's global list of page models.  # noqa
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
        response = self.client.post(self.basic_page.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_spam(self):
        """
        Test to check if the default spam catching works.
        """
        response = self.client.post(self.basic_page.url, {'cr-decoy-comments': 'This is Spam'}, follow=True)  # noqa
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), self.basic_page.get_spam_message())

    def test_not_spam(self):
        """
        Test to check if the default spam catching won't mark correct posts as spam.
        """
        response = self.client.post(self.basic_page.url)
        self.assertFalse(hasattr(response, 'is_spam'))


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


class CoderedStreamFormPageTestCase(AbstractPageTestCase, WagtailPageTests):
    model = CoderedStreamFormPage


class ArticlePageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = ArticlePage

    def test_amp(self):
        site = Site.objects.filter(is_default_site=True)[0]
        settings = SeoSettings.for_site(site)
        settings.amp_pages = True
        settings.save()

        response = self.client.get(self.basic_page.url + '?amp')
        self.assertEqual(response.status_code, 200)


class ArticleIndexPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
    model = ArticleIndexPage


class FormPageTestCase(ConcreteFormPageTestCase, WagtailPageTests):
    model = FormPage


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


class StreamFormPageTestCase(ConcreteFormPageTestCase, WagtailPageTests):
    model = StreamFormPage
