from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import Drawing
from prints.models import ProductVariant


class TestViewCartView(TestCase):
    """
    Tests that the view_cart view is behaving as expected.
    """

    def test_get_view_cart_page(self):
        response = self.client.get(reverse("view_cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")


class TestAddToCartView(TestCase):
    """
    Tests that the add_to_cart view is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )
        ProductVariant.objects.create(
            product=None,
            display_name="Test Variant",
            name="test_variant",
            price=Decimal(1.99),
        )

    def test_can_add_new_item_to_cart(self):
        variant = ProductVariant.objects.get(pk=1)
        response = self.client.post(
            reverse("add_to_cart"),
            {
                "variant": variant.id,
                "quantity": 1,
                "drawing": 0,
                "redirect_url": reverse("view_cart"),
            },
        )
        self.assertEqual(
            self.client.session.get("cart"),
            [{"variant_id": "1", "drawing": "0", "quantity": 1}],
        )

    def test_can_increase_item_quantity_in_cart(self):
        # add item to session cart with quantity 1
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "0", "quantity": 1}]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        response = self.client.post(
            reverse("add_to_cart"),
            {
                "variant": variant.id,
                "quantity": 1,
                "drawing": 0,
                "redirect_url": reverse("view_cart"),
            },
        )
        self.assertEqual(
            self.client.session.get("cart"),
            [{"variant_id": "1", "drawing": "0", "quantity": 2}],
        )


class TestUpdateCartItemView(TestCase):
    """
    Tests that the update_cart_item view is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )
        ProductVariant.objects.create(
            product=None,
            display_name="Test Variant",
            name="test_variant",
            price=Decimal(1.99),
        )

    def test_can_update_item_quantity_in_cart(self):
        # add item to session cart with quantity 10
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "0", "quantity": 10}]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        # update quantity to 5
        response = self.client.post(
            reverse("update_cart_item"),
            {
                "variant_id": variant.id,
                "quantity": 5,
                "drawing": 0,
            },
        )
        self.assertEqual(
            self.client.session.get("cart"),
            [{"variant_id": "1", "drawing": "0", "quantity": 5}],
        )

    def test_can_remove_item_from_cart(self):
        # add item to session cart with quantity 10
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "0", "quantity": 10}]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        # update quantity to 0
        response = self.client.post(
            reverse("update_cart_item"),
            {
                "variant_id": variant.id,
                "quantity": 0,
                "drawing": 0,
            },
        )
        self.assertEqual(self.client.session.get("cart"), [])


class TestRemoveCartItemView(TestCase):
    """
    Tests that the remove_cart_item view is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )
        ProductVariant.objects.create(
            product=None,
            display_name="Test Variant",
            name="test_variant",
            price=Decimal(1.99),
        )

    def test_can_remove_item_from_cart(self):
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "0", "quantity": 5}]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        response = self.client.post(
            reverse("remove_cart_item"),
            {
                "variant_id": variant.id,
                "drawing": 0,
            },
        )
        self.assertEqual(self.client.session.get("cart"), [])

    def test_only_selected_item_removed(self):
        session = self.client.session
        session["cart"] = [
            {"variant_id": "1", "drawing": "0", "quantity": 5},
            {"variant_id": "2", "drawing": "0", "quantity": 5},
            {"variant_id": "1", "drawing": "1", "quantity": 5},
            {"variant_id": "2", "drawing": "1", "quantity": 5},
        ]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        response = self.client.post(
            reverse("remove_cart_item"),
            {
                "variant_id": variant.id,
                "drawing": 0,
            },
        )
        self.assertEqual(
            self.client.session.get("cart"),
            [
                {"variant_id": "2", "drawing": "0", "quantity": 5},
                {"variant_id": "1", "drawing": "1", "quantity": 5},
                {"variant_id": "2", "drawing": "1", "quantity": 5},
            ],
        )
