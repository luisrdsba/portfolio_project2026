from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistoForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('projetos')
        return render(request, 'accounts/login.html', {'mensagem': 'Credenciais invalidas'})
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('projetos')


def registo_view(request):
    if request.method == 'POST':
        form = RegistoForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('projetos')
    else:
        form = RegistoForm()
    return render(request, 'accounts/registo.html', {'form': form})
