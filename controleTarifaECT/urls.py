#Controle de Tarifas URLs
from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^$', views.getFile, name='index'),
    url(r'table/', views.table, name='table'),
    url(r'formTest/', views.formDeTest, name='Form'),
]