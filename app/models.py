from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Consulta(models.Model):
    cod_consul = models.AutoField(primary_key=True)
    cod_pac = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='cod_pac')
    motivo = models.TextField()
    dt_prev_consulta = models.DateField()
    dt_consul = models.DateField(blank=True, null=True)
    valor = models.FloatField()
    status = models.BooleanField()

    class Meta:
        db_table = 'consulta'


class Especializacao(models.Model):
    cod_especializacao = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    valor_consulta = models.FloatField()

    class Meta:
        db_table = 'especializacao'


class Medico(models.Model):
    crm = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    data_nascimento = models.DateField(blank=True, null=True)
    cod_especializacao = models.ForeignKey(Especializacao, models.DO_NOTHING, db_column='cod_especializacao', blank=True, null=True)

    class Meta:
        db_table = 'medico'


class Paciente(models.Model):
    cod_pac = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=50)
    contato = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    dt_nasc = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'paciente'

