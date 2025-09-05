from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    pages = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, default="English")
    publisher = models.CharField(max_length=100, blank=True, null=True)
    publication_date = models.CharField(max_length=20, blank=True, null=True)
    format = models.CharField(max_length=50, default="Paperback")

    def __str__(self):
        return self.name
