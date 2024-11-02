from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.shortcuts import render
from .models import Paciente
from .forms import PacienteForm
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect, csrf_exempt

class ListPacientes(generic.ListView):
    model = Paciente
    template_name = 'app/list_pacientes.html' 

def buscar_paciente(request):
    nome_busca = request.GET.get('nome_busca', '').strip()
    pacientes = Paciente.objects.none()

    if nome_busca:
        if nome_busca.isdigit():
            pacientes = Paciente.objects.filter(
                Q(cod_pac = int(nome_busca))
            )
        else:
            pacientes = Paciente.objects.filter(
                Q(nome__icontains = nome_busca) |
                Q(cpf__icontains = nome_busca)
            )
    
    return render(request, 'app/list_pacientes.html', { 'paciente_list': pacientes})

@csrf_exempt
def add_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    if request.method == 'GET':
        form = PacienteForm()
        return render(request, 'app/add_paciente.html', {'form': form})
        

