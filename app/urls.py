from django.urls import path
from app import views

urlpatterns = [
    path("", views.ListPacientes.as_view(), name="index"),
    path("list_pacientes/download", views.list_pacientes_pdf, name="download_pacientes"),
    path("buscar_paciente", views.buscar_paciente, name="buscar_paciente"),
    path("add_paciente", views.add_paciente, name="add_paciente"),
    path("edit_paciente/<int:id>", views.edit_paciente, name="edit_paciente"),
    path("delete_paciente/<int:id>", views.delete_paciente, name="delete_paciente")
]