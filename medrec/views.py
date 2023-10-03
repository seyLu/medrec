from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, "medrec/index.html")
