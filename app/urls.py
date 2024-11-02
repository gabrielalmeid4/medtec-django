from django.urls import path
from app import views

urlpatterns = [
    path("", views.ListPacientes.as_view(), name="index"),
]