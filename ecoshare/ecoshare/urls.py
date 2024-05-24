from django.contrib import admin
from django.urls import path
from core import views  
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('homeCliente/', login_required(views.HomeClienteView.as_view()), name='homeCliente'),
    path('relatorioCliente/', login_required(views.RelatorioClienteView.as_view()), name='relatorioCliente'),
    path('doacoesCliente/', login_required(views.DoacoesClienteView.as_view()), name='doacoesCliente'),
    path('brindesCliente/', login_required(views.BrindesClienteView.as_view()), name='brindesCliente'),
    path('perfilCliente/', login_required(views.PerfilClienteView.as_view()), name='perfilCliente'),
    path('editPerfilCliente/', login_required(views.EditPerfilClienteView.as_view()), name='editPerfilCliente'),
    path('logout/', views.LogoutView, name='logout'),

]

