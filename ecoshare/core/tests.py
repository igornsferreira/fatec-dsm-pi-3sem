from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import UsuarioModel, DoacaoModel

class CadastroViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('cadastro')

    def test_get_cadastro_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro.html')

    def test_post_cadastro_view(self):
        data = {
            'nome_completo': 'Fulano',
            'email': 'fulano@example.com',
            'senha': '123456',
            'cpf': '123.456.789-01',
            'cep': '12345-678',
            'rua': 'Rua Exemplo',
            'bairro': 'Bairro Teste',
            'numero': '123',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'pais': 'País'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='fulano@example.com').exists())
        self.assertTrue(UsuarioModel.objects.filter(cpf='123.456.789-01').exists())
        self.assertRedirects(response, reverse('homeCliente'))

    def test_post_cadastro_view_existing_user(self):
        User.objects.create_user(username='fulano@example.com', email='fulano@example.com', password='123456')
        data = {
            'nome_completo': 'Fulano',
            'email': 'fulano@example.com',
            'senha': '123456',
            'cpf': '123.456.789-01',
            'cep': '12345-678',
            'rua': 'Rua Exemplo',
            'bairro': 'Bairro Teste',
            'numero': '123',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'pais': 'País'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'cadastro.html')
        self.assertContains(response, 'Já existe um usuário com este email ou CPF cadastrado.')

class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='123456')

    def test_get_login_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_login_view_valid_credentials(self):
        data = {
            'email': 'test@example.com',
            'senha': '123456',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('homeCliente'))

    def test_post_login_view_invalid_credentials(self):
        data = {
            'email': 'test@example.com',
            'senha': 'invalidpassword',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'E-mail ou senha incorretos.')

class HomeClienteViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('homeCliente')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='123456')
        self.client.login(username='test@example.com', password='123456')

    def test_get_home_cliente_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homeCliente.html')
        self.assertContains(response, 'Nome do usuário')

    def test_home_cliente_view_doacoes(self):
        doacao = DoacaoModel.objects.create(material_doado='Material Teste', peso=10, item_recebido='Item Teste', validacao=False)
        usuario = UsuarioModel.objects.get(user=self.user)
        usuario.doacoes.add(doacao)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homeCliente.html')

class RelatorioClienteViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('relatorioCliente')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='123456')
        self.client.login(username='test@example.com', password='123456')

    def test_get_relatorio_cliente_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'relatorioCliente.html')

    def test_relatorio_cliente_view_delete(self):
        doacao = DoacaoModel.objects.create(material_doado='Material Teste', peso=10, item_recebido='Item Teste', validacao=False)
        usuario = UsuarioModel.objects.get(user=self.user)
        usuario.doacoes.add(doacao)

        response = self.client.post(self.url, {'action': 'delete', 'doacao_id': str(doacao.pk)})
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(DoacaoModel.objects.filter(pk=doacao.pk).exists())

    def test_relatorio_cliente_view_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'relatorioCliente.html')
        self.assertContains(response, 'Senha Aleatória')

    def test_relatorio_cliente_view_no_doacoes(self):
        usuario = UsuarioModel.objects.get(user=self.user)
        usuario.doacoes.clear()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'relatorioCliente.html')
        self.assertContains(response, 'Nenhuma doação encontrada.')
        
class TemplateTests(TestCase):

    def test_index_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_cadastro_template(self):
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro.html')

    def test_login_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_home_cliente_template(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='123456')
        self.client.login(username='test@example.com', password='123456')
        response = self.client.get(reverse)