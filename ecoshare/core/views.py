from django.views import View
from django.shortcuts import render, redirect
from .models import Usuario
from bson import ObjectId
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.urls import reverse

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    
class CadastroView(View):
    def get(self, request):
        return render(request, 'cadastro.html')
    
    def post(self, request):
        # Obtenha os dados do formulário
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifique se já existe um usuário com o mesmo nome
        if User.objects.filter(username=nome_completo).exists():
            return HttpResponse('Já existe um usuário com este nome.')

        # Crie o usuário
        user = User.objects.create_user(username=nome_completo, email=email, password=senha)
        user.save()
        
        # Divida o nome completo em partes (primeiro nome e sobrenome)
        # partes_nome = nome_completo.split()
        # primeiro_nome = partes_nome[0]
        # sobrenome = partes_nome[-1]
        
        endereco_dict = {
            "_id": str(ObjectId()),
            "cep": request.POST['cep'],
            "rua": request.POST['rua'],
            "bairro": request.POST['bairro'],
            "numero": request.POST['numero'],
            "cidade": request.POST['cidade'],
            "estado": request.POST['estado'],
            "pais": request.POST['pais']
        }

        usuario = Usuario(
            nome_completo=user,
            # primeiro_nome=primeiro_nome,
            # sobrenome=sobrenome,
            cpf=request.POST['cpf'],
            email=request.POST['email'],
            senha=request.POST['senha'],
            telefone=request.POST['telefone'],
            data_nascimento=request.POST['data_nascimento'],
            endereco=endereco_dict,
            doacoes=[]
        )
        usuario.save()
        
        return HttpResponseRedirect(reverse('index'))
    
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(email=email, password=senha)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homeCliente'))
        else:
            return HttpResponse('Usuário ou senha inválidos.')

def LogoutView(request):
    """Faz logout do usuário."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))
        
class HomeClienteView(View):
    def get(self, request):
        return render(request, 'homeCliente.html')

class RelatorioClienteView(View):
    def get(self, request):
        return render(request, 'relatorioCliente.html')

class DoacoesClienteView(View):
    def get(self, request):
        return render(request, 'doacoesCliente.html')

class BrindesClienteView(View):
    def get(self, request):
        return render(request, 'brindesCliente.html')

class PerfilClienteView(View):
    def get(self, request):
        return render(request, 'perfilCliente.html')
    