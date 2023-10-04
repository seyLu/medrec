from django.urls import path

from . import views

urlpatterns = [
    path("", views.RegionsView.as_view(), name="regions"),
]
