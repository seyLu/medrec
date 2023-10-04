from urllib.parse import parse_qs, urlparse

from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from .models import City, District


class DistrictsQueryView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response = None

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = District.objects.get(code=code)

        elif city_code := regions.get("city_code"):
            city_code = city_code[0]  # type: ignore
            response = District.objects.filter(city_code=city_code)  # type: ignore

        elif province_code := regions.get("province_code"):
            province_code = province_code[0]  # type: ignore
            response = District.objects.filter(province_code=province_code)[:10]  # type: ignore

        else:
            response = District.objects.all()[:10]  # type: ignore

        return HttpResponse(response)


class CitiesQueryView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        response = None

        if code := regions.get("code"):
            code = code[0]  # type: ignore
            response = City.objects.get(code=code)

        elif province_code := regions.get("province_code"):
            province_code = province_code[0]  # type: ignore
            response = City.objects.filter(province_code=province_code)  # type: ignore

        else:
            response = City.objects.all()[:10]  # type: ignore

        return HttpResponse(response)
