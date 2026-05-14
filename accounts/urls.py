from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registo/', views.registo_view, name='registo'),
    path('magic-link/', views.magic_link_pedir, name='magic_link_pedir'),
    path('magic-link/entrar/<str:token>/', views.magic_link_entrar, name='magic_link_entrar'),
]
