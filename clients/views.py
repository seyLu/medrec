from django.http import HttpRequest, HttpResponse
from django.views.generic import View


class ClientCreateView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse("hello world")


class ClientDetailView(View):
    def post(self, request: HttpRequest, reference_number: int = 0) -> HttpResponse:
        pass
