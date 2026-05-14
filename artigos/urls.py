from django.urls import path
from . import views

urlpatterns = [
    path('', views.artigos_lista, name='artigos_lista'),
]
