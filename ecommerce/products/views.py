from django.shortcuts import render
from django.http import HttpResponse

def product_list(request):
    return render(request, "products/product_list.html")

def product_detail(request, product_id):
    # For now just pass product_id, later we'll fetch from DB
    return render(request, "products/product_detail.html", {"product_id": product_id})
