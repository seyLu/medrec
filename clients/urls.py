from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.ClientCreateView.as_view(), name="client-create"),
    path(
        "<int:reference_number>/",
        views.ClientDetailView.as_view(),
        name="client-detail",
    ),
]
