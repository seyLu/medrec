from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django_htmx.http import HttpResponseClientRedirect

from users.models import User


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "auth/login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        email: str = request.POST["email"].strip()
        password: str = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is None:
            return HttpResponse("Invalid Email or Password!")

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
            return HttpResponse("User already exists.")

        if password != re_password:
            return HttpResponse("Password and Confirm Password do not match.")

        user = authenticate(request, email=email, password=password)
        if user:
            return HttpResponse({"detail": "User already exists!"}, status=400)

        user = User.objects.create_user(email, password)
        login(request, user)
        return HttpResponseClientRedirect(reverse("index"))
