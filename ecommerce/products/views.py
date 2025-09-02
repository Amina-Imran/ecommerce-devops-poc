from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    books = Product.objects.all()
    return render(request, "products/product_list.html", {"books": books})

def product_detail(request, pk):
    book = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"book": book})
