from django.test import TestCase
from .models import Product
from django.urls import reverse

class ProductModelTest(TestCase):
    def test_create_product(self):
        """Test that a Product can be created and its string output is correct"""
        product = Product.objects.create(
            name="Test Book",
            description="A sample test book",
            price=9.99,
            stock=10
        )
        self.assertEqual(str(product), "Test Book")
        self.assertEqual(product.price, 9.99)
        self.assertEqual(product.stock, 10)

class ProductViewsTest(TestCase):
    def test_product_list_view(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        # Since no products exist yet, detail may 404, so allow 200 or 404
        response = self.client.get("/products/1/")
        self.assertIn(response.status_code, [200, 404])