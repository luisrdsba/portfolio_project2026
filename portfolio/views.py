from django.shortcuts import render
from .models import Projeto, Tecnologia, TFC, UnidadeCurricular, Competencia


def projetos_view(request):
    projetos = Projeto.objects.select_related('uc').prefetch_related('tecnologias').all()
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})


def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})


def tfcs_view(request):
    tfcs = TFC.objects.prefetch_related('tecnologias').all()
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})


def unidades_curriculares_view(request):
    ucs = UnidadeCurricular.objects.select_related('licenciatura').prefetch_related('docentes').all()
    return render(request, 'portfolio/unidades_curriculares.html', {'ucs': ucs})


def competencias_view(request):
    competencias = Competencia.objects.prefetch_related('projetos', 'tecnologias').all()
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})
