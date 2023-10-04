from urllib.parse import parse_qs, urlparse

from django.http import HttpRequest, HttpResponse
from django.views.generic import View


class RegionsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        parsed_url = urlparse(request.get_full_path())
        regions: dict[str, list[str]] = parse_qs(parsed_url.query)

        if province_code := regions.get("province_code"):
            province_code = province_code[0]  # type: ignore
            print(province_code)

        return HttpResponse("something")
