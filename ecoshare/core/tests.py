from django.test import TestCase
from .models import EnderecoModel, DoacaoModel, UsuarioModel

class EnderecoVazioTest(TestCase):
    def __init__(self, *args, **kwargs):
        self.address = kwargs.pop('address', 'http://127.0.0.1:8000')
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.resp = self.client.get('/')

    def test_200_response(self):
        self.assertEqual(200, self.resp.status_code)
        
    def test_templateUsed(self):
        self.assertTemplateUsed(self.resp, 'index.html')

        
