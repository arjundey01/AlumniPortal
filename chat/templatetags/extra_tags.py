from django import template

register = template.Library()

@register.filter(name='val_list')
def val_list(value, arg):
    return [getattr(x,arg) for x in value]

@register.filter(name='key')
def key(value,arg):
    return value.get(arg)