#-*- coding: utf-8 -*-

from django import forms
from jiboia.models import BlocoNota

class NotaForm(forms.ModelForm):

    class Meta:
        model = BlocoNota
        fields = ['nota', 'status']
        labels = {
            'nota': 'Conteúdo',
            'status': 'Processada' 
        }

