from django import template
from django.template.loader import render_to_string
from django.utils.html import format_html


register = template.Library()

@register.filter(name='atividades')
def get_atividades(projeto, fase='a-fazer'):
    atividades = projeto.atividades_deste.filter(workflow=fase)
    html_string = render_to_string('jiboia/componentes/aux_taglibs.html',
        {'objects': atividades, 'opcao': 'atividades' })
    return format_html(html_string)

@register.filter(name='layout')
def get_layout_taglib(modulo):
    return 'jiboia/paginas/%s.html' % modulo