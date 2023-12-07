from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("patient-list/", views.PatientListView.as_view(), name="patient-list"),
]
