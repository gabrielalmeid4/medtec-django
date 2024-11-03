from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.shortcuts import render
from .models import Paciente
from .forms import PacienteForm
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.loader import render_to_string
from django.conf import settings
from reportlab.pdfgen import canvas
from io import BytesIO  
from datetime import datetime
import json


class ListPacientes(generic.ListView):
    model = Paciente
    template_name = 'app/list_pacientes.html' 

def index(request):
    return render(request, 'app/index.html')

def list_pacientes_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista_pacientes.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, "Lista de Pacientes")

    pacientes = Paciente.objects.all()
    y = 750

    for paciente in pacientes:
        linha = f"{paciente.cod_pac} - {paciente.nome} - {paciente.cpf} - {paciente.contato} - {paciente.endereco} - {paciente.dt_nasc}"
        p.drawString(100, y, linha)
        y -= 20 

        if y < 50:
            p.showPage() 
            y = 750  

    p.showPage()
    p.save()
    return response

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
    if nome_busca is None or nome_busca == '':
        pacientes = Paciente.objects.all()
        
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
    
@csrf_exempt
def edit_paciente(request, id):
    paciente = get_object_or_404(Paciente, cod_pac=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('index')
    if request.method == 'GET':
        form = PacienteForm(request.POST, instance=paciente)
        return render(request, 'app/edit_paciente.html', {'form': form, 'paciente': paciente})

@csrf_exempt
def delete_paciente(request, id):
    paciente = get_object_or_404(Paciente, cod_pac=id)
    
    if request.method == 'POST':
        paciente.delete()
        return redirect('index')
    if request.method == 'GET': 
        return render(request, 'app/delete_paciente.html', {'paciente': paciente})

@csrf_exempt
def dashboard(request):
    total_pacientes = Paciente.objects.count()
    pacientes_0_18 = 0
    pacientes_19_35 = 0
    pacientes_36_60 = 0
    pacientes_60_mais = 0

    for paciente in Paciente.objects.all():
        if (datetime.now().year - paciente.dt_nasc.year) <= 18:
            pacientes_0_18 += 1
        elif (datetime.now().year - paciente.dt_nasc.year) <= 35:
            pacientes_19_35 += 1
        elif (datetime.now().year - paciente.dt_nasc.year) <= 60:
            pacientes_36_60 += 1
        elif (datetime.now().year - paciente.dt_nasc.year > 60):
            pacientes_60_mais += 1

    # Pacientes por faixa etária
    faixa_etaria = {
        '0_18': pacientes_0_18,
        '19_35': pacientes_19_35,
        '36_60': pacientes_36_60,
        '60_plus': pacientes_60_mais,
    }

    faixa_etaria_json = json.dumps(faixa_etaria)

    context = {
        'total_pacientes': total_pacientes,
        'faixa_etaria': faixa_etaria_json,
    }
    return render(request, 'app/dashboard.html', context)