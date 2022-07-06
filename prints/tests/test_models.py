import tempfile
from PIL import Image

from django.test import TestCase
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from prints.models import ProductImage, product_image_path

# tests which use temporary files will override MEDIA_ROOT and store files in
# this temporary directory path
TEMP_DIR = 'temp_test_data'


class TestProductImagePath(TestCase):
    """
    Tests that the product_image_path function is behaving as expected.
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def test_correct_path_is_returned(self):
        # create an image in a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            # create ProductImage object
            image = ProductImage.objects.create(
                name_slug="test_image",
                image_type=".jpg",
                overlay_width="50%",
                overlay_x_offset="10%",
                overlay_y_offset="10%",
                image=SimpleUploadedFile(
                    name="temp_file.jpg",
                    content=temp_file.read(),
                ),
            )

        # call function
        path = product_image_path(image, "0.jpg")
        self.assertEqual(path, "products/images/test_image.jpg")
