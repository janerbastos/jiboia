#-*- coding: utf-8 -*-

from django import forms
from jiboia.models import Atividade


class AtividadeCreateForm(forms.ModelForm):

    class Meta:
        model = Atividade
        fields = ['nome', 'descricao', 'inicio_at', 'termino_at']
        labels = {
            'nome': 'Atividade:',
            'descricao': 'Descrição:',
            'inicio_at': 'Início:',
            'termino_at': 'Temino:',
        }
        help_texts = {
            'nome': 'Informe um nome para essa atividade.',
            'descricao': 'Porque essa atividade deve ser realizad?',
             'inicio_at': 'Previsão para iniciar a atividade.',
            'termino_at': 'Previsão para encerrar aa atividade.',
        }


class AtividadeStarForm(forms.ModelForm):

    class Meta:
        model = Atividade
        fields = ['inicio_at', 'termino_at', ]
        labels ={
            'inicio_at': 'Início:',
            'termino_at': 'Temino:',
            'inicio_at': 'Previsão para iniciar a atividade.',
            'termino_at': 'Previsão para encerrar aa atividade.',
        }
        help_texts = {
            'inicio_at': 'Previsão para iniciar a atividade.',
            'termino_at': 'Previsão para encerrar aa atividade.',
        }
