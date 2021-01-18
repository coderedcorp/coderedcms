import re

from django.template import engines
from django.test import TestCase


django_engine = engines['django']
html_id_re = re.compile(r"^[A-Za-z][A-Za-z0-9_:\.-]*$")


class TemplateTagTests(TestCase):
    def test_coderedcms_generate_random_id(self):
        count = 1000
        t = django_engine.from_string(
            "{% load coderedcms_tags %}{% generate_random_id as rid %}{{rid}}"
        )
        ids = set([])
        for i in range(count):
            ids.add(t.render())

        # ensure we are reasonably unique
        self.assertEqual(len(ids), count)

        # ensure ids are valid
        for i, value in enumerate(ids, start=1):
            self.assertTrue(
                html_id_re.match(value),
                'ID #%s "%s" did not match regex %r' % (i, value, html_id_re),
            )
