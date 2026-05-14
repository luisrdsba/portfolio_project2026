from django.urls import path
from . import views

urlpatterns = [
    path('', views.artigos_lista, name='artigos_lista'),
    path('novo/', views.novo_artigo, name='novo_artigo'),
    path('<int:artigo_id>/', views.artigo_detalhe, name='artigo_detalhe'),
    path('<int:artigo_id>/edita/', views.edita_artigo, name='edita_artigo'),
    path('<int:artigo_id>/apaga/', views.apaga_artigo, name='apaga_artigo'),
    path('<int:artigo_id>/like/', views.dar_like, name='dar_like'),
    path('<int:artigo_id>/comentar/', views.comentar, name='comentar'),
]
