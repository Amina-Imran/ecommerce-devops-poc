from django.test import TestCase
from django.urls import reverse

class OrdersViewsTest(TestCase):
    def test_cart_view(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)

    def test_checkout_view(self):
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
