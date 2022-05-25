from django.test import TestCase

# Create your tests here.


class TestViews(TestCase):
    def test_get_sketchbook_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sketchbook/index.html")
