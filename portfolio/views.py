from django.shortcuts import render, redirect
from .models import Projeto, Tecnologia, TFC, UnidadeCurricular, Competencia
from .forms import ProjetoForm


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


def novo_projeto_view(request):
    form = ProjetoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('projetos')
    return render(request, 'portfolio/novo_projeto.html', {'form': form})


def edita_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)
        if form.is_valid():
            form.save()
            return redirect('projetos')
    else:
        form = ProjetoForm(instance=projeto)
    return render(request, 'portfolio/edita_projeto.html', {'form': form, 'projeto': projeto})


def apaga_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    projeto.delete()
    return redirect('projetos')
