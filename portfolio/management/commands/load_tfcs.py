import json
from pathlib import Path
from django.core.management.base import BaseCommand
from portfolio.models import TFC


class Command(BaseCommand):
    help = 'Loads TFCs from data/tfcs_2025.json into the database'

    def handle(self, *args, **options):
        json_path = Path(__file__).resolve().parents[3] / 'data' / 'tfcs_2025.json'

        with open(json_path, encoding='utf-8') as f:
            tfcs_data = json.load(f)

        created_count = 0
        skipped_count = 0

        for data in tfcs_data:
            tfc, created = TFC.objects.get_or_create(
                titulo=data['titulo'],
                ano=data['ano'],
                defaults={
                    'autor':        data.get('autor', ''),
                    'orientador':   data.get('orientador', ''),
                    'tipo':         data.get('tipo', 'licenciatura'),
                    'resumo':       data.get('resumo', ''),
                    'palavras_chave': data.get('palavras_chave', ''),
                    'destaque':     data.get('destaque', False),
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"  Created: {tfc}")
            else:
                skipped_count += 1
                self.stdout.write(f"  Already exists: {tfc}")

        self.stdout.write(self.style.SUCCESS(
            f'\nDone — {created_count} created, {skipped_count} already existed.'
        ))
