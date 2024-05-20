from django import forms
from django.core.exceptions import ValidationError
from .models import Endereco, Doacao, Usuario

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'rua', 'bairro', 'numero', 'cidade', 'estado', 'pais']

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['material_doado', 'peso', 'data', 'item_recebido', 'validacao']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome_completo', 'cpf', 'email', 'senha', 'telefone', 'data_nascimento', 'endereco', 'doacoes']

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
    
    def clean_senha(self):
        senha = self.cleaned_data['senha']
        return senha

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