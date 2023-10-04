from django.urls import path

from . import views

urlpatterns = [
    path("districts/", views.DistrictsQueryView.as_view(), name="districts-query"),
]
