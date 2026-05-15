from django.core.management.base import BaseCommand
from portfolio.models import MakingOf


class Command(BaseCommand):
    help = 'Carrega entradas do Making-Of da Ficha 8'

    def handle(self, *args, **options):
        entradas = [
            {
                'titulo': 'Ajustes na modelação das tecnologias',
                'entidade_relacionada': 'outro',
                'descricao': '''Revi a modelação das tecnologias. O campo categoria que tinha era um CharField com choices fixos, o que era limitado.

Decidi criar uma entidade nova, TipoTecnologia, ligada por ForeignKey. Fica mais flexivel: posso adicionar tipos pelo admin sem mexer no codigo, e cada tipo pode ter descrição própria.''',
                'erros_correcoes': '''A primeira tentativa de fazer a migration falhou. Como ja tinha tecnologias na base de dados e o campo tipo era obrigatório, o Django nao sabia o que pôr nas linhas existentes.

Solução: pus null=True, blank=True no campo. Assim as tecnologias antigas ficam sem tipo e atualizo depois.''',
                'uso_ia': '',
            },
            {
                'titulo': 'CRUD para Projetos',
                'entidade_relacionada': 'projeto',
                'descricao': '''Implementei criar/editar/apagar projetos. Usei ModelForm em vez de fazer o HTML manualmente.

Porque ModelForm:
- Muito menos código
- Validação automatica
- Se mudar o modelo o form atualiza sozinho

Primeira vez que fiz CRUD completo. A lógica das três views (criar, editar, apagar) é parecida mas com pequenas diferenças. Tive como referencia o tutorial da biblioteca.''',
                'erros_correcoes': '''Tres erros tipicos pelo caminho:

1. Esqueci o csrf token no form, deu 403 Forbidden. Adicionei {% csrf_token %} e ficou.

2. As imagens nao faziam upload. Faltava enctype=multipart/form-data no form e request.FILES na view. Rapido de corrigir mas se nao souberes ficas perdido.

3. Na edição, se nao mexesse na imagem ela ficava em branco. Resolvi garantindo que o request.FILES é sempre passado.''',
                'uso_ia': '',
            },
            {
                'titulo': 'Estender CRUD às outras entidades',
                'entidade_relacionada': 'tecnologia',
                'descricao': '''Depois do Projeto fiz o mesmo para Tecnologia, Competencia e Formacao. Foi basicamente copy paste com pequenos ajustes nos nomes e redirects.

Percebi o DRY (Don't Repeat Yourself) na prática. Em projetos maiores isto provavelmente seria abstraido em Class-Based Views mas para já prefiro escrever tudo explicito.''',
                'erros_correcoes': 'Os campos ManyToMany aparecem como caixas de seleção feias por defeito. Existem widgets melhores mas deixei assim para focar na funcionalidade.',
                'uso_ia': '',
            },
            {
                'titulo': 'Adicionar TipoTecnologia ao código',
                'entidade_relacionada': 'tecnologia',
                'descricao': '''Criei a entidade TipoTecnologia. Adicionei ForeignKey no Tecnologia a apontar para este novo modelo.

Tipos definidos: Frontend, Backend, Base de Dados, Storage, Ferramenta de Desenvolvimento, Outro.

Atualizei o script load_initial_data para criar os tipos e atribuir aos tecnologias existentes (Python e Django como Backend, HTML e CSS como Frontend, Git como Ferramenta).''',
                'erros_correcoes': '',
                'uso_ia': '',
            },
            {
                'titulo': 'Pagina Sobre',
                'entidade_relacionada': 'outro',
                'descricao': '''Criei a pagina /sobre/ que explica a aplicação. Tem 6 seções:

1. Arquitetura MVT com fotografia do desenho que fiz no caderno
2. Modelação com foto do DER em papel
3. Tecnologias listadas e agrupadas por tipo
4. Estrutura de navegação (mapa do site)
5. Repositorio GitHub
6. Making-Of com preview e link para a pagina completa

Para escrever a parte do MVT tive de pensar bem nas palavras:

Model = camada dos dados, define as tabelas
View = lógica, recebe pedidos, fala com models, devolve resposta
Template = HTML com placeholders preenchidos com dados

Fluxo: utilizador clica num link, Django identifica a rota, executa a view, a view consulta os models, passa dados ao template, devolve HTML.''',
                'erros_correcoes': 'A pagina ficou enorme com tudo dentro. Decidi separar o Making-Of numa pagina propria (/makingof/) e na pagina Sobre fica só um preview com as 5 entradas mais recentes. Fica mais limpo.',
                'uso_ia': '',
            },
            {
                'titulo': 'Integrar django-markdownify',
                'entidade_relacionada': 'outro',
                'descricao': '''Quis que as entradas do Making-Of tivessem formatação (titulos, listas, negrito) sem instalar um editor visual no admin.

A solução foi o django-markdownify. Escrevo em markdown num TextField normal e renderizo como HTML no template com o filtro {{ texto|markdownify }}.

Setup foi rápido: pip install, adicionar ao INSTALLED_APPS, configurar a whitelist de tags em settings.py, e {% load markdownify %} nos templates onde quero usar.

Markdown já conheço do GitHub e Discord por isso foi natural.''',
                'erros_correcoes': '',
                'uso_ia': 'O Claude Code sugeriu esta biblioteca quando descrevi o problema. Antes de instalar fui ver a documentação oficial em django-markdownify.readthedocs.io para confirmar.',
            },
            {
                'titulo': 'Reflexão da semana',
                'entidade_relacionada': 'outro',
                'descricao': '''Esta ficha foi bastante densa. CRUD com ModelForms e templates partilhados (base.html com blocks) são coisas que ficaram bem claras.

O que correu bem:
- Padrão MVT já faz sentido
- ModelForms reduzem imenso codigo
- Seguir o tutorial da biblioteca foi util como referencia

O que foi mais dificil:
- Saber quando usar request.POST vs request.FILES
- Manter a disciplina de documentar no Making-Of
- Pensar na modelação como algo que evolui

O que mais gostei foi perceber quão pouco codigo é preciso para ter um CRUD funcional. Comparado com escrever SQL e HTML do zero é muito menos trabalho.''',
                'erros_correcoes': '',
                'uso_ia': '',
            },
        ]

        for entrada in entradas:
            obj, created = MakingOf.objects.get_or_create(
                titulo=entrada['titulo'],
                defaults=entrada,
            )
            status = 'Criada' if created else 'Ja existe'
            self.stdout.write(f'{status}: {obj.titulo}')

        self.stdout.write(self.style.SUCCESS('\nEntradas do Making-Of carregadas.'))
