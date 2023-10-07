from typing import Any
from urllib.parse import parse_qs, urlparse

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from .models import City, District, Province


class DistrictsQueryView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response: Any = []

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = District.objects.get(code=code)

        elif city_code := regions.get("city_code"):
            city_code = city_code[0]  # type: ignore
            response = District.objects.filter(city_code=city_code)  # type: ignore[misc]

        return HttpResponse(response)


class CitiesQueryView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response: Any = []

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = City.objects.get(code=code)

        elif province_code := regions.get("province_code"):
            province_code = province_code[0]  # type: ignore
            response = City.objects.filter(province_code=province_code)  # type: ignore[misc]

        return HttpResponse(response)


class ProvincesQueryView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response: Any = []

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = Province.objects.get(code=code)

        else:
            response = Province.objects.all()

        return JsonResponse(list(response.values()), safe=False)
