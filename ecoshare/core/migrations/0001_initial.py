import core.models
import django.core.validators
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doacao',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('material_doado', models.CharField(max_length=50)),
                ('peso', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('data', models.DateField()),
                ('item_recebido', models.CharField(max_length=50)),
                ('validacao', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('cep', models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(regex='^\\d{5}-\\d{3}$')])),
                ('rua', models.CharField(max_length=100)),
                ('bairro', models.CharField(max_length=50)),
                ('numero', models.CharField(max_length=10)),
                ('cidade', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
                ('pais', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(regex='^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$')])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('senha', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(regex='^\\(\\d{2}\\) \\d{4,5}-\\d{4}$')])),
                ('data_nascimento', models.DateField()),
                ('endereco', djongo.models.fields.EmbeddedField(model_container=core.models.Endereco)),
                ('doacoes', djongo.models.fields.ArrayField(model_container=core.models.Doacao)),
            ],
        ),
    ]
