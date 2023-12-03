from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from users.models import User


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "medrec/index.html")


class TestView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        user: User = User.objects.get(email=request.user)  # type: ignore[assignment]
        email: str = user.email
        avatar: str = ""
        display_name: str = ""

        avatar = email[0].upper()
        display_name = email.split("@")[0].title()

        context = {
            "email": email,
            "avatar": avatar,
            "display_name": display_name,
        }

        return render(request, "medrec/test_index.html", context)
