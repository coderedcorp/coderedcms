from django.test import TestCase
from coderedcms.models.page_models import (
    CoderedArticleIndexPage,
    CoderedArticlePage,
    CoderedFormPage,
    CoderedPage,
    CoderedWebPage,
    get_page_models
)
from website.models import (
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
