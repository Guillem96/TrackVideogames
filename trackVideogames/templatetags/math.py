from django import template

register = template.Library()


@register.filter
def div(a, b):
    return int(a) / int(b)


@register.filter
def mod(a, b):
    return int(a) % int(b)