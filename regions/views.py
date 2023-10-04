from typing import Any
from urllib.parse import parse_qs, urlparse

from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from .models import District


class DistrictsQueryView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response: list[dict[str, Any]] = []

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = District.objects.get(code=code)

        elif city_code := regions.get("city_code"):
            city_code = city_code[0]  # type: ignore
            response = District.objects.filter(city_code=city_code)

        elif province_code := regions.get("province_code"):
            province_code = province_code[0]  # type: ignore
            response = District.objects.filter(province_code=province_code)[:10]

        else:
            response = District.objects.all()[:10]

        return HttpResponse(response)
