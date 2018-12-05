#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html

# Create your models here.

CHOICE_WORKSPACE_ATIVIDADE = (
    ('a-fazer', 'A Fazer'),
    ('desenvolvimento', 'Desenvolvimento'),
    ('concluido', 'Concluido'),
    ('cancelado', 'Cancelado')
)


class Projeto(models.Model):
    """
    Essa classe armazena as informeções gerais dos projetos,
    possui um relacinamento com ativdade e membro isso significa que
    uma ou mais instancias dessa classe complementa suas informações.
    """
    nome = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    criacao_at = models.DateTimeField(auto_created=True)
    inicio_at = models.DateField(null=True, blank=True)
    termino_at = models.DateField(null=True, blank=True)
    executado = models.PositiveIntegerField()
    status = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.nome


    @property
    def content_type(self):
        return 'at_projeto'


    @property
    def is_status(self):
        if status:
            return 'Bloqueado'
        return 'Em produção'


class Atividade(models.Model):
    """
    Essa classe representa as atividades de em um projeto.
    possui um relacionamento de agregação com as class ações e que
    podem produzir uma serie de artefatos que contempla suas informções.
    """
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='atividades_deste')
    prioridade = models.PositiveIntegerField(default=1)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    inicio_at = models.DateField(null=True, blank=True)
    termino_at = models.DateField(null=True, blank=True)
    criacao_at = models.DateTimeField(auto_created=True)
    workflow = models.CharField(max_length=30, choices=CHOICE_WORKSPACE_ATIVIDADE, default='a-fazer')
    notas = models.ManyToManyField('BlocoNota', blank=True)
    artefatos = models.ManyToManyField('Artefato', blank=True)


    @property
    def tolltip(self):
        html_tag = '%s\n%s' % (self.nome, self.descricao)
        return format_html(html_tag)
    

    @property
    def producao(self):
        concuidos = self.acoes_desta.filter(status=True).count()
        aguardando = self.acoes_desta.filter(status=False).count()
        if not aguardando:
            return '100.0'
        
        total = concuidos + aguardando
        total = (concuidos*100)/total
        return ('%s') % round(total,0)



class Acao(models.Model):
    """
    Essa class representa as ações tomadas por um atividade,
    """
    atividade = models.ForeignKey('Atividade',  on_delete=models.CASCADE, related_name='acoes_desta')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    criacao_at = models.DateTimeField(auto_created=True)
    inicio_at = models.DateField(null=True, blank=True)
    termino_at = models.DateField(null=True, blank=True)
    prioridade = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=False)


    @property
    def tolltip(self):
        html_tag = '%s\n%s' % (self.nome, self.descricao)
        return format_html(html_tag)
    

    @property
    def is_status(self):
        if self.status:
            return '[Finalizado]'
        return '[Aguardando]'
    

    def get_absolute_url(self):
        return '/jiboia/projetos/%s/atividades/%s/acoes/%s/' % (self.atividade.projeto.id, self.atividade.id, self.id)



class Artefato(models.Model):
    """
    Essa classe representa um documento produzido durante as fazes do projeto
    em suas atividades em função de alguma ação especifica.
    """
    nome = models.CharField(max_length=200)
    criacao_at = models.DateTimeField(auto_created=True)
    arquivo = models.FileField(upload_to='jiboia-doc/artefatos/')

    @property
    def tolltip(self):
        html_tag = '%s' % (self.nome)
        return format_html(html_tag)


class BlocoNota(models.Model):
    """
    Essa classe representa as anotações produzidas nas fase do projeto providadas
    de uma atividade ou ação.
    """
    nota = models.TextField()
    criacao_at = models.DateTimeField(auto_created=True)
    status = models.BooleanField(default=False)


#Classes de modelo de controle

class Papel(models.Model):
    """
    Essa class representa uma permissão especifica,
    exercido por um membro ou grupo.
    """
    nome = models.CharField(max_length=30)


class Grupo(models.Model):
    """
    Essa class representa um grupo contendo uma ou muitos papeis,
    representada pelo relacinamento com papeis. 
    """
    nome = models.CharField(max_length=20)
    papeis = models.ManyToManyField('Papel', blank=True)


class Membro(models.Model):
    """
    Essa class representa um membro de um projeto,
    esta relacionado com um ou mais grupos
    ou pode possuir um papel especifico para um determinado
    projeto.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='membros_deste')
    grupos = models.ManyToManyField('Grupo', blank=True)
    papeis = models.ManyToManyField('Papel', blank=True)
    criacao_at = models.DateTimeField(auto_created=True)