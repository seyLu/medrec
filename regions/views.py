from typing import Any
from urllib.parse import parse_qs, urlparse

from django.http import HttpRequest, JsonResponse
from django.views.generic import View

from .models import City, District, Province


class DistrictsQueryView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response: Any = []

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = District.objects.get(code=code)

        elif city := regions.get("city"):
            city = city[0]  # type: ignore
            response = District.objects.filter(city=city)  # type: ignore[misc]

        if not response:
            return JsonResponse(list(response), safe=False)

        return JsonResponse(list(response.values()), safe=False)


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

        if not response:
            return JsonResponse(list(response), safe=False)

        return JsonResponse(list(response.values()), safe=False)


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

        if not response:
            return JsonResponse(list(response), safe=False)

        return JsonResponse(list(response.values()), safe=False)
