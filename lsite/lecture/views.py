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

def index(request):
    slide_list = defaultdict(list)
    for x in Slide.objects.order_by('chapter'):
        slide_list[int(x.chapter)].append(int(x.index))
    return render(request, 'lecture/index.html', {'slide_list': dict(slide_list)})

def content(request, slide):
    #if 'query' in request.GET:
    #    print(search.send(request.get['query']))

    slide_list = defaultdict(lambda: defaultdict(list))
    for x in Slide.objects.order_by('chapter'):
        slide_list[int(x.chapter)][int(x.subchapter)].append(int(x.page))

    keyterms = {}
    keyterm_relation = {}
    for k in Slidekeyterm.objects.filter(title=slide):
        if not k.keyterm == '':
            keyterms[k.keyterm] = (Slidekeyterm.objects.filter(keyterm=k.keyterm), KeytermRelation.objects.filter(k1=k.keyterm))

    for x in slide_list:
        slide_list[x] = dict(slide_list[x])
        for y in slide_list[x]:
            slide_list[x][y] = sorted(slide_list[x][y])

    index = slide.split('-', 1)

    video = None
    for x in VideoAttr.objects.filter(title=slide):
        video = x

        #VideoAttr(title='1', prev_ch=1, cur_ch=1, ch_time='1', prev_subch=1, cur_subch=1, subch_time='1', prev = 1, cur = 1, time='1')

    return render(request, 'lecture/course.html', {'slide_list': dict(slide_list), 'ch': index[0], 'title': index[1], 'keyterms': keyterms, 'keyterm_relation': keyterm_relation, 'prev_ch': x.prev_ch, 'cur_ch': x.cur_ch, 'ch_time': x.ch_time, 'prev_subch': x.prev_subch, 'cur_subch': x.cur_subch, 'subch_time': x.subch_time, 'prev': x.prev, 'cur': x.cur, 'time': x.time})
