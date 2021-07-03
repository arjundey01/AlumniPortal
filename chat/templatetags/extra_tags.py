from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='val_list')
def val_list(value, arg):
    return [getattr(x,arg) for x in value]

@register.filter(name='key')
def key(value,arg):
    return value.get(arg)

@register.filter(name='chat_other_name')
def chat_other_name(value, arg):
    name = None
    for user in list(value.members.all()):
        if user.user != arg:
            name = user.name

    return name

@register.filter(name='first_word')
def first_word(value):
    return value.split(' ')[0]

@register.filter(name='chat_other_img')
def chat_other_img(value, arg):
    url = None
    for user in list(value.members.all()):
        if user.user != arg:
            url = user.profile_img_url

    return url

@register.filter(name='time_from_iso')
def time_from_iso(value):
    return datetime.fromisoformat(value).strftime("%I:%M %p")