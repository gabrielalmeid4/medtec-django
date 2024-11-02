from django.urls import path
from app import views

urlpatterns = [
    path("", views.ListPacientes.as_view(), name="index"),
    path("buscar_paciente", views.buscar_paciente, name="buscar_paciente"),
    path("add_paciente", views.add_paciente, name="add_paciente")
]