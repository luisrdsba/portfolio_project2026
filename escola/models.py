from django.db import models


class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'professores'


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    numero = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.nome} ({self.numero})'

    class Meta:
        verbose_name_plural = 'alunos'


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='cursos/')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='cursos')
    alunos = models.ManyToManyField(Aluno, related_name='cursos')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'cursos'
