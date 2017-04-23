from django import template

register = template.Library()

@register.filter
def getfirst(kdict, k):
    return [(kdict[k][0], kdict[k][0].replace('-', '.', 1))]

@register.filter
def getrelated(kdict, k):
    return sorted([(x, x.replace('-', '.', 1)) for x in kdict[k][1]], key=lambda x: int(x[0].split('-')[0])*10000+int(x[0].split('-')[1])*100+int(x[0].split('-')[2]))

@register.filter
def vtime(vdict, title):
    return vdict[title]
