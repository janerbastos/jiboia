from django.urls import path, include

from . import views

app_name = 'jiboia'

urlpatterns = [
    path('', views.index, name='index'),
    path('projetos/', views.projetos, name='projetos'),
    path('projetos/<int:projeto_id>/', views.projetos, name='projetos'),

    path('projetos/<int:projeto_id>/atividades/', views.atividades, name='atividades'),
    path('projetos/<int:projeto_id>/atividades/<int:atividade_id>/', views.atividades, name='atividades'),
    
    path('projetos/<int:projeto_id>/atividades/<int:atividade_id>/acoes/', views.acoes, name='acoes'),
    path('projetos/<int:projeto_id>/atividades/<int:atividade_id>/acoes/<int:acao_id>/', views.acoes, name='acoes'),

    path('projetos/<int:projeto_id>/atividades/<int:atividade_id>/notas/', views.notas, name='notas'),
    path('projetos/<int:projeto_id>/atividades/<int:atividade_id>/notas/<int:nota_id>/', views.notas, name='notas'),
]