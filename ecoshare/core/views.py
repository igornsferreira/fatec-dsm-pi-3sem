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

import secrets
import string

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
        cpf = request.POST.get('cpf')

        # Verifique se já existe um usuário com o mesmo e-mail
        if User.objects.filter(username=email).exists():
           messages.error(request, 'Já existe um usuário com este email.')
        #    return HttpResponse('Já existe um usuário com este email.')

        # Verifique se já existe um usuário com o mesmo CPF
        if UsuarioModel.objects.filter(cpf=cpf).exists():
           messages.error(request, 'Já existe um usuário com este CPF.')
        #    return HttpResponse('Já existe um usuário com este CPF.')

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
        nome = get_object_or_404(UsuarioModel, user=request.user)
        return render(request, self.template_name, {'nome': nome})
    
    def get(self, request):
        usuario = get_object_or_404(UsuarioModel, user=request.user)
        quantidade_doacoes = len(usuario.doacoes)
        
        # filtra as doacoes validadas
        doacoes_validadas = [doacao for doacao in usuario.doacoes if doacao.get('validacao') is True]
        qtd_doacoes_validadas = len(doacoes_validadas)

        return render(request, self.template_name, {
            'nome': usuario,
            'quantidade_doacoes': quantidade_doacoes,
            'qtd_doacoes_validadas': qtd_doacoes_validadas
        })
    


def generate_random_password():
    # Define os caracteres permitidos (letras minúsculas, dígitos e caracteres especiais)
    allowed_chars = string.ascii_letters + string.digits + "!@#$%&"

    # Gera uma senha aleatória com 6 caracteres
    random_password = ''.join(secrets.choice(allowed_chars) for _ in range(6))

    return random_password

class RelatorioClienteView(View):
    template_name = 'relatorioCliente.html'

    def get(self, request):
        usuario = get_object_or_404(UsuarioModel, user=request.user)
        doacoes = usuario.doacoes

        filtro_status = request.GET.get('status')
        if filtro_status == 'retirado':
            doacoes = [doacao for doacao in doacoes if doacao.get('validacao')]
        elif filtro_status == 'pendente':
            doacoes = [doacao for doacao in doacoes if not doacao.get('validacao')]

        for doacao in doacoes:
            doacao['id'] = doacao.pop('_id')

        senha_aleatoria = generate_random_password()

        context = {
            'doacoes': doacoes,
            'senha_aleatoria': senha_aleatoria,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        action = request.POST.get('action')
        doacao_id = request.POST.get('doacao_id')

        if action == 'delete' and doacao_id:
            try:
                usuario = UsuarioModel.objects.get(user=request.user)

                # Filtro de doações para remover a doação com o id especificado
                doacoes_atualizadas = [doacao for doacao in usuario.doacoes if str(doacao['_id']) != doacao_id]

                UsuarioModel.objects.filter(user=request.user).update(doacoes=doacoes_atualizadas)

            except UsuarioModel.DoesNotExist:
                messages.error(request, "Usuário não encontrado.")
        return HttpResponseRedirect(reverse('relatorioCliente'))

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
        return HttpResponseRedirect(reverse('relatorioCliente'))
        
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

    def post(self, request):
        usuario = get_object_or_404(UsuarioModel, user=request.user)
        
        # Obtenha os dados do formulário
        nome_completo = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        data_nascimento = request.POST.get('data_nascimento')
        senha = request.POST.get('senha')

        # Pegue o _id do endereço existente
        endereco_id = usuario.endereco['_id']
        
        endereco_dict = {
            "_id": endereco_id,  # Certifique-se de que o _id está incluído
            "cep": request.POST.get('cep'),
            "rua": request.POST.get('rua'),
            "bairro": request.POST.get('bairro'),
            "numero": request.POST.get('numero'),
            "cidade": request.POST.get('cidade'),
            "estado": request.POST.get('estado'),
            "pais": request.POST.get('pais')
        }

        # Atualizar os campos do usuário
        UsuarioModel.objects.filter(user=request.user).update(
            nome_completo=nome_completo,
            cpf=cpf,
            email=email,
            telefone=telefone,
            data_nascimento=data_nascimento,
            senha=senha,
            endereco=endereco_dict
        )

        return HttpResponseRedirect(reverse('perfilCliente'))
