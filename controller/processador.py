#-*- coding: utf-8 -*-

from jiboia.negocio.projeto_negocio import ProjetoNegocio
from jiboia.negocio.atividade_negocio import AtividadeNegocio
from jiboia.negocio.acao_negocio import AcaoNegocio

class Processador():

    """
    Classe processdora da camada de controlle, responsabilidade controlar as requições
    para camanda de negocio.
    """

    @staticmethod
    def __methodo(**kwargs):
        
        methodo = {
            'projeto': ProjetoNegocio(kwargs.get('projeto_id', None)),
            'atividade': AtividadeNegocio(kwargs.get('projeto_id', None), kwargs.get('atividade_id', None)),
            'nota': "NotaNegocio(kwargs.get('projeto_id', None), kwargs.get('atividade_id', None), kwargs.get('nota_id'))",
            'acao': AcaoNegocio(kwargs.get('projeto_id', None), kwargs.get('atividade_id', None), kwargs.get('acao_id'))
        }

        return methodo


    @staticmethod
    def controller(request, **kwargs):
        
        #Inicia o processador
        executor = Processador.__methodo( **kwargs)
        

        operador = kwargs.get('operador', None)
        modulo = kwargs.get('modulo', None)

        #Somente na fase desenvolvimento
        print('\n', 'Modulo: ', modulo, '\n', 'Operador: ', operador, '\n')


        if operador in ['@@create']:
            return executor[modulo].create(request)


        if operador in ['@@update']:
            return executor[modulo].update(request)


        if operador in ['@@list-all']:
            return executor[modulo].list_all(request)


        if operador in ['@@open-object']:
            return executor[modulo].open_object(request)


        if operador in ['@@delete']:
            return executor[modulo].delete(request)
        
    
        if operador in ['@@workflow']:
            return executor[modulo].workflow(request)
        
