from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('relatorios/tokens/', views.token_pdf, name='token_pdf'),
    path('configs/', views.configs, name='configs'),

    path('editar-chacara/novo-residente/', views.NovoResidenteView.as_view(), name='novo residente'),
    path('editar-chacara/<int:page>/', views.EditarChacaraView.as_view(), name='editar chacara'),

    path('autorizar-visitas/<int:page>/', views.autorizar_visitas, name='autorizar visitas'),
    path('autorizar-visitas/<int:page>/blacklist/', views.autorizar_visitas_blacklist,
         name='autorizar visitas blacklist'),
    path('autorizar-visitas/novo-visitante/', views.NovoVisitanteView.as_view(), name='novo visitante'),

    path('<str:code>/', views.error),
]
