#-*- coding: utf-8 -*-
from django import forms

from jiboia.models import Acao

class AcaoForm(forms.ModelForm):

    class Meta:
        model = Acao
        fields = ['nome', 'descricao', 'status', ]
        labels = {
            'nome': 'Nome:',
            'descricao': 'Descrição:',
            'status': 'Finalizada'
        }
        help_text = {
            'descricao': 'Porque devo executar essa ação.'
        }