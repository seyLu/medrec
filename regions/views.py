from typing import Any
from urllib.parse import parse_qs, urlparse

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from .models import City, District, Province


class DistrictsQueryView(View):
    def post(self, request: HttpRequest) -> JsonResponse | HttpResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response: Any = []

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = District.objects.get(code=code)

        elif city := regions.get("city"):
            city = city[0]  # type: ignore
            response = District.objects.filter(city=city)  # type: ignore[misc]

        if not request.htmx:
            if not response:
                return JsonResponse(list(response), safe=False)

            return JsonResponse(list(response.values()), safe=False)

        if not response:
            return HttpResponse()

        return render(
            request,
            "medrec/partials/regions-form/district-datalist.html",
            {"districts": list(response)},
        )


class CitiesQueryView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response: Any = []

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = City.objects.get(code=code)

        elif province := regions.get("province"):
            province = province[0]  # type: ignore
            response = City.objects.filter(province=province)  # type: ignore[misc]

        if not request.htmx:
            if not response:
                return JsonResponse(list(response), safe=False)

            return JsonResponse(list(response.values()), safe=False)

        if not response:
            return HttpResponse()

        return render(
            request,
            "medrec/partials/regions-form/city-datalist.html",
            {"cities": list(response)},
        )


class ProvincesQueryView(View):
    def post(self, request: HttpRequest) -> JsonResponse | HttpResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response: Any = []

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = Province.objects.get(code=code)

        else:
            response = Province.objects.all()

        if not request.htmx:
            if not response:
                return JsonResponse(list(response), safe=False)

            return JsonResponse(list(response.values()), safe=False)

        if not response:
            return HttpResponse()

        return render(
            request,
            "medrec/partials/regions-form/province-datalist.html",
            {"provinces": list(response)},
        )
