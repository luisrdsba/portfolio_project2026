from django.urls import path
from . import views

urlpatterns = [
    path('projetos/', views.projetos_view, name='projetos'),
    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('tfcs/', views.tfcs_view, name='tfcs'),
    path('unidades-curriculares/', views.unidades_curriculares_view, name='unidades_curriculares'),
    path('competencias/', views.competencias_view, name='competencias'),
    path('projeto/novo', views.novo_projeto_view, name='novo_projeto'),
    path('projeto/<int:projeto_id>/edita', views.edita_projeto_view, name='edita_projeto'),
    path('projeto/<int:projeto_id>/apaga', views.apaga_projeto_view, name='apaga_projeto'),
    path('', views.projetos_view),
]
