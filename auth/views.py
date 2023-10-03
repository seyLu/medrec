from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "auth/login.html")


class LogoutView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return HttpResponse({"message": "Successfully logged out."})


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "auth/register.html")
