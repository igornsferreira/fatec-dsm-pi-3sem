from sqlite3 import IntegrityError
from django.test import TestCase
from .models import EnderecoModel, DoacaoModel, UsuarioModel

class EnderecoVazioTest(TestCase):
    def __init__(self, *args, **kwargs):
        self.address = kwargs.pop('address', 'http://127.0.0.1:8000')
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.resp = self.client.get('/')

    def test_200_response(self):
        # Testa se a resposta HTTP é 200 (OK)
        self.assertEqual(200, self.resp.status_code)
        
    def test_templateUsed(self):
        # Testa se o template 'index.html' é usado
        self.assertTemplateUsed(self.resp, 'index.html')

    class EnderecoModelTest(TestCase):
        def test_str_representation(self):
            endereco = EnderecoModel(cep="12345-678", rua="Rua Principal")
            self.assertEqual(str(endereco), "12345-678 - Rua Principal")

    class DoacaoModelTest(TestCase):
        def test_validacao_default_value(self):
            doacao = DoacaoModel(material_doado="Roupas", peso=10)
            self.assertFalse(doacao.validacao)

    class UsuarioModelTest(TestCase):
        def test_email_unique_constraint(self):
            # Testa se o campo de e-mail é único
            usuario1 = UsuarioModel(email="user@example.com")
            usuario2 = UsuarioModel(email="user@example.com")
            usuario1.save()
            with self.assertRaises(IntegrityError):
                usuario2.save()
