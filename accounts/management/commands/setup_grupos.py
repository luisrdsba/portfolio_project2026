from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from portfolio.models import (
    Projeto, Tecnologia, Competencia, Formacao, TipoTecnologia,
    UnidadeCurricular, TFC, Docente, Licenciatura, MakingOf
)


class Command(BaseCommand):
    help = 'Cria o grupo gestor-portfolio com as permissoes apropriadas'

    def handle(self, *args, **options):
        grupo, created = Group.objects.get_or_create(name='gestor-portfolio')
        status = 'Criado' if created else 'Ja existia'
        self.stdout.write(f'{status}: grupo gestor-portfolio')

        modelos = [Projeto, Tecnologia, Competencia, Formacao, TipoTecnologia,
                   UnidadeCurricular, TFC, Docente, Licenciatura, MakingOf]

        for modelo in modelos:
            ct = ContentType.objects.get_for_model(modelo)
            perms = Permission.objects.filter(content_type=ct)
            for perm in perms:
                grupo.permissions.add(perm)
            self.stdout.write(f'  Permissoes adicionadas para {modelo.__name__}')

        gestor_user, created = User.objects.get_or_create(
            username='gestor',
            defaults={
                'email': 'gestor@exemplo.com',
                'first_name': 'Gestor',
                'is_staff': True,
            }
        )
        if created:
            gestor_user.set_password('gestor123')
            gestor_user.save()
            self.stdout.write('Utilizador gestor criado (password: gestor123)')
        gestor_user.groups.add(grupo)
        self.stdout.write('Utilizador gestor adicionado ao grupo')

        self.stdout.write(self.style.SUCCESS('Grupo configurado com sucesso.'))
