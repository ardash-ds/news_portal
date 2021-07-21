from django import template

register = template.Library()

censor_list = ['слово1', 'слово2', 'слово3']

@register.filter(name='censor')
def censor(value):
    value_new = []
    value_list = value.split()
    for word in value_list:
        if word in censor_list:
            word = 'цензура'
        value_new.append(word)
    value_censor = ' '.join(value_new)
    return value_censor
