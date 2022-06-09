from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import Drawing


class TestDrawingModel(TestCase):
    """
    Tests that the Drawing model is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )
        # create a test drawing object
        Drawing.objects.create(
            title="Test Drawing",
            save_slot=1,
            user_account=self.test_user.useraccount,
            image=SimpleUploadedFile(
                name="test_image.png",
                content=open("./media/testing/test_image.png", "rb").read(),
            ),
        )

    def test_drawing_string_method(self):
        drawing = Drawing.objects.get(title="Test Drawing")
        self.assertEqual(
            str(drawing),
            f"{drawing.user_account} - Drawing {drawing.save_slot}",
        )
