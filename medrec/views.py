from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from users.models import User

PAGE_TITLE_MAP: dict[str, str] = {
    "overview": "Overview",
    "patient_list": "Patient List",
}


def get_page_info(request: HttpRequest, page: str) -> dict[str, str]:
    user: User = User.objects.get(email=request.user)  # type: ignore[assignment]
    email: str = user.email
    avatar: str = f"{email[0].upper()}{email[1].upper()}"
    display_name: str = email.split("@")[0].title()

    return {
        "email": email,
        "avatar": avatar,
        "display_name": display_name,
        "page": page,
        "page_title": PAGE_TITLE_MAP[page],
    }


class IndexView(LoginRequiredMixin, View):
    page: str = "overview"

    def get(self, request: HttpRequest) -> HttpResponse:
        context: dict[str, Any] = {
            **get_page_info(request, IndexView.page),
        }

        return render(request, "medrec/index.html", context)


class PatientListView(LoginRequiredMixin, View):
    page: str = "patient_list"

    def get(self, request: HttpRequest) -> HttpResponse:
        context: dict[str, Any] = {
            **get_page_info(request, PatientListView.page),
        }

        return render(request, "medrec/partials/page/patient-list.html", context)
