from django.views import View
from django.shortcuts import render, redirect
from .models import Usuario, Endereco, Doacao
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
