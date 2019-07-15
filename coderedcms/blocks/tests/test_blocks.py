from coderedcms.blocks import base_blocks
from django.test import SimpleTestCase

from wagtail.tests.utils import WagtailTestUtils


class TestMultiSelectBlock(WagtailTestUtils, SimpleTestCase):
    def test_render_single_choice(self):
        block = base_blocks.MultiSelectBlock(
            choices=[('tea', 'Tea'), ('coffee', 'Coffee'), ('water', 'Water')])
        html = block.render_form(['tea'])
        self.assertInHTML('<option value="tea" selected>Tea</option>', html)
        self.assertTrue(html.count('selected'), 1)

    def test_render_multi_choice(self):
        block = base_blocks.MultiSelectBlock(
            choices=[('tea', 'Tea'), ('coffee', 'Coffee'), ('water', 'Water')])
        html = block.render_form(['coffee', 'tea'])
        self.assertInHTML('<option value="tea" selected>Tea</option>', html)
        self.assertInHTML('<option value="coffee" selected>Coffee</option>', html)
        self.assertTrue(html.count('selected'), 2)
