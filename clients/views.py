from typing import Any, Iterator
from urllib.parse import parse_qs, urlencode, urlparse

from django.core.paginator import Page, Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from records.models import Record

from .models import Client


class ClientListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        client_list: Client = Client.objects.all().order_by("-updated_datetime")  # type: ignore[assignment]
        paginator: Paginator = Paginator(client_list, 7)  # type: ignore

        page_number: str = request.GET.get("page", "1")
        page_obj: Page[Client] = paginator.get_page(page_number)
        page_range: Iterator[str | int] = page_obj.paginator.get_elided_page_range(
            int(page_number), on_each_side=2, on_ends=1
        )
        clients: list[Client] = page_obj.object_list  # type: ignore[assignment]

        context: dict[str, Any] = {
            "num_clients": len(client_list),  # type: ignore[arg-type]
            "clients": clients,
            "page_obj": page_obj,
            "page_range": page_range,
        }

        return render(request, "medrec/partials/client-list.html", context)


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
