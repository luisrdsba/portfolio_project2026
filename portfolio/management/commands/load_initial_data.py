from django.core.management.base import BaseCommand
from portfolio.models import Licenciatura, Docente, UnidadeCurricular, Tecnologia, Projeto, Competencia


class Command(BaseCommand):
    help = 'Loads initial data into the database'

    def handle(self, *args, **options):
        # Licenciatura
        licenciatura, created = Licenciatura.objects.get_or_create(
            nome='Informática de Gestão',
            defaults={
                'instituicao': 'Universidade Lusófona',
                'ano_inicio': 2024,
                'website': 'https://www.ulusofona.pt',
            }
        )
        self.stdout.write(f"{'Created' if created else 'Already exists'}: Licenciatura — {licenciatura}")

        # Docentes
        docentes_data = [
            {'nome': 'Lúcio Studer Ferreira', 'pagina_lusofona': 'https://www.ulusofona.pt/lisboa/docentes/lucio-miguel-studer-ferreira-6069'},
            {'nome': 'João Caldeira',          'pagina_lusofona': 'https://www.ulusofona.pt/lisboa/docentes/joao-carlos-palmela-pinheiro-caldeira-7559'},
            {'nome': 'Rui Ribeiro',            'pagina_lusofona': 'https://www.ulusofona.pt/lisboa/docentes/rui-pedro-nobre-ribeiro-3113'},
            {'nome': 'Bruno Cipriano',         'pagina_lusofona': 'https://www.ulusofona.pt/lisboa/docentes/bruno-miguel-pereira-cipriano-4453'},
            {'nome': 'Pedro Alves',            'pagina_lusofona': 'https://www.ulusofona.pt/lisboa/docentes/pedro-hugo-de-queiros-alves-4997'},
        ]

        docentes = {}
        for d in docentes_data:
            obj, created = Docente.objects.update_or_create(
                nome=d['nome'],
                defaults={'pagina_lusofona': d['pagina_lusofona']},
            )
            docentes[d['nome']] = obj
            self.stdout.write(f"{'Created' if created else 'Updated'}: Docente — {obj}")

        lucio = docentes['Lúcio Studer Ferreira']
        joao  = docentes['João Caldeira']

        # Unidades Curriculares
        ucs_data = [
            # 1º Ano - 1º Semestre
            {'nome': 'Contabilidade',                      'sigla': 'CONT', 'ano': 1, 'semestre': 1, 'ects': 6},
            {'nome': 'Fundamentos de Sistemas de Informação','sigla': 'FSI', 'ano': 1, 'semestre': 1, 'ects': 7},
            {'nome': 'Matemática I',                        'sigla': 'MAT1','ano': 1, 'semestre': 1, 'ects': 6},
            {'nome': 'Teoria e Prática de Marketing',       'sigla': 'TPM', 'ano': 1, 'semestre': 1, 'ects': 5},
            # 1º Ano - 2º Semestre
            {'nome': 'Algoritmia e Estruturas de Dados',    'sigla': 'AED', 'ano': 1, 'semestre': 2, 'ects': 6},
            {'nome': 'Cálculo Financeiro',                  'sigla': 'CF',  'ano': 1, 'semestre': 2, 'ects': 5},
            {'nome': 'Competências Comportamentais',         'sigla': 'CC',  'ano': 1, 'semestre': 2, 'ects': 4},
            {'nome': 'Fundamentos de Programação',          'sigla': 'FP',  'ano': 1, 'semestre': 2, 'ects': 6},
            {'nome': 'Linguagens de Programação I',         'sigla': 'LP1', 'ano': 1, 'semestre': 2, 'ects': 5},
            {'nome': 'Matemática II',                       'sigla': 'MAT2','ano': 1, 'semestre': 2, 'ects': 5},
            {'nome': 'Métricas Empresariais',               'sigla': 'ME',  'ano': 1, 'semestre': 2, 'ects': 5},
            # 2º Ano - 1º Semestre
            {'nome': 'Bases de Dados',                      'sigla': 'BD',  'ano': 2, 'semestre': 1, 'ects': 6},
            {'nome': 'Direito Informático',                 'sigla': 'DI',  'ano': 2, 'semestre': 1, 'ects': 3},
            {'nome': 'Instrumentos de Gestão',              'sigla': 'IG',  'ano': 2, 'semestre': 1, 'ects': 6},
            {'nome': 'Motivação e Liderança',               'sigla': 'ML',  'ano': 2, 'semestre': 1, 'ects': 3},
            {'nome': 'Programação Low-Code e No-Code',      'sigla': 'PLCNC','ano': 2,'semestre': 1, 'ects': 6},
            {'nome': 'Sistemas Operativos',                 'sigla': 'SO',  'ano': 2, 'semestre': 1, 'ects': 6},
            # 2º Ano - 2º Semestre
            {'nome': 'Engenharia de Requisitos e Testes',   'sigla': 'ERT', 'ano': 2, 'semestre': 2, 'ects': 6},
            {'nome': 'Gestão Financeira',                   'sigla': 'GF',  'ano': 2, 'semestre': 2, 'ects': 6},
            {'nome': 'Programação Web',                     'sigla': 'PW',  'ano': 2, 'semestre': 2, 'ects': 6},
            {'nome': 'Redes de Computadores',               'sigla': 'RC',  'ano': 2, 'semestre': 2, 'ects': 6},
            {'nome': 'Sistemas de Suporte à Decisão',       'sigla': 'SSD', 'ano': 2, 'semestre': 2, 'ects': 6},
            # 3º Ano - 1º Semestre
            {'nome': 'Data Mining',                         'sigla': 'DM',  'ano': 3, 'semestre': 1, 'ects': 5},
            {'nome': 'Engenharia de Software',              'sigla': 'ES',  'ano': 3, 'semestre': 1, 'ects': 5},
            {'nome': 'Interação Humano-Máquina',            'sigla': 'IHM', 'ano': 3, 'semestre': 1, 'ects': 5},
            {'nome': 'Sistemas Móveis Empresariais',        'sigla': 'SME', 'ano': 3, 'semestre': 1, 'ects': 5},
            # 3º Ano - 2º Semestre
            {'nome': 'Auditoria de Sistemas de Informação', 'sigla': 'ASI', 'ano': 3, 'semestre': 2, 'ects': 4},
            {'nome': 'Controlo de Gestão',                  'sigla': 'CG',  'ano': 3, 'semestre': 2, 'ects': 3},
            {'nome': 'Gestão de Projetos',                  'sigla': 'GP',  'ano': 3, 'semestre': 2, 'ects': 3},
            {'nome': 'Inteligência Artificial',             'sigla': 'IA',  'ano': 3, 'semestre': 2, 'ects': 5},
            {'nome': 'Sistemas de Informação na Nuvem',     'sigla': 'SIN', 'ano': 3, 'semestre': 2, 'ects': 5},
            # 3º Ano - Anual (semestre 0 para indicar anual)
            {'nome': 'Trabalho Final de Curso',             'sigla': 'TFC', 'ano': 3, 'semestre': 0, 'ects': 20},
        ]

        ucs = {}
        for data in ucs_data:
            uc, created = UnidadeCurricular.objects.get_or_create(
                nome=data['nome'],
                licenciatura=licenciatura,
                defaults={
                    'sigla': data['sigla'],
                    'ano': data['ano'],
                    'semestre': data['semestre'],
                    'ects': data['ects'],
                }
            )
            ucs[data['nome']] = uc
            self.stdout.write(f"{'Created' if created else 'Already exists'}: UC — {uc}")

        # Assign docentes to UCs
        ucs['Programação Web'].docentes.add(lucio, joao)
        ucs['Bases de Dados'].docentes.add(lucio)

        # Tecnologias
        tecnologias_data = [
            {'nome': 'Python',  'categoria': 'linguagem'},
            {'nome': 'Django',  'categoria': 'framework'},
            {'nome': 'HTML',    'categoria': 'linguagem'},
            {'nome': 'CSS',     'categoria': 'linguagem'},
            {'nome': 'Git',     'categoria': 'ferramenta'},
        ]

        tecnologias = {}
        for data in tecnologias_data:
            tec, created = Tecnologia.objects.get_or_create(
                nome=data['nome'],
                defaults={
                    'categoria': data['categoria'],
                    'nivel_interesse': 3,
                }
            )
            tecnologias[data['nome']] = tec
            self.stdout.write(f"{'Created' if created else 'Already exists'}: Tecnologia — {tec}")

        # Projeto
        projeto, created = Projeto.objects.get_or_create(
            titulo='Batalha Naval em C',
            defaults={
                'descricao': 'Jogo de batalha naval desenvolvido em linguagem C',
                'uc': ucs['Fundamentos de Programação'],
            }
        )
        self.stdout.write(f"{'Created' if created else 'Already exists'}: Projeto — {projeto}")

        # Competencias
        competencias_data = [
            {'nome': 'Programação em Python',          'tipo': 'tecnica',    'nivel': 3},
            {'nome': 'Desenvolvimento Web HTML e CSS',  'tipo': 'tecnica',    'nivel': 3},
            {'nome': 'Bases de Dados',                  'tipo': 'tecnica',    'nivel': 2},
            {'nome': 'Git e controlo de versões',       'tipo': 'tecnica',    'nivel': 2},
            {'nome': 'Resolução de problemas',          'tipo': 'soft',       'nivel': 3},
            {'nome': 'Trabalho em equipa',              'tipo': 'soft',       'nivel': 3},
            {'nome': 'Inglês',                          'tipo': 'linguistica','nivel': 4},
        ]

        for data in competencias_data:
            comp, created = Competencia.objects.get_or_create(
                nome=data['nome'],
                defaults={
                    'tipo': data['tipo'],
                    'nivel': data['nivel'],
                }
            )
            self.stdout.write(f"{'Created' if created else 'Already exists'}: Competência — {comp}")

        self.stdout.write(self.style.SUCCESS('\nInitial data loaded successfully.'))
