from django.contrib import admin
from .models import (
    Licenciatura, Docente, UnidadeCurricular,
    Tecnologia, Projeto, TFC, Competencia, Formacao, MakingOf
)


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instituicao', 'ano_inicio', 'ano_fim')
    search_fields = ('nome', 'instituicao')


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'pagina_lusofona')
    search_fields = ('nome', 'email')


@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'ano', 'semestre', 'ects', 'licenciatura')
    list_filter = ('ano', 'semestre', 'licenciatura')
    search_fields = ('nome', 'sigla')
    filter_horizontal = ('docentes',)


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'nivel_interesse', 'destaque')
    list_filter = ('categoria', 'nivel_interesse', 'destaque')
    search_fields = ('nome',)


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'uc', 'data_conclusao', 'destaque')
    list_filter = ('uc', 'destaque', 'tecnologias')
    search_fields = ('titulo', 'descricao')
    filter_horizontal = ('tecnologias',)


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'orientador', 'ano', 'tipo', 'destaque')
    list_filter = ('tipo', 'ano', 'destaque')
    search_fields = ('titulo', 'autor', 'orientador', 'palavras_chave')
    filter_horizontal = ('tecnologias',)


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'nivel')
    list_filter = ('tipo', 'nivel')
    search_fields = ('nome',)
    filter_horizontal = ('projetos', 'tecnologias')


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'instituicao', 'data_inicio', 'data_fim')
    list_filter = ('tipo',)
    search_fields = ('titulo', 'instituicao')
    filter_horizontal = ('tecnologias',)


@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'entidade_relacionada', 'data')
    list_filter = ('entidade_relacionada', 'data')
    search_fields = ('titulo', 'descricao')
