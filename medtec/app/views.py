from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.shortcuts import render
from .models import Paciente

class ListPacientes(generic.ListView):
    model = Paciente
    template_name = 'app/list_pacientes.html' 
