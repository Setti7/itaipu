from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('relatorios/tokens', views.token_pdf, name='token_pdf'),
    path('configs/', views.configs, name='configs'),

    path('editar-chacara/', views.EditarChacara.as_view(), name='editar-chacara'),

    path('autorizar-visitas/<int:page>/', views.autorizar_visitas, name='autorizar visitas'),
    path('autorizar-visitas/<int:page>/blacklist', views.autorizar_visitas_blacklist,
         name='autorizar visitas blacklist'),
    path('autorizar-visitas/novo-visitante', views.novo_visitante, name='novo visitante'),

    path('<str:code>/', views.error),
]
