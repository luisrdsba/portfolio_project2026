from django.contrib import admin
from .models import Artigo


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_criacao')
    list_filter = ('data_criacao', 'autor')
    search_fields = ('titulo', 'texto')
