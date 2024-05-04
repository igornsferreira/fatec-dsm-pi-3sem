from django.views import View
from django.shortcuts import render, redirect

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class CadastroView(View):
    def get(self, request):
        return render(request, 'cadastro.html')

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})
