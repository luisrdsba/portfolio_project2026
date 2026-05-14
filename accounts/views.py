from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.urls import reverse
from .forms import RegistoForm
from .models import MagicLink


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
            grupo_autores, _ = Group.objects.get_or_create(name='autores')
            user.groups.add(grupo_autores)
            login(request, user)
            return redirect('artigos_lista')
    else:
        form = RegistoForm()
    return render(request, 'accounts/registo.html', {'form': form})


def magic_link_pedir(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'accounts/magic_link_pedir.html', {
                'mensagem': 'Se este email estiver registado, recebera um link de acesso em breve.'
            })

        magic = MagicLink(user=user)
        magic.gerar_token()
        magic.save()

        link = request.build_absolute_uri(
            reverse('magic_link_entrar', args=[magic.token])
        )

        send_mail(
            subject='O teu link de acesso ao portfolio',
            message=f'Clica neste link para entrares na tua conta:\n\n{link}\n\nO link expira em 15 minutos.',
            from_email=None,
            recipient_list=[email],
        )

        return render(request, 'accounts/magic_link_pedir.html', {
            'mensagem': 'Se este email estiver registado, recebera um link de acesso em breve.'
        })

    return render(request, 'accounts/magic_link_pedir.html')


def magic_link_entrar(request, token):
    try:
        magic = MagicLink.objects.get(token=token)
    except MagicLink.DoesNotExist:
        return render(request, 'accounts/magic_link_erro.html', {
            'mensagem': 'Link invalido.'
        })

    if not magic.is_valido():
        return render(request, 'accounts/magic_link_erro.html', {
            'mensagem': 'Link expirado ou ja utilizado.'
        })

    magic.usado = True
    magic.save()
    login(request, magic.user)
    return redirect('projetos')
