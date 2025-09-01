from django.shortcuts import render

def cart_view(request):
    return render(request, "orders/cart.html")

def checkout_view(request):
    return render(request, "orders/checkout.html")
