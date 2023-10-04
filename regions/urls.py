from django.urls import path

from . import views

urlpatterns = [
    path("districts/", views.DistrictsQueryView.as_view(), name="districts-query"),
    path("cities/", views.CitiesQueryView.as_view(), name="cities-query"),
    path("provinces/", views.ProvincesQueryView.as_view(), name="provinces-query"),
]
