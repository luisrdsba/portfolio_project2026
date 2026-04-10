import json
from pathlib import Path
import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fetches course details for Informática de Gestão (code 12) from the Lusófona API and saves to data/ULHT12-PT.json'

    def handle(self, *args, **options):
        url = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail'
        payload = {
            'language':   'PT',
            'courseCode': '12',
            'schoolYear': '202526',
        }

        self.stdout.write(f'Fetching course details from {url} ...')

        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status()

        data = response.json()

        output_path = Path(__file__).resolve().parents[3] / 'data' / 'ULHT12-PT.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Saved response to {output_path}'))
