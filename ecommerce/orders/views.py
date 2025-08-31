from django.http import HttpResponse

def cart_view(request):
    return HttpResponse("🛒 This is the shopping cart page.")
