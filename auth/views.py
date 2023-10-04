from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django_htmx.http import HttpResponseClientRedirect

from users.models import User


def authError(message: str) -> str:
    return f"""
                <div class="alert alert-warning">
                    <svg xmlns="http://www.w3.org/2000/svg"
                        class="stroke-current shrink-0 h-6 w-6"
                        fill="none"
                        viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <span>{message}</span>
                </div>
            """


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "auth/login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        email: str = request.POST["email"].strip()
        password: str = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is None:
            return HttpResponse(authError("Invalid Email/Password."))

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
            return HttpResponse(authError("User already exists."))

        if password != re_password:
            return HttpResponse(
                authError("Password and Confirm Password do not match.")
            )

        user = User.objects.create_user(email, password)
        login(request, user)
        return HttpResponseClientRedirect(reverse("index"))
