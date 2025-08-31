from django.http import HttpResponse

def login_view(request):
    return HttpResponse("🔑 This is the login page.")
