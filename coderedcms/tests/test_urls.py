from django.test import Client
import unittest, pytest


@pytest.mark.django_db
class URLTestCase(unittest.TestCase):
    def test_404(self):
        client = Client()
        response = client.get("/testing/404/page/")
        self.assertEqual(response.status_code, 404)
