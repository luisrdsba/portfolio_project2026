from django.shortcuts import render
from .models import Artigo


def artigos_lista(request):
    artigos = Artigo.objects.select_related('autor').all()
    return render(request, 'artigos/lista.html', {'artigos': artigos})
