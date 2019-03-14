from django.urls import path
from . import views

urlpatterns = [
    path('', views.AvisoListView.as_view(), name='avisos'),
]
