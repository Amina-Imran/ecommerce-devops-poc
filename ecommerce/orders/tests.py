from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class OrdersViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

    def test_cart_view(self):
        response = self.client.get(reverse("orders:cart"))
        self.assertEqual(response.status_code, 200)

    def test_checkout_view(self):
        response = self.client.get(reverse("orders:checkout"))
        self.assertEqual(response.status_code, 200)
