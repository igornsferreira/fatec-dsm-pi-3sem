from django.views import View
from django.shortcuts import render, redirect
from .models import UsuarioModel  
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
        if User.objects.filter(username=email).exists():
            return HttpResponse('Já existe um usuário com este email.')

        # Crie o usuário
        user = User.objects.create_user(username=email, email=email)
        user.set_password(senha)
        user.save()

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

        usuario = UsuarioModel(
            nome_completo=user,
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
        
        user = authenticate(username=email, password=senha)

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
