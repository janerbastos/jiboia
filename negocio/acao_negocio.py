#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone

from jiboia.forms.acao_forms import AcaoForm
from jiboia.negocio.abstract import Abstract
from jiboia.models import Acao
from jiboia.negocio.atividade_negocio import AtividadeNegocio
from jiboia.utils import contexto

class AcaoNegocio(Abstract):
    
    template = 'jiboia/index.html'


    def __init__(self, projeto_id, atividade_id, acao_id=None):
        self.projeto_id = projeto_id
        self.atividade_id = atividade_id
        self.acao_id = acao_id
    

    def get_object(self):
        try:
            return Acao.objects.get(id=self.acao_id)
        except Acao.DoesNotExist:
            return None
    

    def create(self, request):
        atividade = AtividadeNegocio(self.projeto_id, self.atividade_id).get_object()
        form = AcaoForm(request.POST or None, instance=None)
        is_save = False
        model = None
        if form.is_valid():
            model = form.save(commit=False)
            model.atividade = atividade
            model.criacao_at = timezone.now()
            model.save()
            is_save = True
        
        if request.is_ajax():
            html_string = render_to_string('jiboia/componentes/aux_ajax_form.html', {'form': form, 'opcao':'forms'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)

        if is_save:
            return redirect('jiboia:projetos', projeto_id=self.projeto_id)

        data = contexto.data(form, 'Ações', 'Nova ação.', None, None, 'acao', 'create' )
        return render(request, self.template, context=data)


    def update(self, request):
        acao = self.get_object()
        form = AcaoForm(request.POST or None, instance=acao)
        is_save = False
        model = None
        if form.is_valid():
            model = form.save(commit=False)
            model.save()
            is_save = True
        
        if request.is_ajax():
            html_string = render_to_string('jiboia/componentes/aux_ajax_form.html', {'form': form, 'opcao':'forms'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)

        if is_save:
            return redirect('jiboia:projetos', projeto_id=self.projeto_id)

        data = contexto.data(form, 'Ações', 'Atualizando ação.', None, None, 'acao', 'update' )
        return render(request, self.template, context=None)
    

    def delete(self, request):
        pass
    

    def list_all(self, request):
        atividade = AtividadeNegocio(self.projeto_id, self.atividade_id).get_object()
        acoes = Acao.objects.filter(atividade=atividade)

        if request.is_ajax():
            html_string = render_to_string('jiboia/componentes/aux_ajax_form.html', {'objects':  acoes, 'opcao': 'acoes-atividade'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)

        data = contexto.data(None, 'Ações', 'Lista de ações.', None, acoes, 'acao', 'list' )
        return render(request, self.template, context=None)


    def open_object(self, request):
        acao = self.get_object()

        if request.is_ajax():
            html_string = render_to_string('jiboia/componentes/aux_ajax_form.html', {'object':  acao, 'opcao': 'view-acao'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)

        data = contexto.data(None, 'Ações', 'Detalhes da ação.', acao, None, 'acao', 'open' )
        return render(request, self.template, context=None)