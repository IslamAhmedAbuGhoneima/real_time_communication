from django import template


register = template.Library()


@register.filter(name='initials')
def initials(value):
    initials = ''
    initials += value[0].upper()
    if len(value) >= 2:
        initials += value[1]
    return initials
