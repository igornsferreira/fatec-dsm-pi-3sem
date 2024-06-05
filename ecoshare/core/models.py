from django.db import models
from django.core import validators
from djongo import models as djongo_models
from django.contrib.auth.models import User


class EnderecoModel(models.Model):
    _id = djongo_models.ObjectIdField()
    cep = models.CharField(
        max_length=9, validators=[validators.RegexValidator(regex="^\\d{5}-\\d{3}$")]
    )
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=50)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)

    def __str__(self):
        """Devolve uma representação em string do modelo."""
        return self._id

    class Meta:
        verbose_name = "Endereco"
        verbose_name_plural = "Enderecos"


class DoacaoModel(models.Model):
    _id = djongo_models.ObjectIdField()
    material_doado = models.CharField(max_length=50)
    peso = models.IntegerField(validators=[validators.MinValueValidator(1)])
    data = models.DateTimeField(auto_now_add=True)
    item_recebido = models.CharField(max_length=50)
    validacao = models.BooleanField(default=False)

    def __str__(self):
        """Devolve uma representação em string do modelo."""
        return self.material_doado

    class Meta:
        verbose_name = "Doacao"
        verbose_name_plural = "Doacoes"  # Para quando forem realizadas diversas doações


class UsuarioModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nome_completo = models.CharField(max_length=100)
    cpf = models.CharField(
        max_length=14,
        validators=[
            validators.RegexValidator(regex="^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$")
        ],
    )
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    telefone = models.CharField(
        max_length=15,
        validators=[validators.RegexValidator(regex="^\\(\\d{2}\\) \\d{4,5}-\\d{4}$")],
    )
    data_nascimento = models.DateField()
    endereco = djongo_models.EmbeddedField(model_container=EnderecoModel)
    doacoes = djongo_models.ArrayField(model_container=DoacaoModel)

    def __str__(self):
        """Devolve uma representação em string do modelo."""
        return self.nome_completo

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "ecoshare"  # Define o nome da coleção no MongoDB
