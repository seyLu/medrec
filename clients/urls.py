from django.urls import path

from . import views

urlpatterns = [
    path("", views.ClientListView.as_view(), name="client-list"),
    path("create/", views.ClientCreateView.as_view(), name="client-create"),
    path(
        "<int:reference_number>/",
        views.ClientDetailView.as_view(),
        name="client-detail",
    ),
]
