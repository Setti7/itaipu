from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path("editar-visitante", views.editar_visitante, name='editar-visitante'),
    path("editar-telefone", views.editar_telefone, name='editar-telefone'),
]
