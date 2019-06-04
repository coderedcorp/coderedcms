from django.contrib.auth.models import AnonymousUser
from wagtail.tests.utils import WagtailPageTests
from django.test.client import RequestFactory
from wagtail.core.models import Site

from coderedcms.models.snippet_models import (
    Classifier
)

class BasicPageTestCase():
    """
    This is a testing mixin for testing snippets
    """
    def setup(self):
        pass # Need to research how a snippet is set up for testing

    def test_slug(self):
        self.save()
        assertTrue(self.slug != None)


class ClassifierTestCase(BasicPageTestCase): # Are there wagtail snippet tests?
    model = Classifier
