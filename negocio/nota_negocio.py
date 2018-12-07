#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.template.loader import render_to_string

from jiboia.negocio.abstract import Abstract
from jiboia.models import BlocoNota
from jiboia.forms.nota_forms import NotaForm
from jiboia.negocio.atividade_negocio import AtividadeNegocio
from jiboia.utils import contexto

class NotaNegocio(Abstract):

    template = 'jiboia/index.html'

    def __init__(self, projeto_id, atividade_id, nota_id=None):
        self.projeto_id = projeto_id
        self.atividade_id = atividade_id
        self.nota_id = nota_id
   

    def get_object(self):
        try:
            return BlocoNota.objects.get(id=self.nota_id)
        except:
            return None
    

    def create(self, request):
        atividade = AtividadeNegocio(self.projeto_id, self.atividade_id).get_object()
        
        form = NotaForm(request.POST or None, instance=None)
        model = None
        is_save = False
        if form.is_valid():
            model = form.save(commit=False)
            model.criacao_at = timezone.now()
            model.save()
            atividade.notas.add(model.id)
            is_save = True
            form = NotaForm()

        if request.is_ajax():
            html_string = render_to_string('jiboia/paginas/nota.html', {'form': form, 'action':'ajax'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)
        
        if is_save:
            return redirect('jiboia:projetos', projeto_id=self.projeto_id)
        data = contexto.data(form, 'Nota', 'Bloco de notas', None, None, 'nota', 'create')
        return render(request, self.template, context=data)


    def update(self, request):
        nota = self.get_object()
        form = NotaForm(request.POST or None, instance=nota)
        model = None
        is_save = False
        if form.is_valid():
            model = form.save(commit=False)
            model.save()
            is_save = True
            form = NotaForm()

        if request.is_ajax():
            html_string = render_to_string('jiboia/paginas/nota.html', {'form': form, 'action':'ajax'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)
        
        if is_save:
            return redirect('jiboia:projetos', projeto_id=self.projeto_id)
        data = contexto.data(form, 'Nota', 'Bloco de notas', None, None, 'nota', 'create')
        return render(request, self.template, context=data)
    

    def list_all(self, request):
        atividade = AtividadeNegocio(self.projeto_id, self.atividade_id).get_object()
        notas = atividade.notas.all()
        if request.is_ajax():
            html_string = render_to_string('jiboia/paginas/nota.html',
                {'objects': notas, 'projeto_id': self.projeto_id, 'atividade_id': self.atividade_id, 'action':'ajax'})
            data = {
                'result': html_string,
            }
            return JsonResponse(data)
        data = contexto.data(None, 'Notas', 'Notas desta atividade', None, notas, 'nota', 'listar')
        return render(request, self.template, context=data)


    def open_object(self, request):
        nota = self.get_object()
        if request.is_ajax():
            pass
        data = contexto.data(None, 'Nota', '', nota, None, 'nota', 'open')
        return render(request, self.template, context=data)