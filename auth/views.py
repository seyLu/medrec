from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django_htmx.http import HttpResponseClientRedirect


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "auth/login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        email: str = request.POST["email"].strip()
        password: str = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is None:
            return HttpResponse({"detail": "Invalid Email or Password!"}, status=400)

        login(request, user)
        return HttpResponseClientRedirect(reverse("index"))


class LogoutView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return HttpResponse({"message": "Successfully logged out."})


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "auth/register.html")
