from django import template

register = template.Library()

@register.filter
def getfirst(kdict, k):
    tmp = [x for x in kdict[k][1] if len(x.split('-')) == 3]
    return [sorted([(x, x.replace('-', '.', 1)) for x in tmp], key=lambda x: int(x[0].split('-')[0])*10000+int(x[0].split('-')[1])*100+int(x[0].split('-')[2]))[0]]

@register.filter
def getrelated(kdict, k):
    tmp =  [x for x in kdict[k][1] if len(x.split('-')) == 3]
    return sorted([(x, x.replace('-', '.', 1)) for x in tmp], key=lambda x: int(x[0].split('-')[0])*10000+int(x[0].split('-')[1])*100+int(x[0].split('-')[2]))

@register.filter
def vtime(vdict, title):
    return vdict[title]
