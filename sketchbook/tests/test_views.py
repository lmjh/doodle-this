from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import Drawing


class TestSketchbookView(TestCase):
    """
    Tests that the Drawing model is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test drawing object with a title
        Drawing.objects.create(
            title="Saved Test Drawing",
            save_slot=1,
            user_account=self.test_user.useraccount,
            image=SimpleUploadedFile(
                name="test_image.png",
                content=open("./media/testing/test_image.png", "rb").read(),
            ),
        )

        # create a test drawing object without a title
        Drawing.objects.create(
            title="",
            save_slot=1,
            user_account=self.test_user.useraccount,
            image=SimpleUploadedFile(
                name="test_image.png",
                content=open("./media/testing/test_image.png", "rb").read(),
            ),
        )

    def test_get_sketchbook_page(self):
        response = self.client.get(reverse("sketchbook"))
        self.assertEqual(response.status_code, 200)

    def test_logged_out_view_contains_correct_contexts(self):
        response = self.client.get(reverse("sketchbook"))
        self.assertTemplateUsed(response, "sketchbook/sketchbook.html")
        self.assertIsNone(response.context["saved_drawings"])
        self.assertIsNone(response.context["form"])
        self.assertFalse(response.context["titles"])

    def test_logged_in_view_contains_correct_contexts(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("sketchbook"))
        self.assertIsNotNone(response.context["saved_drawings"])
        self.assertIsNotNone(response.context["form"])
        self.assertTrue(response.context["titles"])
        self.assertEqual(
            response.context["titles"]["title_1"], "Saved Test Drawing"
        )
        self.assertEqual(response.context["titles"]["title_2"], "")
