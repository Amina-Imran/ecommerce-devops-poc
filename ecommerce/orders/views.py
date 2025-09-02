from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal  # ✅ use Decimal for money
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem


# Helper: Get or create session cart
def _get_cart(request):
    cart_id = request.session.get("cart_id")
    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()
        if cart:
            return cart
    cart = Cart.objects.create()
    request.session["cart_id"] = cart.id
    return cart


# ✅ User must be logged in to add to cart
@login_required(login_url="/accounts/login/")
def add_to_cart(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("orders:cart")


# ✅ User must be logged in to view cart
@login_required(login_url="/accounts/login/")
def cart_view(request):
    cart = _get_cart(request)
    cart_items = cart.items.all()

    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    cart_tax = (cart_total * Decimal("0.08")).quantize(Decimal("0.01"))  # ✅ fix
    cart_grand_total = cart_total + cart_tax

    return render(request, "orders/cart.html", {
        "cart_items": cart_items,
        "cart_total": cart_total,
        "cart_tax": cart_tax,
        "cart_grand_total": cart_grand_total,
    })


# ✅ User must be logged in to checkout
@login_required(login_url="/accounts/login/")
def checkout(request):
    cart = _get_cart(request)
    cart_items = cart.items.all()

    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    cart_tax = (cart_total * Decimal("0.08")).quantize(Decimal("0.01"))  # ✅ fix
    cart_grand_total = cart_total + cart_tax

    if request.method == "POST":
        order = Order.objects.create(
            name=request.POST.get("name", request.user.first_name or "Guest"),
            email=request.POST.get("email", request.user.email),
            address=request.POST.get("address", "Unknown Address"),
            phone=request.POST.get("phone", "N/A"),
        )

        # Save order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # clear cart
        cart.items.all().delete()
        request.session.pop("cart_id", None)

        return render(request, "orders/checkout_success.html", {"order": order})

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "cart_total": cart_total,
        "cart_tax": cart_tax,
        "cart_grand_total": cart_grand_total,
    })


# ✅ Update quantity in cart
@login_required(login_url="/accounts/login/")
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()  # if 0 → remove item
        except ValueError:
            pass
    return redirect("orders:cart")


# ✅ Remove item from cart
@login_required(login_url="/accounts/login/")
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("orders:cart")
