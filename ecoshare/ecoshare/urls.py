from django.contrib import admin
from django.urls import path
from core import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('homeCliente/', views.HomeClienteView.as_view(), name='homeCliente'),
    path('relatorioCliente/', views.RelatorioClienteView.as_view(), name='relatorioCliente'),
    path('doacoesCliente/', views.DoacoesClienteView.as_view(), name='doacoesCliente'),
    path('brindesCliente/', views.BrindesClienteView.as_view(), name='brindesCliente'),
    path('perfilCliente/', views.PerfilClienteView.as_view(), name='perfilCliente'),
]

