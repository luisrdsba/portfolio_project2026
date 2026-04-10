from django.db import models


class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    ano_inicio = models.IntegerField()
    ano_fim = models.IntegerField(null=True, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='licenciatura/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} — {self.instituicao}"

    class Meta:
        verbose_name_plural = "Licenciaturas"


class Docente(models.Model):
    nome = models.CharField(max_length=200)
    pagina_lusofona = models.URLField(blank=True, verbose_name="Página na Lusófona")
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Docentes"


class UnidadeCurricular(models.Model):
    SEMESTRE_CHOICES = [
        (0, 'Anual'),
        (1, '1º Semestre'),
        (2, '2º Semestre'),
    ]

    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20, blank=True)
    ano = models.IntegerField(verbose_name="Ano curricular")
    semestre = models.IntegerField(choices=SEMESTRE_CHOICES)
    ects = models.IntegerField(verbose_name="Créditos ECTS")
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='unidades_curriculares/', blank=True, null=True)
    licenciatura = models.ForeignKey(
        Licenciatura, on_delete=models.CASCADE, related_name='unidades_curriculares'
    )
    docentes = models.ManyToManyField(Docente, blank=True, related_name='unidades_curriculares')

    def __str__(self):
        return f"{self.sigla} — {self.nome}" if self.sigla else self.nome

    class Meta:
        verbose_name = "Unidade Curricular"
        verbose_name_plural = "Unidades Curriculares"
        ordering = ['ano', 'semestre', 'nome']


class Tecnologia(models.Model):
    CATEGORIA_CHOICES = [
        ('linguagem', 'Linguagem de Programação'),
        ('framework', 'Framework'),
        ('base_dados', 'Base de Dados'),
        ('ferramenta', 'Ferramenta'),
        ('devops', 'DevOps / Infraestrutura'),
        ('outro', 'Outro'),
    ]

    NIVEL_CHOICES = [
        (1, 'Iniciante'),
        (2, 'Básico'),
        (3, 'Intermédio'),
        (4, 'Avançado'),
        (5, 'Especialista'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='outro')
    descricao = models.TextField(blank=True)
    logo = models.ImageField(upload_to='tecnologias/', blank=True, null=True)
    website_oficial = models.URLField(blank=True)
    nivel_interesse = models.IntegerField(
        choices=NIVEL_CHOICES, default=3,
        verbose_name="Nível de interesse / proficiência"
    )
    destaque = models.BooleanField(default=False, verbose_name="Tecnologia em destaque")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Tecnologias"
        ordering = ['-destaque', 'nome']


class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    uc = models.ForeignKey(
        UnidadeCurricular, on_delete=models.CASCADE,
        related_name='projetos', verbose_name="Unidade Curricular"
    )
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='projetos')
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    video_demo = models.URLField(blank=True, verbose_name="Vídeo demo")
    repositorio_github = models.URLField(blank=True, verbose_name="Repositório GitHub")
    conceitos_aplicados = models.TextField(
        blank=True, verbose_name="Conceitos aplicados da UC"
    )
    data_conclusao = models.DateField(null=True, blank=True, verbose_name="Data de conclusão")
    destaque = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Projetos"
        ordering = ['-destaque', '-data_conclusao']


class TFC(models.Model):
    TIPO_CHOICES = [
        ('licenciatura', 'Trabalho Final de Licenciatura'),
        ('mestrado', 'Dissertação de Mestrado'),
        ('outro', 'Outro'),
    ]

    titulo = models.CharField(max_length=300)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='licenciatura')
    autor = models.CharField(max_length=200)
    orientador = models.CharField(max_length=200, blank=True)
    ano = models.IntegerField()
    resumo = models.TextField(blank=True)
    palavras_chave = models.CharField(max_length=300, blank=True, verbose_name="Palavras-chave")
    link = models.URLField(blank=True, verbose_name="Link para o TFC")
    destaque = models.BooleanField(default=False, verbose_name="TFC em destaque")
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='tfcs')

    def __str__(self):
        return f"{self.titulo} ({self.ano})"

    class Meta:
        verbose_name = "TFC"
        verbose_name_plural = "TFCs"
        ordering = ['-destaque', '-ano']


class Competencia(models.Model):
    TIPO_CHOICES = [
        ('tecnica', 'Técnica'),
        ('soft', 'Soft skill'),
        ('linguistica', 'Linguística'),
        ('outra', 'Outra'),
    ]

    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='tecnica')
    descricao = models.TextField(blank=True)
    nivel = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=3,
        verbose_name="Nível (1-5)"
    )
    projetos = models.ManyToManyField(Projeto, blank=True, related_name='competencias')
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='competencias')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Competências"
        ordering = ['tipo', 'nome']


class Formacao(models.Model):
    TIPO_CHOICES = [
        ('academica', 'Académica'),
        ('curso', 'Curso / Formação'),
        ('certificacao', 'Certificação'),
        ('workshop', 'Workshop'),
        ('outro', 'Outro'),
    ]

    titulo = models.CharField(max_length=300)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='curso')
    instituicao = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateField(verbose_name="Data de início")
    data_fim = models.DateField(null=True, blank=True, verbose_name="Data de conclusão")
    certificado = models.FileField(upload_to='formacoes/certificados/', blank=True, null=True)
    link = models.URLField(blank=True)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='formacoes')

    def __str__(self):
        return f"{self.titulo} — {self.instituicao}"

    class Meta:
        verbose_name = "Formação"
        verbose_name_plural = "Formações"
        ordering = ['-data_inicio']


class MakingOf(models.Model):
    ENTIDADE_CHOICES = [
        ('licenciatura', 'Licenciatura'),
        ('unidade_curricular', 'Unidade Curricular'),
        ('projeto', 'Projeto'),
        ('tecnologia', 'Tecnologia'),
        ('tfc', 'TFC'),
        ('competencia', 'Competência'),
        ('formacao', 'Formação'),
        ('outro', 'Outro'),
    ]

    titulo = models.CharField(max_length=300)
    entidade_relacionada = models.CharField(
        max_length=50, choices=ENTIDADE_CHOICES, default='outro',
        verbose_name="Entidade relacionada"
    )
    descricao = models.TextField(
        verbose_name="Descrição / Decisões tomadas"
    )
    fotografia = models.ImageField(
        upload_to='makingof/', blank=True, null=True,
        verbose_name="Fotografia (caderno / DER / esquema)"
    )
    erros_correcoes = models.TextField(
        blank=True, verbose_name="Erros encontrados e correções"
    )
    uso_ia = models.TextField(
        blank=True,
        verbose_name="Uso de ferramentas de IA (se aplicável)"
    )
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_entidade_relacionada_display()})"

    class Meta:
        verbose_name = "Making Of"
        verbose_name_plural = "Making Of"
        ordering = ['-data']
