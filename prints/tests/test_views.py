import tempfile
from PIL import Image
from decimal import Decimal

from django.test import TestCase
from django.test import override_settings
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from prints.models import Product, ProductImage, ProductVariant
from accounts.models import Drawing

# tests which use temporary files will override MEDIA_ROOT and store files in
# this temporary directory path
TEMP_DIR = 'temp_test_data'


class TestShowAllPrintsView(TestCase):
    """
    Tests that the show_all_prints view is behaving as expected
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            # create ProductImage object
            product_image = ProductImage.objects.create(
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

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        # create a ProductVariant
        ProductVariant.objects.create(
            product=product,
            name="test_variant",
            display_name="Test Variant",
            price=Decimal("9.99"),
        )

    def test_get_show_all_prints_page(self):
        response = self.client.get(reverse("show_all_prints"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/show_all_prints.html")

    def test_view_returns_correct_contexts(self):
        response = self.client.get(reverse("show_all_prints"))

        self.assertIsInstance(response.context["products"], list)
        self.assertEqual(
            response.context["min_prices"], {"test_product": Decimal("9.99")}
        )


class TestProductDetailsView(TestCase):
    """
    Tests that the product_details view is behaving as expected
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            product_image = ProductImage.objects.create(
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

        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test drawing object with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            Drawing.objects.create(
                title="Saved Test Drawing",
                save_slot=1,
                user_account=self.test_user.useraccount,
                image=SimpleUploadedFile(
                    name="test_image.png",
                    content=temp_file.read(),
                ),
            )

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        # create a ProductVariant
        ProductVariant.objects.create(
            product=product,
            name="test_variant",
            display_name="Test Variant",
            description="A variant for testing",
            price=Decimal("9.99"),
        )

    def test_get_product_details_page(self):
        product = Product.objects.get(pk=1)
        response = self.client.get(
            reverse("product_details", args=(product.name,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/product_details.html")

    def test_view_returns_correct_contexts(self):
        self.client.login(username="testuser", password="123456")
        product = Product.objects.get(pk=1)
        response = self.client.get(
            reverse("product_details", args=(product.name,))
        )

        self.assertEqual(response.context["product"], product)
        self.assertIsInstance(response.context["variants"], QuerySet)
        self.assertIsInstance(response.context["saved_drawings"], QuerySet)
        self.assertIsInstance(
            response.context["json_data"]["drawingUrls"][1], str
        )
        self.assertEqual(
            response.context["json_data"]["variantPrices"][1], Decimal("9.99")
        )
        self.assertIsInstance(
            response.context["json_data"]["variantUrls"]["default"], str
        )
        self.assertEqual(
            response.context["json_data"]["overlay"]["default"],
            ["50%", "10%", "10%"],
        )
        self.assertEqual(
            response.context["json_data"]["placeholder"],
            "/media/svg/placeholder.svg",
        )


class TestProductManagementView(TestCase):
    """
    Tests that the product_management view is behaving as expected
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_product_management_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("product_management"))
        self.assertRedirects(
            response, "/admin/login/?next=/prints/product_management/"
        )
        self.assertEqual(response.status_code, 302)

    def test_get_product_management_page(self):
        self.client.login(username="teststaffuser", password="123456")
        response = self.client.get(reverse("product_management"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/product_management.html")


class TestAddProductView(TestCase):
    """
    Tests that the add_product view is behaving as expected
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_add_product_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("add_product"))
        self.assertRedirects(
            response, "/admin/login/?next=/prints/add_product/"
        )
        self.assertEqual(response.status_code, 302)

    def test_get_add_product_page(self):
        self.client.login(username="teststaffuser", password="123456")
        response = self.client.get(reverse("add_product"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/add_product.html")


class TestEditProductView(TestCase):
    """
    Tests that the edit_product view is behaving as expected
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            product_image = ProductImage.objects.create(
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

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_edit_product_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        product = Product.objects.get(pk=1)
        response = self.client.get(reverse("edit_product", args=(product.id,)))
        self.assertRedirects(
            response, f"/admin/login/?next=/prints/edit_product/{product.id}/"
        )
        self.assertEqual(response.status_code, 302)

    def test_get_edit_product_page(self):
        self.client.login(username="teststaffuser", password="123456")
        product = Product.objects.get(pk=1)
        response = self.client.get(reverse("edit_product", args=(product.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/edit_product.html")


class TestDeleteProductView(TestCase):
    """
    Tests that the delete_product view is behaving as expected
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            product_image = ProductImage.objects.create(
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

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_delete_product_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        product = Product.objects.get(pk=1)
        response = self.client.get(
            reverse("delete_product", args=(product.id,))
        )
        self.assertRedirects(
            response,
            f"/admin/login/?next=/prints/delete_product/{product.id}/",
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_product(self):
        self.client.login(username="teststaffuser", password="123456")
        product = Product.objects.get(pk=1)
        response = self.client.get(
            reverse("delete_product", args=(product.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("product_management"))
        product_exists = Product.objects.filter(id=product.id).first()
        self.assertFalse(product_exists)


class TestAddProductVariantView(TestCase):
    """
    Tests that the add_product_variant view is behaving as expected
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_add_product_variant_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("add_product_variant"))
        self.assertRedirects(
            response, "/admin/login/?next=/prints/add_product_variant/"
        )
        self.assertEqual(response.status_code, 302)

    def test_get_add_product_variant_page(self):
        self.client.login(username="teststaffuser", password="123456")
        response = self.client.get(reverse("add_product_variant"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/add_product_variant.html")


class TestEditProductVariantView(TestCase):
    """
    Tests that the edit_product_variant view is behaving as expected
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            product_image = ProductImage.objects.create(
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

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        # create a ProductVariant
        ProductVariant.objects.create(
            product=product,
            name="test_variant",
            display_name="Test Variant",
            price=Decimal("9.99"),
        )

        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_edit_product_variant_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        product_variant = ProductVariant.objects.get(pk=1)
        response = self.client.get(
            reverse("edit_product_variant", args=(product_variant.id,))
        )
        self.assertRedirects(
            response,
            f"/admin/login/?next=/prints/edit_product_variant/"
            + f"{product_variant.id}/",
        )
        self.assertEqual(response.status_code, 302)

    def test_get_edit_product_variant_page(self):
        self.client.login(username="teststaffuser", password="123456")
        product_variant = ProductVariant.objects.get(pk=1)
        response = self.client.get(
            reverse("edit_product_variant", args=(product_variant.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/edit_product_variant.html")


class TestDeleteProductVariantView(TestCase):
    """
    Tests that the delete_product_variant view is behaving as expected
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            product_image = ProductImage.objects.create(
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

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        # create a ProductVariant
        ProductVariant.objects.create(
            product=product,
            name="test_variant",
            display_name="Test Variant",
            price=Decimal("9.99"),
        )

        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_delete_product_variant_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        product_variant = ProductVariant.objects.get(pk=1)
        response = self.client.get(
            reverse("delete_product_variant", args=(product_variant.id,))
        )
        self.assertRedirects(
            response,
            f"/admin/login/?next=/prints/delete_product_variant/"
            + f"{product_variant.id}/",
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_product_variant(self):
        self.client.login(username="teststaffuser", password="123456")
        product_variant = ProductVariant.objects.get(pk=1)
        response = self.client.get(
            reverse("delete_product_variant", args=(product_variant.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("product_management"))
        product_variant_exists = ProductVariant.objects.filter(
            id=product_variant.id
        ).first()
        self.assertFalse(product_variant_exists)


class TestAddProductImageView(TestCase):
    """
    Tests that the add_product_image view is behaving as expected
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_add_product_image_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("add_product_image"))
        self.assertRedirects(
            response, "/admin/login/?next=/prints/add_product_image/"
        )
        self.assertEqual(response.status_code, 302)

    def test_get_add_product_image_page(self):
        self.client.login(username="teststaffuser", password="123456")
        response = self.client.get(reverse("add_product_image"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/add_product_image.html")


class TestEditProductImageView(TestCase):
    """
    Tests that the edit_product_image view is behaving as expected
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            product_image = ProductImage.objects.create(
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

        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_edit_product_image_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        product_image = ProductImage.objects.get(pk=1)
        response = self.client.get(
            reverse("edit_product_image", args=(product_image.id,))
        )
        self.assertRedirects(
            response,
            f"/admin/login/?next=/prints/edit_product_image/"
            + f"{product_image.id}/",
        )
        self.assertEqual(response.status_code, 302)

    def test_get_edit_product_image_page(self):
        self.client.login(username="teststaffuser", password="123456")
        product_image = ProductImage.objects.get(pk=1)
        response = self.client.get(
            reverse("edit_product_image", args=(product_image.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/edit_product_image.html")


class TestDeleteProductImageView(TestCase):
    """
    Tests that the delete_product_image view is behaving as expected
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            product_image = ProductImage.objects.create(
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

        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test staff user
        self.test_staff_user = User.objects.create_user(
            username="teststaffuser", password="123456", is_staff=True
        )

    def test_delete_product_image_view_redirects_non_staff(self):
        self.client.login(username="testuser", password="123456")
        product_image = ProductImage.objects.get(pk=1)
        response = self.client.get(
            reverse("delete_product_image", args=(product_image.id,))
        )
        self.assertRedirects(
            response,
            f"/admin/login/?next=/prints/delete_product_image/"
            + f"{product_image.id}/",
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_product_image(self):
        self.client.login(username="teststaffuser", password="123456")
        product_image = ProductImage.objects.get(pk=1)
        response = self.client.get(
            reverse("delete_product_image", args=(product_image.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("product_management"))
        product_image_exists = ProductImage.objects.filter(
            id=product_image.id
        ).first()
        self.assertFalse(product_image_exists)
