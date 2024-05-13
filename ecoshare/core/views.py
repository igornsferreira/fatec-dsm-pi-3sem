from django.views import View
from django.shortcuts import render

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class CadastroView(View):
    def get(self, request):
        return render(request, 'cadastro.html')