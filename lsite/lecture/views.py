import os

from django.shortcuts import render
from django.http import HttpResponse
from lsite.settings import BASE_DIR
from .models import Slide
from .models import SIndex

from collections import defaultdict

def uniqlist():
    slide_list = ['']
    for x in Slide.objects.order_by('title'):
        if x.title != slide_list[-1]:
            slide_list.append(x.title)
    slide_list = slide_list[1:]
    slide_list = sorted(slide_list, key=lambda x: tuple([int(y) for y in x.split('-')]))
    return slide_list

def index(request):
    #slide_list = uniqlist()
    slide_list = defaultdict(list)
    for x in SIndex.objects.order_by('chapter'):
        slide_list[int(x.chapter)].append(int(x.index))
    return render(request, 'lecture/index.html', {'slide_list': dict(slide_list)})

def content(request, slide):
    #slide_list = uniqlist()
    slide_list = defaultdict(list)
    for x in SIndex.objects.order_by('chapter'):
        slide_list[int(x.chapter)].append(int(x.index))

    '''
    title = 'Not Found'
    for s in uniqlist():
        if s == slide:
            title = s
    '''

    keyterms = {}
    for k in Slide.objects.filter(title=slide):
        if not k.keyterm == '':
            keyterms[k.keyterm] = Slide.objects.filter(keyterm=k.keyterm)

    return render(request, 'lecture/course.html', {'slide_list': dict(slide_list), 'title': slide, 'keyterms': keyterms})
