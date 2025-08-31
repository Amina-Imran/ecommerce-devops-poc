from django.http import HttpResponse

def product_list(request):
    return HttpResponse("📚 List of products will appear here.")
