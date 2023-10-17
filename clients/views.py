from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from records.models import Record

from .models import Client


class ClientCreateView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        reference_number: int = int(request.POST["reference_number"])
        return HttpResponseRedirect(
            reverse("client-detail", kwargs={"reference_number": reference_number})
        )


class ClientDetailView(View):
    def get(self, request: HttpRequest, reference_number: int = 0) -> HttpResponse:
        client: Client = Client.objects.get(reference_number=reference_number)
        records: list[Record] = list(Record.objects.filter(client=client))

        return render(
            request,
            "medrec/partials/client.html",
            {"client": client, "records": records},
        )
