from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "medrec/index.html")


class TestView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "medrec/test_index.html")
