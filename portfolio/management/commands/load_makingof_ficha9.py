from django.core.management.base import BaseCommand
from portfolio.models import MakingOf


class Command(BaseCommand):
    help = 'Carrega entradas do Making-Of da Ficha 9'

    def handle(self, *args, **options):
        entradas = [
            {
                'titulo': 'Autenticação por username e password',
                'entidade_relacionada': 'outro',
                'descricao': '''Criei a app accounts com as views de login, logout e registo. Usei o UserCreationForm do Django como base e adicionei o email como campo obrigatório no registo.

A logica de login usa as funções authenticate() e login() do Django. Se as credenciais sao validas redireciona para os projetos, caso contrario mostra mensagem de erro.

No registo, quando um utilizador é criado, ele é automaticamente adicionado ao grupo "autores" para poder publicar artigos.''',
                'erros_correcoes': 'A primeira tentativa de login deu erro 404 porque tinha a URL errada no LOGIN_URL do settings. Corrigi para "/accounts/login/" e ficou.',
                'uso_ia': '',
            },
            {
                'titulo': 'Grupos e permissoes',
                'entidade_relacionada': 'outro',
                'descricao': '''Criei dois grupos: "gestor-portfolio" e "autores".

O gestor-portfolio tem permissoes para todos os modelos do portfolio (criar, editar, apagar, ver Projetos, Tecnologias, etc).

O grupo autores so tem permissoes para o modelo Artigo.

Para automatizar isto fiz um management command setup_grupos que cria os grupos e atribui as permissoes. Tambem cria um utilizador "gestor" para testar.

Os botões de editar/apagar/criar nas paginas de projetos, tecnologias, competencias e formacoes so aparecem se o utilizador estiver autenticado e for do grupo gestor-portfolio. Tambem usei @login_required nas views como camada extra de segurança.''',
                'erros_correcoes': '',
                'uso_ia': '',
            },
            {
                'titulo': 'Magic Link',
                'entidade_relacionada': 'outro',
                'descricao': '''Implementei autenticação por magic link como alternativa ao login com password.

Funciona assim: utilizador insere o email, é gerado um token aleatorio guardado na base de dados, e é enviado um email com o link para autenticar. O link tem validade de 15 minutos e so pode ser usado uma vez.

Para desenvolvimento usei o EMAIL_BACKEND console, que imprime os emails no terminal em vez de enviar realmente. Em produção bastaria mudar o backend para SMTP real.

Por questões de segurança, a view nao revela se o email existe ou nao. Mostra sempre a mesma mensagem generica.''',
                'erros_correcoes': '''Tive um bug chato com os tokens. Inicialmente usei secrets.token_urlsafe(), que gera tokens com caracteres "=" no fim. Quando o email era impresso no terminal, o link era partido em duas linhas e o "=" ficava no fim da primeira linha. Ao copiar perdia caracteres.

Resolvi criando o token manualmente com secrets.choice() apenas com letras e digitos, sem caracteres especiais.''',
                'uso_ia': '',
            },
            {
                'titulo': 'App Artigos',
                'entidade_relacionada': 'outro',
                'descricao': '''Criei uma nova app artigos para publicação de conteudos.

Modelo Artigo com: titulo, texto, fotografia, link externo, data de criação e autor (ForeignKey para User).

Fiz CRUD completo mas com regras de permissão:
- Qualquer pessoa pode ver os artigos
- So utilizadores do grupo "autores" podem criar
- Cada autor so pode editar/apagar os seus proprios artigos

A verificação "artigo.autor == request.user" garante isto na view. No template, os botões de editar/apagar so aparecem se o utilizador for o autor.''',
                'erros_correcoes': '',
                'uso_ia': '',
            },
            {
                'titulo': 'Likes e Comentarios',
                'entidade_relacionada': 'outro',
                'descricao': '''Adicionei duas funcionalidades sociais aos artigos.

Likes: qualquer pessoa pode dar gosto, mesmo sem estar autenticada. Para evitar likes duplicados da mesma pessoa, uso a session_key como identificador. Cada sessão so pode dar like uma vez por artigo (graças ao unique_together no modelo).

Comentarios: so utilizadores autenticados podem comentar. Os comentarios ficam visiveis para toda a gente debaixo do artigo, ordenados por data.

Usei ForeignKey para ligar tanto Like como Comentario ao Artigo, com related_name para conseguir aceder facilmente como artigo.likes.count() ou artigo.comentarios.all() no template.''',
                'erros_correcoes': 'Para o sistema de likes funcionar tive de garantir que a sessão era criada antes de tentar usar a session_key. Adicionei request.session.create() se a chave nao existisse.',
                'uso_ia': 'O Claude Code ajudou a estruturar o modelo de likes com a logica de unique_together por sessão, que nao tinha pensado.',
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
