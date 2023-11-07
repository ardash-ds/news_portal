from django import template

register = template.Library()

censor_list = ['слово1', 'слово2', 'слово3']

@register.filter(name='censor')
def censor(value):
    value_new = []
    value_list = value.split()
    for word in value_list:
        if word in censor_list:
            word = '*цензура*'
        value_new.append(word)
    value_censor = ' '.join(value_new)
    return value_censor

# @register.filter(name='multiply')
# def multiply(value, arg):
#     if isinstance(value, str) and isinstance(arg, int):
#         return str(value) * arg
#     else:
#         raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')
@register.filter(name='multiply')
def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int):  # проверяем, что value — это точно строка, а arg — точно число, чтобы не возникло курьёзов
        return str(value) * arg
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')  #  в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку