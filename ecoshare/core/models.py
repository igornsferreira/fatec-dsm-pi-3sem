from django.db import models
from djongo import models as djongo_models

import uuid


class Endereco(models.Model):
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=50)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    pais = models.CharField(max_length=50)

    class Meta:
        abstract = True

class Doacao(models.Model):
    id = models.CharField(max_length=24, unique=True, default=uuid.uuid4)
    material_doado = models.CharField(max_length=50)
    peso = models.IntegerField()
    data = models.DateField()
    item_recebido = models.CharField(max_length=50)
    validacao = models.BooleanField()

    class Meta:
        abstract = True

    class Meta:
        abstract = True

class Usuario(models.Model):
    nome_completo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()
    senha = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField()
    endereco = djongo_models.EmbeddedField(
       model_container=Endereco,
    )
    doacoes = djongo_models.ArrayField(
        model_container=Doacao,
    )
