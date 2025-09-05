from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_url = request.POST.get("next") or request.GET.get("next")

        try:
            # ✅ First check if email exists
            user = User.objects.get(email=email)
            username = user.username

            # ✅ Then check password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                if next_url and next_url != "None":
                    return redirect(next_url)
                return redirect("home")
            else:
                messages.error(request, "Invalid password. Please try again.")  # ✅ password error
        except User.DoesNotExist:
            messages.error(request, "No account found with this email. Please register.")  # ✅ email error
            return redirect("register")

    return render(request, "accounts/login.html", {"next": request.GET.get("next")})


def register_view(request):
    next_url = request.POST.get("next") or request.GET.get("next")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered! Please login.")
            return redirect("login")
        else:
            user = User.objects.create_user(
                username=email, email=email, password=password1, first_name=name
            )
            login(request, user)
            messages.success(request, "Account created successfully!")
            # ✅ only redirect if next_url is valid
            if next_url and next_url != "None":
                return redirect(next_url)
            return redirect("home")

    return render(request, "accounts/register.html", {"next": request.GET.get("next")})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")
