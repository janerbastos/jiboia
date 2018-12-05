#-*- coding: utf-8 -*-

from django import forms
from jiboia.models import Projeto

class ProjetoCreateForm(forms.ModelForm):

    class Meta:
        model = Projeto
        fields = ['nome', 'descricao', 'inicio_at', 'termino_at', 'executado']
        labels = {
            'nome': 'Nome do projeto',
            'descricao': 'Resumo',
            'inicio_at': 'Início',
            'termino_at': 'Termino',
            'executado': 'Executado',
        }
        help_texts = {
            'nome': 'Oque deve ser feito?',
            'descricao': 'Por que este projeto deve ser realizada?',
            'inicio_at': 'Quando você pretende iniciar? Já iniciou quando?',
            'termino_at': 'Quando você pretende terminar? Já concluiu quando?',
            'executado': 'Quanto você já concluiu? Já conclui? (em %)'
        }