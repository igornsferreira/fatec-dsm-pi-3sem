from django.contrib import messages
from django.views import View
from django.shortcuts import render
from .models import UsuarioModel, DoacaoModel
from bson import ObjectId
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404

class IndexView(View):
    template_name = 'index.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
class CadastroView(View):
    template_name = 'cadastro.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        # Obtenha os dados do formulário
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifique se já existe um usuário com o mesmo e-mail
        if User.objects.filter(username=email).exists():
           return HttpResponse('Já existe um usuário com este email.')

        # Cria o usuário
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
            user=user,
            nome_completo=request.POST['nome_completo'],
            cpf=request.POST['cpf'],
            email=request.POST['email'],
            senha=request.POST['senha'],
            telefone=request.POST['telefone'],
            data_nascimento=request.POST['data_nascimento'],
            endereco=endereco_dict,
            doacoes=[]
        )
        usuario.save()
        
        return HttpResponseRedirect(reverse('homeCliente'))
    
class LoginView(View):
    template_name = 'login.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        user = authenticate(username=email, password=senha)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homeCliente'))
        else:
            # Caso o usuário insira informações erradas
            messages.info(request, 'E-mail ou senha incorretos.')
            return render(request, self.template_name)

def LogoutView(request):
    """Faz logout do usuário."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))
        
class HomeClienteView(View):
    template_name = 'homeCliente.html'

    def get(self, request):
        return render(request, self.template_name)
    
class RelatorioClienteView(View):
    template_name = 'relatorioCliente.html'

    def get(self, request):
        usuario = get_object_or_404(UsuarioModel, user=request.user)
        doacoes = usuario.doacoes

        for doacao in doacoes:
            doacao['id'] = doacao.pop('_id')

        context = {
            'doacoes': doacoes,
        }
        return render(request, self.template_name, context)

class DoacoesClienteView(LoginRequiredMixin, View):
    template_name = 'doacoesCliente.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Obtendo os dados do formulário
        material_doado = request.POST.get('material')
        peso = request.POST.get('peso')
        data = request.POST.get('data')
        item_recebido = request.POST.get('brinde')

        # Criando uma nova instância de DoacaoModel
        doacao = DoacaoModel(
            _id=ObjectId(),
            material_doado=material_doado,
            peso=peso,
            data=data,
            item_recebido=item_recebido,
            validacao=False  # Sempre inicializado como falso
        )

        # Salvando a nova doação
        doacao.save()

        # Converte a instância de doação para um dicionário
        doacao_dict = {
            "_id": doacao._id,
            "material_doado": doacao.material_doado,
            "peso": doacao.peso,
            "data": doacao.data,
            "item_recebido": doacao.item_recebido,
            "validacao": doacao.validacao
        }

        try:
            # Obtendo o usuário
            usuario = UsuarioModel.objects.get(user=request.user)
            
            # Usando o método update para adicionar a doação
            UsuarioModel.objects.filter(user=request.user).update(
                doacoes=[*usuario.doacoes, doacao_dict]
            )

        except UsuarioModel.DoesNotExist:
            # Se o usuário não existir, criar um novo
            usuario = UsuarioModel(
                user=request.user,
                doacoes=[doacao_dict]
            )
            usuario.save()

        # Redirecionando de volta para a página de doações
        return HttpResponseRedirect(reverse('doacoesCliente'))
        
class BrindesClienteView(View):
    template_name = 'brindesCliente.html'

    def get(self, request):
        return render(request, self.template_name)

class PerfilClienteView(LoginRequiredMixin, TemplateView):
    template_name = 'perfilCliente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = get_object_or_404(UsuarioModel, user=self.request.user)
        context['usuario'] = usuario
        return context
    
class EditPerfilClienteView(LoginRequiredMixin, TemplateView):
    template_name = 'editPerfilCliente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = get_object_or_404(UsuarioModel, user=self.request.user)
        context['usuario'] = usuario
        return context