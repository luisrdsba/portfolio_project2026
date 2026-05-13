from django.core.management.base import BaseCommand
from portfolio.models import MakingOf


class Command(BaseCommand):
    help = 'Carrega entradas do Making-Of relativas à Ficha 8'

    def handle(self, *args, **options):
        entradas = [
            {
                'titulo': 'Feedback do professor e ajustes à modelação',
                'entidade_relacionada': 'outro',
                'descricao': '''## Sessão de feedback

Durante a aula, tive oportunidade de discutir a modelação inicial com o professor. A conversa foi muito útil porque me obrigou a **justificar cada decisão** que tinha tomado.

### Pontos discutidos
- Estrutura geral das entidades e relações
- Necessidade de categorizar tecnologias
- Importância de documentar continuamente o processo

O feedback levou a uma revisão da modelação, especialmente no que diz respeito à organização das tecnologias.''',
                'erros_correcoes': '''**Problema identificado:** Inicialmente não existia uma forma de agrupar tecnologias por categoria. Tinha apenas o campo `categoria` como CharField com choices, o que limitava a flexibilidade.

**Solução implementada:** Criei a entidade `TipoTecnologia` com uma relação ForeignKey a partir de `Tecnologia`. Isto permite:
- Adicionar novos tipos sem alterar o código
- Associar uma descrição a cada tipo
- Filtrar e organizar tecnologias por categoria nas listagens

**Commit relacionado:** Adicionar entidade TipoTecnologia''',
                'uso_ia': 'Utilizei o Claude Code como apoio técnico para acelerar a implementação das migrações e atualização do script de carregamento de dados. Todas as decisões de modelação foram minhas, com base no feedback recebido.',
            },
            {
                'titulo': 'Implementação CRUD para Projetos',
                'entidade_relacionada': 'projeto',
                'descricao': '''## Operações CRUD com Django ModelForms

Implementei as quatro operações fundamentais para a entidade `Projeto`:
- **Create** — criação de novo projeto
- **Read** — listagem (já existia)
- **Update** — edição de projeto existente
- **Delete** — eliminação de projeto

### Decisão arquitetural
Optei por usar `ModelForm` do Django em vez de criar formulários HTML manuais. As vantagens são claras:

1. **Menos código** — o formulário é gerado automaticamente a partir do modelo
2. **Validação automática** — o Django valida os campos com base nas restrições do modelo
3. **Widgets adequados** — cada tipo de campo (CharField, ImageField, etc.) tem o widget HTML correto
4. **Manutenção fácil** — se adicionar um campo ao modelo, o formulário atualiza-se sozinho

### Estrutura criada
- `forms.py` — ProjetoForm como ModelForm
- Três views: `novo_projeto_view`, `edita_projeto_view`, `apaga_projeto_view`
- Templates `novo_projeto.html` e `edita_projeto.html`
- Botões "Inserir novo", "Editar" e "Apagar" na listagem''',
                'erros_correcoes': '''**Erro 1 — CSRF Token em falta:**
Ao submeter o primeiro formulário, recebi um erro 403 Forbidden. Faltava o `{% csrf_token %}` dentro do form. Corrigido facilmente, mas serviu para perceber a importância da proteção CSRF no Django.

**Erro 2 — Upload de imagens não funcionava:**
O ImageField não guardava os ficheiros enviados. Descobri que faltava `enctype="multipart/form-data"` no elemento form e `request.FILES` na criação do form na view.

**Erro 3 — Edição perdia a imagem existente:**
Ao editar um projeto sem alterar a imagem, a imagem era removida. Resolvido garantindo que o ModelForm recebe `request.FILES` mesmo quando vazio.''',
                'uso_ia': 'Utilizei o Claude Code para gerar a estrutura inicial das views e templates, seguindo o padrão do tutorial da biblioteca da Lusófona disponibilizado pelo professor. Revi cada linha do código gerado para garantir que compreendo o fluxo completo: request → form → validação → save → redirect.',
            },
            {
                'titulo': 'Extensão CRUD às restantes entidades',
                'entidade_relacionada': 'tecnologia',
                'descricao': '''## Aplicação do princípio DRY

Após implementar o CRUD para `Projeto`, repliquei o mesmo padrão para:
- **Tecnologia**
- **Competencia**
- **Formacao**

### O que aprendi
O **princípio DRY (Don't Repeat Yourself)** ganha sentido prático quando se replica o mesmo padrão várias vezes. Notei que:

- A consistência da abordagem torna o código previsível
- Quem ler o código consegue intuir como funcionam outras partes
- A manutenção é mais simples (corrige-se um padrão, corrige-se em todos)

Em projetos maiores, este tipo de repetição seria abstraído em **Class-Based Views** ou **generic views**, mas para esta fase de aprendizagem, escrever as views explicitamente ajuda a compreender o que está a acontecer.''',
                'erros_correcoes': '''**Dificuldade com campos ManyToMany:**
Os campos `ManyToManyField` (como `tecnologias` no Projeto) não apareciam de forma user-friendly nos formulários — apareciam como caixa de seleção múltipla básica.

**Possível melhoria futura:** usar widgets como `CheckboxSelectMultiple` ou bibliotecas como `django-select2` para melhorar a experiência. Por agora mantive o widget padrão para focar na funcionalidade.''',
                'uso_ia': 'O Claude Code foi muito útil para replicar rapidamente o padrão sem erros de copy-paste. Verifiquei manualmente cada view e URL para garantir que os nomes estão consistentes.',
            },
            {
                'titulo': 'Adição da entidade TipoTecnologia',
                'entidade_relacionada': 'tecnologia',
                'descricao': '''## Iteração na modelação

Esta foi uma alteração importante e mostra como **a modelação é um processo iterativo**. Não chega pensar uma vez — à medida que implementamos, surgem oportunidades de melhoria.

### O que mudou
- Nova entidade `TipoTecnologia` com `nome` e `descricao`
- Campo `tipo` adicionado a `Tecnologia` como ForeignKey para `TipoTecnologia`
- Permite agora agrupar tecnologias por: Frontend, Backend, Base de Dados, Storage, Ferramenta de Desenvolvimento

### Porque ForeignKey e não CharField com choices?
Considerei manter o campo como `CharField` com `choices`, mas a ForeignKey traz vantagens:
- Os tipos ficam na base de dados (podem ter descrição própria)
- Posso adicionar novos tipos pelo admin sem alterar código
- Permite estatísticas (quantas tecnologias por tipo, etc.)''',
                'erros_correcoes': '''**Migração com dados existentes:**
A primeira tentativa de migração falhou porque já existiam tecnologias na base de dados e o campo `tipo` era obrigatório. Resolvi tornando o campo `null=True, blank=True`, permitindo que tecnologias existentes ficassem sem tipo até serem atualizadas manualmente.''',
            },
            {
                'titulo': 'Criação da página Sobre',
                'entidade_relacionada': 'outro',
                'descricao': '''## Compreensão do padrão MVT

A criação da página Sobre obrigou-me a **explicar por palavras minhas** o padrão MVT do Django. Este exercício foi muito útil para consolidar o conhecimento.

### A minha compreensão

**Model** — A camada de dados. Define como a informação é estruturada na base de dados. Cada classe Python que herda de `models.Model` representa uma tabela.

**View** — A lógica de negócio. Recebe um pedido HTTP, decide o que fazer (consultar a base de dados, processar formulários, etc.), e devolve uma resposta.

**Template** — A apresentação. Ficheiros HTML que recebem dados da View e renderizam uma página para o utilizador.

### Fluxo completo
1. O utilizador faz um pedido (clica num link)
2. O URL dispatcher do Django identifica que View executar
3. A View consulta os Models necessários
4. A View passa os dados ao Template
5. O Template é renderizado em HTML
6. O HTML é devolvido ao utilizador

### Conteúdo da página Sobre
- Arquitetura MVT (com fotografia do diagrama desenhado à mão)
- Modelação (com DER em papel)
- Tecnologias agrupadas por tipo
- Mapa de navegação
- Link para o GitHub
- Preview do Making-Of''',
                'erros_correcoes': '''**Decisão sobre organização do conteúdo:**
A página Sobre tinha muito conteúdo. Inicialmente coloquei tudo na mesma página, incluindo o Making-Of completo, mas ficou demasiado longa. Decidi:
- Deixar apenas as 5 entradas mais recentes do Making-Of na página Sobre
- Criar uma página separada `/makingof/` com todas as entradas

Esta separação melhorou a legibilidade e respeita o princípio de cada página ter um propósito claro.''',
            },
            {
                'titulo': 'Integração de django-markdownify',
                'entidade_relacionada': 'outro',
                'descricao': '''## Permitir formatação rica no Making-Of

Para que as entradas do Making-Of pudessem ter formatação rica (títulos, listas, negrito, etc.) sem complicar o admin com editores visuais, instalei a biblioteca `django-markdownify`.

### Como funciona
1. Guardo o texto em **markdown** num `TextField` normal
2. No template, uso o filtro `{{ texto|markdownify }}` que converte markdown para HTML
3. Configuro em `settings.py` que tags HTML são permitidas (whitelist)

### Vantagens
- Não preciso de editores complexos no admin
- Posso escrever markdown facilmente (familiar de GitHub, Discord, etc.)
- O HTML gerado é seguro (whitelist controlada)
- Funciona em qualquer TextField, em qualquer template

### Passos de integração
1. `pip install django-markdownify`
2. Adicionar `markdownify.apps.MarkdownifyConfig` aos INSTALLED_APPS
3. Configurar `MARKDOWNIFY` com a whitelist de tags
4. Em cada template, `{% load markdownify %}` e usar o filtro''',
                'uso_ia': 'O Claude Code sugeriu esta biblioteca quando descrevi o problema (queria formatação rica sem complicar a interface admin). Validei a sugestão consultando a documentação oficial em django-markdownify.readthedocs.io antes de integrar.',
            },
            {
                'titulo': 'Reflexão geral da Ficha 8',
                'entidade_relacionada': 'outro',
                'descricao': '''## O que esta semana me ensinou

### Pontos fortes
- **Compreensão sólida do padrão MVT** — já não é um conceito abstrato
- **Domínio dos ModelForms** — perceber o quanto reduzem código repetitivo
- **Importância de seguir convenções** — o tutorial da biblioteca foi referência clara
- **Iteração na modelação** — perceber que o design da base de dados evolui com o projeto

### Dificuldades
- Inicialmente confundi quando usar `request.POST` vs `request.FILES`
- A disciplina de documentar continuamente no Making-Of exige esforço consciente
- Decidir o nível de abstração certo (quando repetir, quando generalizar)

### O que mais gostei
A forma como o Django **reduz drasticamente o código necessário** para CRUD completo. Comparando com escrever SQL e HTML do zero, é uma diferença abismal. Em meia dúzia de linhas, tenho:
- Validação de formulários
- Conversão de tipos
- Proteção contra SQL injection
- Proteção CSRF
- Geração de HTML

Faz sentido porque é que o Django é tão popular para desenvolvimento web rápido.

### O que vou explorar a seguir
- Class-Based Views como evolução das function-based views
- Personalização de formulários (widgets, validators custom)
- Sistema de autenticação para proteger views CRUD''',
                'uso_ia': '''## Reflexão honesta sobre o uso de IA

Utilizei o Claude Code de forma consistente ao longo desta ficha, principalmente para:
- **Acelerar implementação** de padrões repetitivos (CRUD em múltiplas entidades)
- **Validar abordagens** antes de implementar
- **Esclarecer dúvidas técnicas** específicas (parâmetros de funções, sintaxe do Django)

**O que a IA *não* fez:**
- Não tomou decisões de modelação por mim — essas foram minhas com base no enunciado e feedback
- Não escolheu a estrutura da página Sobre — fui eu que defini o que era importante incluir
- Não escreveu as reflexões do Making-Of — estas refletem o meu processo real

**Aprendizagens sobre usar IA responsavelmente:**
- Validar sempre o código gerado linha a linha
- Comparar sugestões com documentação oficial
- Garantir que consigo explicar tudo o que está no código

Acredito que o uso transparente e crítico de ferramentas de IA faz parte do trabalho de um desenvolvedor moderno, desde que não substitua a compreensão.''',
            },
        ]

        for entrada in entradas:
            obj, created = MakingOf.objects.get_or_create(
                titulo=entrada['titulo'],
                defaults=entrada,
            )
            status = 'Criada' if created else 'Já existe'
            self.stdout.write(f'{status}: {obj.titulo}')

        self.stdout.write(self.style.SUCCESS('\nEntradas do Making-Of da Ficha 8 carregadas com sucesso.'))
