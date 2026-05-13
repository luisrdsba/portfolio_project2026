from django.shortcuts import render, redirect
from .models import Projeto, Tecnologia, TFC, UnidadeCurricular, Competencia, Formacao
from .forms import ProjetoForm, TecnologiaForm, CompetenciaForm, FormacaoForm


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


def formacoes_view(request):
    formacoes = Formacao.objects.prefetch_related('tecnologias').all()
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})


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


def nova_tecnologia_view(request):
    form = TecnologiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('tecnologias')
    return render(request, 'portfolio/nova_tecnologia.html', {'form': form})


def edita_tecnologia_view(request, tecnologia_id):
    tecnologia = Tecnologia.objects.get(id=tecnologia_id)
    if request.method == 'POST':
        form = TecnologiaForm(request.POST, request.FILES, instance=tecnologia)
        if form.is_valid():
            form.save()
            return redirect('tecnologias')
    else:
        form = TecnologiaForm(instance=tecnologia)
    return render(request, 'portfolio/edita_tecnologia.html', {'form': form, 'tecnologia': tecnologia})


def apaga_tecnologia_view(request, tecnologia_id):
    tecnologia = Tecnologia.objects.get(id=tecnologia_id)
    tecnologia.delete()
    return redirect('tecnologias')


def nova_competencia_view(request):
    form = CompetenciaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('competencias')
    return render(request, 'portfolio/nova_competencia.html', {'form': form})


def edita_competencia_view(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)
    if request.method == 'POST':
        form = CompetenciaForm(request.POST, request.FILES, instance=competencia)
        if form.is_valid():
            form.save()
            return redirect('competencias')
    else:
        form = CompetenciaForm(instance=competencia)
    return render(request, 'portfolio/edita_competencia.html', {'form': form, 'competencia': competencia})


def apaga_competencia_view(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)
    competencia.delete()
    return redirect('competencias')


def nova_formacao_view(request):
    form = FormacaoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('formacoes')
    return render(request, 'portfolio/nova_formacao.html', {'form': form})


def edita_formacao_view(request, formacao_id):
    formacao = Formacao.objects.get(id=formacao_id)
    if request.method == 'POST':
        form = FormacaoForm(request.POST, request.FILES, instance=formacao)
        if form.is_valid():
            form.save()
            return redirect('formacoes')
    else:
        form = FormacaoForm(instance=formacao)
    return render(request, 'portfolio/edita_formacao.html', {'form': form, 'formacao': formacao})


def apaga_formacao_view(request, formacao_id):
    formacao = Formacao.objects.get(id=formacao_id)
    formacao.delete()
    return redirect('formacoes')
