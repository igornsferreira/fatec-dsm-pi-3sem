from django.test import TestCase
from .models import EnderecoModel, DoacaoModel, UsuarioModel

class EnderecoVazioTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_200_response(self):
        self.assertEqual(200, self.resp.status_code)
        
    def test_templateUsed(self):
        self.assertTemplateUsed(self.resp, 'index.html')

        
