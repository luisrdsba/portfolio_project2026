import os
from django.core.files import File
from django.core.management.base import BaseCommand
from portfolio.models import (
    Licenciatura, UnidadeCurricular, Projeto, Tecnologia,
    Formacao, MakingOf
)
from artigos.models import Artigo


class Command(BaseCommand):
    help = 'Migra ficheiros de media locais para Cloudinary'

    def migrar_campo(self, obj, campo_nome):
        campo = getattr(obj, campo_nome)
        if not campo or not campo.name:
            return False
        try:
            local_path = campo.path
        except Exception:
            return False
        if not os.path.exists(local_path):
            return False
        with open(local_path, 'rb') as f:
            nome_ficheiro = os.path.basename(local_path)
            campo.save(nome_ficheiro, File(f), save=True)
        return True

    def handle(self, *args, **options):
        migracoes = [
            (Licenciatura, 'logo'),
            (UnidadeCurricular, 'imagem'),
            (Projeto, 'imagem'),
            (Tecnologia, 'logo'),
            (Formacao, 'certificado'),
            (MakingOf, 'fotografia'),
            (Artigo, 'fotografia'),
        ]

        for modelo, campo in migracoes:
            self.stdout.write(f'\nMigrando {modelo.__name__}.{campo}...')
            count = 0
            for obj in modelo.objects.all():
                if self.migrar_campo(obj, campo):
                    count += 1
                    self.stdout.write(f'  Migrado: {obj}')
            self.stdout.write(self.style.SUCCESS(f'  Total: {count} ficheiros'))

        self.stdout.write(self.style.SUCCESS('\nMigracao concluida.'))
