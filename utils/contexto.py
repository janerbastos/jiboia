#-*- coding: utf-8 -*-

def data(form, titulo, descricao, objeto, objetos, modulo, action):

    #Função de contexto de requisição

    result = {
        'form': form,
        'titulo': titulo,
        'descricao': descricao,
        'objeto': objeto,
        'objetos': objetos,
        'modulo': modulo,
        'action': action 
    }

    return result