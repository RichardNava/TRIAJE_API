from django import template

register = template.Library()

@register.filter(name="indice")
def indice(indexable, i):
    return indexable[i]

