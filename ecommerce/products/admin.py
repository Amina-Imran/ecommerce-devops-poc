
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "author", "publisher", "publication_date")
    search_fields = ("name", "author", "isbn")
    list_filter = ("publisher", "language")
