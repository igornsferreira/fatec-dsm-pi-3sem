from django import forms
from django.core.exceptions import ValidationError
from .models import EnderecoModel, DoacaoModel, UsuarioModel
from django.contrib.auth.forms import UserCreationForm

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = EnderecoModel
        fields = ['cep', 'rua', 'bairro', 'numero', 'cidade', 'estado', 'pais']

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = DoacaoModel
        fields = ['_id', 'material_doado', 'peso', 'data', 'item_recebido', 'validacao']
        labels = {
            'material_doado': 'Material Doado',
            'peso': 'Peso',
            'data': 'Data',
            'item_recebido': 'Item Recebido',
        }

class UsuarioForm(UserCreationForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(
            format=('%d/%m/%Y'),
            attrs={
                'class': 'form-control',
                'placeholder': 'Data de Nascimento',
                'type': 'date'
            }
        )
    )

    class Meta:
        model = UsuarioModel
        fields = ['nome_completo', 'cpf', 'email', 'telefone', 'data_nascimento', 'endereco', 'doacoes']
        labels = {
            'nome_completo': 'Nome Completo',
            'cpf': 'CPF',
            'email': 'Email',
            'telefone': 'Telefone',
            'data_nascimento': 'Data de Nascimento',
            'endereco': 'Endereço',
            'doacoes': 'Doações',
        }

    def clean_nome_completo(self):
        nome_completo = self.cleaned_data['nome_completo']
        return nome_completo.upper().strip()

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = cpf.strip()
        if len(cpf) == 11:
            return cpf
        raise ValidationError('Insira um CPF válido no formato 999.999.999-99.')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if telefone:
            return telefone
        raise ValidationError('Insira um telefone válido no formato (99) 99999-9999 ou (99) 9999-9999.')

    def clean_endereco(self):
        endereco = self.cleaned_data['endereco']
        return endereco
    
    def clean_doacoes(self):
        doacoes = self.cleaned_data['doacoes']
        return doacoes
