from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Artigo
from .forms import ArtigoForm


def is_autor(user):
    return user.is_authenticated and user.groups.filter(name='autores').exists()


def artigos_lista(request):
    artigos = Artigo.objects.select_related('autor').all()
    return render(request, 'artigos/lista.html', {
        'artigos': artigos,
        'is_autor': is_autor(request.user),
    })


def artigo_detalhe(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    pode_editar = request.user.is_authenticated and artigo.autor == request.user
    return render(request, 'artigos/detalhe.html', {
        'artigo': artigo,
        'pode_editar': pode_editar,
    })


@login_required
def novo_artigo(request):
    if not is_autor(request.user):
        return redirect('artigos_lista')
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user
            artigo.save()
            return redirect('artigo_detalhe', artigo_id=artigo.id)
    else:
        form = ArtigoForm()
    return render(request, 'artigos/novo.html', {'form': form})


@login_required
def edita_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    if artigo.autor != request.user:
        return redirect('artigos_lista')
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES, instance=artigo)
        if form.is_valid():
            form.save()
            return redirect('artigo_detalhe', artigo_id=artigo.id)
    else:
        form = ArtigoForm(instance=artigo)
    return render(request, 'artigos/edita.html', {'form': form, 'artigo': artigo})


@login_required
def apaga_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    if artigo.autor != request.user:
        return redirect('artigos_lista')
    artigo.delete()
    return redirect('artigos_lista')
