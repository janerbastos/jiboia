#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.utils.html import format_html
from django.template.loader import render_to_string

from jiboia.forms.atividade_forms import AtividadeCreateForm, AtividadeStarForm
from jiboia.negocio.abstract import Abstract
from jiboia.negocio.projeto_negocio import ProjetoNegocio
from jiboia.models import Atividade

from jiboia.utils import contexto

class AtividadeNegocio(Abstract):

    template = 'jiboia_layout/index.html'

    def __init__(self, projeto_id, atividade_id):
        self.projeto_id = projeto_id
        self.atividade_id = atividade_id

    
    def get_object(self):
        try:
            return Atividade.objects.get(id=self.atividade_id)
        except Atividade.DoesNotExist:
            return None


    def create(self, request):
        projeto = ProjetoNegocio(self.projeto_id).get_object()
        form = AtividadeCreateForm(request.POST or None)
        model = None
        is_save = False
        if form.is_valid():
            model = form.save(commit=False)
            model.projeto = projeto
            model.criacao_at = timezone.now()
            model.save()
            is_save = True
        
        if request.is_ajax():
            html_string = render_to_string('jiboia_layout/componentes/aux_ajax_form.html', {'form': form, 'opcao':'forms'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)

        if is_save:
            return redirect('jiboia:projetos', projeto_id=projeto.id)

        data = contexto.data(form, 'Atividade', 'Nova atividade', None, None, 'atividade', 'create' )
        return render(request, self.template, context=data)


    def update(self, request):

        atividade = self.get_object()
        form = AtividadeCreateForm(request.POST or None, instance=atividade)
        model = None
        is_save = False

        if request.is_ajax():
            html_string = render_to_string('jiboia_layout/componentes/aux_ajax_form.html', {'form': form, 'opcao':'forms'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)

        if form.is_valid():
            model = form.save(commit=False)
            model.save()
            is_save = True
        
        
        if is_save:
            return redirect('jiboia:projetos', projeto_id=self.projeto_id)
        
        data = contexto.data(form, 'Atividade', 'Iniciacializando atividade', atividade, None, 'atividade', 'update' )
        return render(request, self.template, context=data)


    def open_object(self, request):
        atividade = self.get_object()
        
        if request.is_ajax():
            acoes = atividade.acoes_desta.all()
            html_string = render_to_string('jiboia_layout/componentes/aux_ajax_form.html', {'object': atividade, 'acoes': acoes, 'opcao':'view-atividade'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)
        data = contexto.data(None, 'Atividade', 'Detalhes da atividade', atividade, None, 'atividade', 'open' )
        return render(request, self.template, context=data)

    
    def __start_atividade(self, request):
        atividade = self.get_object()
        model = None
        is_save = False
        
        form = AtividadeStarForm(request.POST or None, instance=atividade)

        if request.is_ajax():
            html_string = render_to_string('jiboia_layout/componentes/aux_ajax_form.html', {'form': form, 'opcao':'forms'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)
        
        if request.method=='POST':
            if form.is_valid():
                model = form.save(commit=False)
                model.workflow = 'desenvolvimento'
                model.save()
                is_save = True
        
        if is_save:
            return redirect('jiboia:projetos', projeto_id=self.projeto_id)
    

    def workflow(self, request):
        atividade = self.get_object()

        if atividade.workflow == 'a-fazer':
            return self.__start_atividade(request)
        
        if request.method=='POST':
            w_flow = request.POST.get('workflow', None)
            atividade.workflow = w_flow
            atividade.save()
            return redirect('jiboia:projetos', projeto_id=self.projeto_id)
        

        if request.is_ajax():
            html_string = render_to_string('jiboia_layout/componentes/aux_ajax_form.html', {'object': atividade, 'opcao':'workflow'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)


    def delete(self, request):
        pass