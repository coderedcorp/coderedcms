from django.test import TestCase
from django.test.client import RequestFactory
from coderedcms.models.wagtailsettings_models import LayoutSettings
from coderedcms.utils import convert_to_amp, process_richtext
from wagtail.core.models import Site


class AMPConversionTestCase(TestCase):
    """
    Test case for AMP tag conversions
    """

    def setUp(self):
        self.unprocessed_img_html = """<img src="/source.jpg" /><img src="/source2.jpg" />"""  # noqa
        self.unprocessed_iframe_html = """<iframe src="/source.html"></iframe><iframe src="/source-2.html"></iframe>"""  # noqa

        self.processed_amp_img_html = """<amp-img src="/source.jpg"/><amp-img src="/source2.jpg"/>"""  # noqa
        self.processed_amp_iframe_html = """<amp-iframe layout="responsive" src="/source.html"></amp-iframe><amp-iframe layout="responsive" src="/source-2.html"></amp-iframe>"""  # noqa

    def test_img_processing(self):
        """
        Test to verify img tags are converted to amp-img tags.
        """
        processed_html = convert_to_amp(self.unprocessed_img_html, pretty=False)
        self.assertEqual(processed_html, self.processed_amp_img_html)

    def test_iframe_processing(self):
        """
        Test to verify iframe tags are converted to amp-iframe tags.
        """
        processed_html = convert_to_amp(self.unprocessed_iframe_html, pretty=False)
        print(self.processed_amp_iframe_html)
        print(processed_html)
        self.assertEqual(processed_html, self.processed_amp_iframe_html)


class RichTextProcessingTestCase(TestCase):
    """
    Test case for richtext processing
    """

    def setUp(self):

        self.unprocessed_a_html = """<a href="www.google.com">Google</a><a href="www.yahoo.com">Yahoo</a>"""  # noqa
        self.processed_a_html = """<a href="www.google.com" target="_blank">Google</a><a href="www.yahoo.com" target="_blank">Yahoo</a>"""  # noqa

    def test_new_tab_setting(self):
        """
        Test to verify that the new_tab setting on LayoutSettings will
        change <a> tags in RichText Blocks to open in a new tab.
        """
        rf = RequestFactory()
        site = Site.objects.get(is_default_site=True)
        settings = LayoutSettings.for_site(site)
        settings.new_tab = True
        settings.save()
        request = rf.get('/home/')
        request.site = site
        processed_html = process_richtext(self.unprocessed_a_html, pretty=False, request=request)
        self.assertEqual(processed_html, self.processed_a_html)

        settings.new_tab = False
        settings.save()

        processed_html = process_richtext(self.unprocessed_a_html, pretty=False, request=request)
        self.assertEqual(processed_html, self.unprocessed_a_html)
