from django.contrib import admin
from .models import Artigo, Like, Comentario


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_criacao')
    list_filter = ('data_criacao', 'autor')
    search_fields = ('titulo', 'texto')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'sessao', 'data')
    list_filter = ('data',)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'autor', 'data')
    list_filter = ('data', 'autor')
    search_fields = ('texto',)
