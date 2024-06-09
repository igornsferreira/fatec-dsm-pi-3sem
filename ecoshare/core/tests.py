from django.test import TestCase, Client
from django.urls import reverse
from .forms import EnderecoForm, DoacaoForm, UsuarioForm
from .models import EnderecoModel, DoacaoModel, UsuarioModel
from django.contrib.auth.models import User
import datetime

class IndexViewTest(TestCase):
    """Verifica se os metodos GET e POST de IndexView estão corretos."""
    def test_index_view(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class CadastroViewTest(TestCase):
    """Verifica se os metodos GET e POST de CadastroView estão corretos."""
    def setUp(self):
        self.client = Client()
        self.url = reverse('cadastro')

    def test_get_cadastro(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro.html')

    def test_post_cadastro(self):
        form_data = {
            'nome_completo': 'John Doe',
            'email': 'john@example.com',
            'senha': 'password123',
            'confirm_senha': 'password123',
            'cep': '12345-678',
            'rua': 'Main St',
            'bairro': 'Centro',
            'numero': '123',
            'cidade': 'City',
            'estado': 'State',
            'pais': 'Country',
            'cpf': '12345678900',
            'telefone': '123456789',
            'data_nascimento': '1990-01-01',
        }
        response = self.client.post(self.url, form_data)
        self.assertRedirects(response, reverse('homeCliente'))
        user = User.objects.get(username='john@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(UsuarioModel.objects.filter(user=user).exists())
        self.assertTrue(EnderecoModel.objects.filter(cep='12345-678').exists())

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.user = User.objects.create_user(username='john@example.com', email='john@example.com', password='password123')

    def test_get_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_login(self):
        response = self.client.post(self.url, {'email': 'john@example.com', 'senha': 'password123'})
        self.assertRedirects(response, reverse('homeCliente'))

class RelatorioClienteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='john@example.com', email='john@example.com', password='password123')
        self.usuario = UsuarioModel.objects.create(user=self.user, nome_completo='John Doe')
        self.client.login(username='john@example.com', password='password123')

    def test_get_relatorio_cliente(self):
        response = self.client.get(reverse('relatorioCliente'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'relatorioCliente.html')

class EnderecoFormTest(TestCase):
    def test_endereco_form_valid(self):
        form_data = {
            'cep': '12345-678',
            'rua': 'Rua Principal',
            'bairro': 'Centro',
            'numero': '123',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'pais': 'Pais'
        }
        form = EnderecoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_endereco_form_invalid_cep(self):
        form_data = {
            'cep': '12345678',
            'rua': 'Rua Principal',
            'bairro': 'Centro',
            'numero': '123',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'pais': 'Pais'
        }
        form = EnderecoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cep', form.errors)


class DoacaoFormTest(TestCase):
    def test_doacao_form_valid(self):
        form_data = {
            'material_doado': 'Roupas',
            'peso': 10,
            'data': datetime.datetime.now(),
            'item_recebido': 'Camisa',
            'validacao': False
        }
        form = DoacaoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_doacao_form_invalid_peso(self):
        form_data = {
            'material_doado': 'Roupas',
            'peso': 0,
            'data': datetime.datetime.now(),
            'item_recebido': 'Camisa',
            'validacao': False
        }
        form = DoacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('peso', form.errors)


class UsuarioFormTest(TestCase):
    def test_usuario_form_valid(self):
        endereco = EnderecoModel.objects.create(
            cep="12345-678",
            rua="Rua Principal",
            bairro="Centro",
            numero="123",
            cidade="Cidade",
            estado="Estado",
            pais="Pais"
        )
        user = User.objects.create_user(username='testuser', password='12345')
        form_data = {
            'nome_completo': 'John Doe',
            'cpf': '123.456.789-00',
            'email': 'john@example.com',
            'telefone': '(12) 3456-7890',
            'data_nascimento': '2000-01-01',
            'endereco': endereco,
            'doacoes': []
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_usuario_form_invalid_cpf(self):
        endereco = EnderecoModel.objects.create(
            cep="12345-678",
            rua="Rua Principal",
            bairro="Centro",
            numero="123",
            cidade="Cidade",
            estado="Estado",
            pais="Pais"
        )
        user = User.objects.create_user(username='testuser', password='12345')
        form_data = {
            'nome_completo': 'John Doe',
            'cpf': '12345678900',
            'email': 'john@example.com',
            'telefone': '(12) 3456-7890',
            'data_nascimento': '2000-01-01',
            'endereco': endereco,
            'doacoes': []
        }
        form = UsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cpf', form.errors)

    def test_usuario_form_invalid_telefone(self):
        endereco = EnderecoModel.objects.create(
            cep="12345-678",
            rua="Rua Principal",
            bairro="Centro",
            numero="123",
            cidade="Cidade",
            estado="Estado",
            pais="Pais"
        )
        user = User.objects.create_user(username='testuser', password='12345')
        form_data = {
            'nome_completo': 'John Doe',
            'cpf': '123.456.789-00',
            'email': 'john@example.com',
            'telefone': '1234567890',
            'data_nascimento': '2000-01-01',
            'endereco': endereco,
            'doacoes': []
        }
        form = UsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefone', form.errors)