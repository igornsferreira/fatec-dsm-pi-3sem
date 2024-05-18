from django.views import View
from django.shortcuts import render, redirect
from .models import Usuario
from bson import ObjectId

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    
class CadastroView(View):
    def get(self, request):
        return render(request, 'cadastro.html')
    
    def post(self, request):
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
            nome_completo=request.POST['nome'],
            cpf=request.POST['cpf'],
            email=request.POST['email'],
            senha=request.POST['senha'],
            telefone=request.POST['telefone'],
            data_nascimento=request.POST['data_nascimento'],
            endereco=endereco_dict,
            doacoes=[]
        )
        usuario.save()

        return redirect('index')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

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
