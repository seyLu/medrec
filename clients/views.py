from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from records.models import Record

from .models import Client


class ClientCreateView(View):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        reference_number: int = int(request.POST["reference_number"])
        response: str = reverse(
            "client-detail",
            kwargs={"reference_number": reference_number},
        )
        query_string: str = urlencode({"close-modal": True})
        response += f"?{query_string}"

        return redirect(response)


class ClientDetailView(View):
    def get(self, request: HttpRequest, reference_number: int = 0) -> HttpResponse:
        client: Client = Client.objects.get(reference_number=reference_number)
        records: list[Record] = list(Record.objects.filter(client=client))

        context: dict[str, Any] = {"client": client, "records": records}

        parsed_url = urlparse(request.get_full_path())
        query: dict[str, list[str]] = parse_qs(parsed_url.query)

        if close_modal := query.get("close-modal"):
            context["close_modal"] = close_modal

        return render(
            request,
            "medrec/partials/client.html",
            context,
        )
