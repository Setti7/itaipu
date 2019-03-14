from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path("editar-visitante/", views.EditarVisitante.as_view(), name='editar-visitante'),
    path("editar-telefone/", views.EditarTelefone.as_view(), name='editar-telefone'),
    path("editar-morador/", views.EditarMorador.as_view(), name='editar-morador'),
    path("aviso-lido/", views.MarqueAvisoComoLido.as_view(), name='aviso-lido'),
]
