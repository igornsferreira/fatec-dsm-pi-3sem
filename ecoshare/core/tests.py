from sqlite3 import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.shortcuts import resolve_url as r
from rest_framework import status
from rest_framework.tests import APIClient, APITestCase
from app.users.models import User

class IndexGetPostTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('index'), follow=True)
        self.resp_post = self.client.post(r('index'))

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp_post.status_code , 302)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')

class EnderecoVazioTest(TestCase):
    # def __init__(self, *args, **kwargs):
    #     self.address = kwargs.pop('address', 'http://127.0.0.1:8000')
    #     super().__init__(*args, **kwargs)

    def setUp(self):
        self.resp = self.client.get('/')

    def test_200_response(self):
        # Testa se a resposta HTTP é 200 (OK)
        self.assertEqual(200, self.resp.status_code)
        
    def test_templateUsed(self):
        # Testa se o template 'index.html' é usado
        self.assertTemplateUsed(self.resp, 'index.html')

from .models import EnderecoModel

class EnderecoModelTest(TestCase):
    def test_str_representation(self):
        endereco = EnderecoModel(cep="12345-678", rua="Rua Principal")
        self.assertEqual(str(endereco), "12345-678 - Rua Principal")

from .models import DoacaoModel

class DoacaoModelTest(TestCase):
    def test_validacao_default_value(self):
        doacao = DoacaoModel(material_doado="Roupas", peso=10)
        self.assertFalse(doacao.validacao)

from .models import UsuarioModel

class UsuarioModelTest(TestCase):
    def test_email_unique_constraint(self):
        # Testa se o campo de e-mail é único
        usuario1 = UsuarioModel(email="user@example.com")
        usuario2 = UsuarioModel(email="user@example.com")
        usuario1.save()
        with self.assertRaises(IntegrityError):
            usuario2.save()

class LoginUserTestCase(APITestCase):
    def setUp(self):
        self.novo_usuario = User.objects.create_user(
            email="teste@gmail.com",
            username="teste",
            password="123456"
        ) # Criar o usuário para testar a rota de login
        self.client = APIClient() # Vai fazer nossos testes de rota

    def test_sucess_login_200(self):
        url = reverse('login') 
        response = self.client.post(url,{"email":"teste@gmail.com", "password":"123456"})          
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_err_password_null_400(self):
        url = reverse('login')
        response = self.client.post(url,{"email":"teste@gmail.com","password":""})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

from .views import CadastroView

class CadastroViewTest(TestCase):
    def test_cadastro_usuario(self):
        # Simula uma requisição POST com dados de cadastro
        response = self.client.post(reverse('cadastro'), {
            'nome_completo': 'John Doe',
            'cpf': 12345678901,
            'email': 'john@example.com',
            'senha': 'mysecret123',
            'telefone': 19999999999,
            'data_nascimento': '07/10/2003',
        })
        
        # Verifica se o usuário foi criado
        self.assertEqual(User.objects.count(), 1)
        
        # Verifica se o redirecionamento ocorreu corretamente
        self.assertRedirects(response, reverse('homeCliente'))

from .views import LoginView

class LoginViewTest(TestCase):
    def test_login_usuario(self):
        user = User.objects.create_user(username='john@example.com', password='mysecret')
        response = self.client.post(reverse('login'), {
            'nome_completo': 'John Doe',
            'cpf': 12345678901,
            'email': 'john@example.com',
            'senha': 'mysecret123',
            'telefone': 19999999999,
            'data_nascimento': '07/10/2003',
        })
        
        # Verifica se o usuário está autenticado
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # Verifica se o redirecionamento ocorreu corretamente
        self.assertRedirects(response, reverse('homeCliente'))

from .views import LogoutView

class LoginViewTest(TestCase):
    def test_login_usuario(self):
        user = User.objects.create_user(username='john@example.com', password='mysecret')
        response = self.client.post(reverse('login'), {
            'email': 'john@example.com',
            'senha': 'mysecret',
        })
        
        # Verifica se o usuário está autenticado
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # Verifica se o redirecionamento ocorreu corretamente
        self.assertRedirects(response, reverse('homeCliente'))

