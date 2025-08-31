from django.test import TestCase
from .models import Product

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
