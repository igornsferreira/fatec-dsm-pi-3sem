from django.test import TestCase, Client
from django.urls import reverse
from core.models import UsuarioModel, DoacaoModel, EnderecoModel

class UsuarioTest(TestCase):
    def setUp(self):
        UsuarioModel.objects.create(
            nome_completo='Bruno',
            cpf='11111111111',
            email='email@email.com',
            telefone='19999999999',
        )
        
    def test_usuario(self):
        """Verificando as informações do usuário."""
        bruno = UsuarioModel.objects.get(cpf='11111111111')
        self.assertEqual(bruno.nome_completo, 'Bruno')
        self.assertEqual(bruno.email, 'email@email.com')
        self.assertEqual(bruno.telefone, '19999999999')
        self.assertEqual(bruno.cpf, '11111111111')
        