#-*- coding: utf-8 -*-

class Abstract():

    """
    Classe abstrada da camada de negocio
    """


    def create(self, request):
        raise NotImplementedError
    

    def update(self, request):
        raise NotImplementedError

    
    def list_all(self, request):
        raise NotImplementedError

    
    def open_object(self, request):
        raise NotImplementedError

    
    def delete(self, object):
        try:
            object.delete()
            return 201
        except:
            return 500
