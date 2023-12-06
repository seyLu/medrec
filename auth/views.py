from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
from django_htmx.http import HttpResponseClientRedirect

from users.models import User


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(reverse("index"))

        return render(request, "auth/login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        email: str = request.POST["email"].strip()
        password: str = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is None:
            return render(
                request,
                "medrec/partials/alerts/auth-error.html",
                {"message": "Invalid Email/Password."},
            )

        login(request, user)
        return HttpResponseClientRedirect(reverse("index"))


class LogoutView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return HttpResponseClientRedirect(reverse("login"))


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "auth/register.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        email: str = request.POST["email"].strip()
        password: str = request.POST["password"]
        re_password: str = request.POST["re-password"]

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "medrec/partials/alerts/auth-error.html",
                {"message": "User already exists."},
            )

        if password != re_password:
            return render(
                request,
                "medrec/partials/alerts/auth-error.html",
                {"message": "Password and Confirm Password do not match."},
            )

        user = User.objects.create_user(email, password)
        login(request, user)
        return HttpResponseClientRedirect(reverse("index"))


class DemoView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user = authenticate(
            request, email="demo@email.com", password="demo"  # noqa: S106
        )
        login(request, user)
        return redirect(reverse("index"))
