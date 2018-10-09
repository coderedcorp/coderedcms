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
class CoderedCMSPageTestCase(TestCase):

    def test_CoderedArticleIndexPage_not_available(self):
        self.assertFalse(CoderedArticleIndexPage.is_creatable)
        self.assertFalse(CoderedArticleIndexPage in get_page_models())

    def test_CoderedArticlePage_not_available(self):
        self.assertFalse(CoderedArticlePage.is_creatable)
        self.assertFalse(CoderedArticlePage in get_page_models())

    def test_CoderedFormPage_not_available(self):
        self.assertFalse(CoderedFormPage.is_creatable)
        self.assertFalse(CoderedFormPage in get_page_models())

    def test_CoderedPage_not_available(self):
        self.assertFalse(CoderedPage.is_creatable)
        self.assertTrue(CoderedPage in get_page_models())

    def test_CoderedWebPage_not_available(self):
        self.assertFalse(CoderedWebPage.is_creatable)
        self.assertFalse(CoderedWebPage in get_page_models())


class WebsitePageTestCase(TestCase):

    def test_ArticlePage_available(self):
        self.assertTrue(ArticlePage.is_creatable)
        self.assertTrue(WebPage in get_page_models())

    def test_ArticleIndexPage_available(self):
        self.assertTrue(ArticleIndexPage.is_creatable)
        self.assertTrue(ArticleIndexPage in get_page_models())

    def test_FormPage_available(self):
        self.assertTrue(FormPage.is_creatable)
        self.assertTrue(FormPage in get_page_models())

    def test_WebPage_available(self):
        self.assertTrue(WebPage.is_creatable)
        self.assertTrue(WebPage in get_page_models())