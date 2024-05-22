from django import forms
from django.core.exceptions import ValidationError
from .models import Endereco, Doacao, Usuario
from django.contrib.auth.forms import UserCreationForm

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'rua', 'bairro', 'numero', 'cidade', 'estado', 'pais']

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
        model = Usuario
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
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
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

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data['data_nascimento']
        return data_nascimento

    def clean_endereco(self):
        endereco = self.cleaned_data['endereco']
        return endereco
    
    def clean_doacoes(self):
        doacoes = self.cleaned_data['doacoes']
        return doacoes
