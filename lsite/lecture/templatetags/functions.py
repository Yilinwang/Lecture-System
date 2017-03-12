from django import template

register = template.Library()

@register.filter
def getfirst(kdict, k):
    return [(kdict[k][0], kdict[k][0].replace('-', '.', 1))]

@register.filter
def getrelated(kdict, k):
    return [(x, x.replace('-', '.', 1)) for x in kdict[k][1]]
