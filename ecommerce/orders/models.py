from django.db import models
from django.utils import timezone
from products.models import Product


class Cart(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.product.title}"

    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    name = models.CharField(max_length=100, default="Guest")   # default added
    email = models.EmailField(default="guest@example.com")     # default added
    address = models.TextField(default="Unknown Address")      # default added
    phone = models.CharField(max_length=20, blank=True, null=True, default="N/A")  # safe default
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} by {self.name}"

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):   # new model
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # default added

    def __str__(self):
        return f"{self.quantity} × {self.product.title} (Order {self.order.id})"

    @property
    def total_price(self):
        return self.price * self.quantity
