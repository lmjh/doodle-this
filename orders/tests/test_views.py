import tempfile
from PIL import Image
from decimal import Decimal

from django.test import TestCase
from django.test import override_settings
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from orders.models import Order, OrderDrawingCache
from prints.models import ProductVariant, Product, ProductImage
from accounts.models import Drawing

# tests which use temporary files will override MEDIA_ROOT and store files in
# this temporary directory path
TEMP_DIR = "temp_test_data"


class TestCheckoutView(TestCase):
    """
    Tests that the Checkout view is behaving as expected
    """

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def setUp(self):
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
            display_name="Test Variant",
            name="test_variant",
            price=Decimal(1.99),
            sku="TEST-1",
        )

    def test_view_redirects_if_cart_empty(self):
        session = self.client.session
        session["cart"] = []
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("show_all_prints"),
        )

    def test_get_checkout_page(self):
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "1", "quantity": 1}]
        session.save()
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("orders/checkout.html")

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def test_can_create_order(self):
        self.client.login(username="testuser", password="123456")
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "1", "quantity": 1}]
        session.save()
        form_data = {
            "first_name": "Test",
            "last_name": "Test",
            "address_1": "Test",
            "address_2": "Test",
            "town": "Test",
            "county": "Test",
            "postcode": "Test",
            "country": "GB",
            "email_address": "test@test.com",
            "phone_number": "0123456789",
            "client_secret": "test_secret",
        }
        response = self.client.post(reverse("checkout"), form_data)
        order_exists = Order.objects.all().first()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(order_exists)


class TestOrderConfirmedView(TestCase):
    """
    Tests that the order_confirmed view is behaving as expected
    """

    def setUp(self):
        Order.objects.create(
            first_name="Test",
            last_name="Test",
            address_1="Test",
            address_2="Test",
            town="Test",
            county="Test",
            postcode="Test",
            country="GB",
            email_address="test@test.com",
            phone_number="0123456789",
        )

    def test_get_order_confirmed_page(self):
        order = Order.objects.get(pk=1)
        response = self.client.get(
            reverse("order_confirmed", args=(order.order_number,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("orders/order_confirmed.html")


class TestOrderDetailsView(TestCase):
    """
    Tests that the order_details view is behaving as expected
    """

    def setUp(self):
        Order.objects.create(
            first_name="Test",
            last_name="Test",
            address_1="Test",
            address_2="Test",
            town="Test",
            county="Test",
            postcode="Test",
            country="GB",
            email_address="test@test.com",
            phone_number="0123456789",
        )

    def test_get_order_confirmed_page(self):
        order = Order.objects.get(pk=1)
        response = self.client.get(
            reverse("order_details", args=(order.order_number,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("orders/order_details.html")


class TestCacheOrderDataView(TestCase):
    """
    Tests that the cache_order_data view is behaving as expected
    """

    def test_error_returned_to_get_request(self):
        response = self.client.get(reverse("cache_order_data"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(messages[0].tags, "error")


class TestCacheOrderDrawingView(TestCase):
    """
    Tests that the cache_order_drawing view is behaving as expected
    """

    def test_400_error_if_form_invalid(self):
        form_data = {}
        response = self.client.post(
            reverse("cache_order_drawing"),
            form_data,
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"},
        )
        self.assertEqual(response.status_code, 400)

    @override_settings(MEDIA_ROOT=TEMP_DIR)
    def test_can_create_order_drawing_cache(self):
        self.client.login(username="testuser", password="123456")
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)
            response = self.client.post(
                reverse("cache_order_drawing"),
                {
                    "stripe_pid": "test_pid",
                    "image": SimpleUploadedFile(
                        name="test_image.png",
                        content=temp_file.read(),
                    ),
                },
                **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"},
            )
        cache_exists = OrderDrawingCache.objects.filter(
            stripe_pid="test_pid"
        ).first()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cache_exists)
