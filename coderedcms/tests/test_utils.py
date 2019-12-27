from django.test import TestCase
from coderedcms.utils import convert_to_amp


class AMPConversionTestCase(TestCase):
    """
    Test case for AMP tag conversions
    """

    def setUp(self):
        self.unprocessed_img_html = """<img src="/source.jpg" /><img src="/source2.jpg" />"""  # noqa
        self.unprocessed_iframe_html = """<iframe src="/source.html"></iframe><iframe src="/source-2.html"></iframe>"""  # noqa

        self.processed_amp_img_html = """<amp-img src="/source.jpg"></amp-img><amp-img src="/source2.jpg"></amp-img>"""  # noqa
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
