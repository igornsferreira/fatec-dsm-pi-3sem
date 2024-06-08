from django.test import TestCase
from django.urls import reverse
from django.shortcuts import resolve_url as r
from rest_framework import status
from rest_framework.tests import APIClient, APITestCase
from sqlite3 import IntegrityError
from app.users.models import User
from .models import EnderecoModel, DoacaoModel, UsuarioModel
from .views import CadastroView, LoginView, LogoutView


class IndexGetPostTest(TestCase):
    """
    Testa a view index para métodos GET e POST.
    """

    def setUp(self):
        # Faz uma solicitação GET e POST para a view index
        self.resp = self.client.get(r('index'), follow=True)
        self.resp_post = self.client.post(r('index'))

    def test_status_code(self):
        # Verifica os códigos de status das respostas
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(self.resp_post.status_code, 302)

    def test_template_used(self):
        # Verifica se o template 'index.html' é usado
        self.assertTemplateUsed(self.resp, 'index.html')


class EnderecoVazioTest(TestCase):
    """
    Testa a view raiz ('/') para endereço vazio.
    """

    def setUp(self):
        # Faz uma solicitação GET para a view raiz
        self.resp = self.client.get('/')

    def test_200_response(self):
        # Verifica se a resposta HTTP é 200 (OK)
        self.assertEqual(200, self.resp.status_code)

    def test_templateUsed(self):
        # Verifica se o template 'index.html' é usado
        self.assertTemplateUsed(self.resp, 'index.html')


class EnderecoModelTest(TestCase):
    """
    Testa o modelo EnderecoModel.
    """

    def test_str_representation(self):
        # Verifica a representação em string do objeto EnderecoModel
        endereco = EnderecoModel(cep="12345-678", rua="Rua Principal")
        self.assertEqual(str(endereco), "12345-678 - Rua Principal")


class DoacaoModelTest(TestCase):
    """
    Testa o modelo DoacaoModel.
    """

    def test_validacao_default_value(self):
        # Verifica o valor padrão do campo 'validacao' em DoacaoModel
        doacao = DoacaoModel(material_doado="Roupas", peso=10)
        self.assertFalse(doacao.validacao)


class UsuarioModelTest(TestCase):
    """
    Testa o modelo UsuarioModel.
    """

    def test_email_unique_constraint(self):
        # Testa se o campo de e-mail é único
        usuario1 = UsuarioModel(email="user@example.com")
        usuario2 = UsuarioModel(email="user@example.com")
        usuario1.save()
        with self.assertRaises(IntegrityError):
            usuario2.save()


class LoginUserTestCase(APITestCase):
    """
    Testa a autenticação do usuário.
    """

    def setUp(self):
        # Cria um novo usuário para testar a autenticação
        self.novo_usuario = User.objects.create_user(
            email="teste@gmail.com",
            username="teste",
            password="123456"
        )
        self.client = APIClient()  # Cliente para fazer solicitações

    def test_sucess_login_200(self):
        # Testa o login com sucesso (código 200)
        url = reverse('login')
        response = self.client.post(url, {"email": "teste@gmail.com", "password": "123456"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_err_password_null_400(self):
        # Testa o login com senha em branco (erro 400)
        url = reverse('login')
        response = self.client.post(url, {"email": "teste@gmail.com", "password": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CadastroViewTest(TestCase):
    """
    Testa a view de cadastro de usuário.
    """

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


class LoginViewTest(TestCase):
    """
    Testa a view de login.
    """

    def test_login_usuario(self):
        # Cria um usuário para testar o login
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


class LogoutViewTest(TestCase):
    """
    Testa a view de logout.
    """

    def test_logout_usuario(self):
        # Cria um usuário e autentica ele
        user = User.objects.create_user(username='john@example.com', password='mysecret')
        self.client.force_login(user)

        # Realiza o logout
        response = self.client.post(reverse('logout'))

        # Verifica se o usuário não está autenticado após o logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # Verifica se o redirecionamento ocorreu corretamente
        self.assertRedirects(response, reverse('index'))