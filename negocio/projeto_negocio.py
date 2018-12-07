#-*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils import timezone

from jiboia.negocio.abstract import Abstract
from jiboia.models import Projeto
from jiboia.forms.projeto_forms import ProjetoCreateForm
from jiboia.utils import contexto


class ProjetoNegocio(Abstract):

    template = 'jiboia/index.html'

    def __init__(self, projeto_id=None):
        self.projeto_id = projeto_id

    
    def get_object(self):
        try:
            return Projeto.objects.get(id=self.projeto_id)
        except Projeto.DoesNotexist:
            return None 


    def create(self, request):
        form = ProjetoCreateForm(request.POST or None, instance=None)
        model = None
        user = request.user
        is_save = False
        if form.is_valid():
            model = form.save(commit=False)
            model.criacao_at = timezone.now()
            model.usuario = user
            model.save()
            is_save = True
    
        if is_save:
            return redirect('jiboia:index')
        data = contexto.data(form, 'Projeto', 'Criando novo peojeto', None, None, 'projeto', 'create')
        return render(request, self.template, context=data)


    def update(self, resquet):
        pass


    def open_object(self, request):
        projeto = self.get_object()
        data = contexto.data(None, projeto.nome, projeto.descricao, projeto, None, 'projeto', 'open')
        return render(request, self.template, context=data)
    
    
    def list_all(self, request):
        pass