import os

from django.shortcuts import render
from django.http import HttpResponse
from lsite.settings import BASE_DIR
from .models import Slidekeyterm
from .models import Slide
from .models import KeytermRelation
from .models import VideoAttr

from collections import defaultdict
from search import send

def mk_slide_list():
    slide_list = defaultdict(lambda: defaultdict(list))
    for x in Slide.objects.order_by('chapter'):
        slide_list[int(x.chapter)][int(x.subchapter)].append(int(x.page))

    for x in slide_list:
        slide_list[x] = dict(slide_list[x])
        for y in slide_list[x]:
            slide_list[x][y] = sorted(slide_list[x][y])
    return dict(slide_list)

def index(request):
    slide_list = mk_slide_list()
    return render(request, 'lecture/index.html', {'slide_list': slide_list})

def content(request, slide):
    #if 'query' in request.GET:
    #    print(search.send(request.get['query']))

    slide_list = mk_slide_list()

    keyterms = {}
    keyterm_relation = {}
    for k in Slidekeyterm.objects.filter(title=slide):
        if not k.keyterm == '':
            keyterms[k.keyterm] = (Slidekeyterm.objects.filter(keyterm=k.keyterm), KeytermRelation.objects.filter(k1=k.keyterm))

    index = slide.split('-', 1)

    v = None
    for x in VideoAttr.objects.filter(title=slide):
        v = x

    return render(request, 'lecture/course.html', {'slide_list': slide_list, 'ch': index[0], 'title': index[1], 'keyterms': keyterms, 'keyterm_relation': keyterm_relation, 'v': v})
