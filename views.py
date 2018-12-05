from django.shortcuts import render

from jiboia.controller.processador import Processador
# Create your views here.

def index(request):

    return Processador.controller(request, modulo='projeto', operador='@@create', oid=None)


def projetos(request, projeto_id=None, operador='@@open-object'):
    
    return Processador.controller(request, modulo='projeto', operador=operador,
                                    projeto_id=projeto_id)


def atividades(request, projeto_id, atividade_id=None):
    operador = request.GET.get('action', '@@create')
    return Processador.controller(request, modulo='atividade', operador=operador,
                                    projeto_id=projeto_id, atividade_id=atividade_id)


def acoes(request, projeto_id, atividade_id, acao_id=None):
    operador = request.GET.get('action', '@@create')
    return Processador.controller(request, modulo='acao', operador=operador,
                                    projeto_id=projeto_id, atividade_id=atividade_id, acao_id=acao_id)

    