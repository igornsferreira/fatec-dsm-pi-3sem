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
from django.forms.widgets import DateInput

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    
class CadastroView(View):
    def get(self, request):
        return render(request, 'cadastro.html')
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if User.objects.filter(username=username).exists():
            return HttpResponse('Já existe um usuário com este nome.')

        user = User.objects.create_user(username=username, email=email, password=senha)
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

        usuario = Usuario(
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
        
        return HttpResponseRedirect(reverse('index.html'))
    
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse('Usuário ou senha inválidos.')
        
def logout_view(request):
    """Faz logout do usuário."""
    logout(request)
    return HttpResponseRedirect(reverse('index')
        
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
