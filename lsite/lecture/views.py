import os
import sys
import re

from lecture import kws

from django.shortcuts import render
from django.http import HttpResponse
from lsite.settings import BASE_DIR
from .models import Slidekeyterm
from .models import Slide
from .models import KeytermRelation
from .models import VideoAttr
from .models import SumAttr
from .models import SumPageTitle
from .models import ChapVideoAttr

from collections import defaultdict
from subprocess import Popen, PIPE

def mk_slide_list():
    slide_list = defaultdict(lambda: defaultdict(list))
    for x in Slide.objects.order_by('chapter'):
        slide_list[int(x.chapter)][int(x.subchapter)].append(int(x.page))
    for x in slide_list:
        slide_list[x] = dict(slide_list[x])
        for y in slide_list[x]:
            slide_list[x][y] = sorted(slide_list[x][y])
    return dict(slide_list)

def getvideoattr(slide):
    v = None
    for x in VideoAttr.objects.filter(title=slide):
        v = x
    return v

def getsummaryattr(slide):
    s = None
    for x in SumAttr.objects.filter(title=slide):
        s = x
    return s

def getkeyterm(slide):
    keyterms = {}
    tmp = [x.keyterm for x in Slidekeyterm.objects.filter(title=slide)]
    for k in Slidekeyterm.objects.filter(title=slide):
        if not k.keyterm == '':
            r = KeytermRelation.objects.filter(k1=k.keyterm)
            keyterms[k.keyterm] = r
            tmp.extend([x.k2 for x in r])
            tmp.extend([x.k1 for x in r])
    keyterm_attr = {}
    for k in set(tmp):
        attr = set([x.title for x in Slidekeyterm.objects.filter(keyterm=k)])
        keyterm_attr[k] = attr
    return keyterms, keyterm_attr

def getkeytermattr(ks):
    keyterm_attr = {}
    for k in ks:
        attr = set([x.title for x in Slidekeyterm.objects.filter(keyterm=k)])
        keyterm_attr[k] = attr
    return keyterm_attr

def search(request):
    if 'q' in request.GET:
        k = kws.kws()
        output_list = k.search(request.GET['q'])
        num = len(output_list)
        result = []
        keyterms = set()
        p = 10
        if 'p' in request.GET:
            p = int(request.GET['p'])*10
        for x in output_list[p-10:p]:
            x = x.strip().split(' ', 3)
            t = re.sub(r'^0', '1-0', x[0][7:].split('_')[0].replace('-0', '-').replace('--', '-0-'))
            ks = set([k.keyterm for k in Slidekeyterm.objects.filter(title=t)])
            keyterms |= set(ks)
            index = t.split('-')
            title_text = Slide.objects.filter(chapter=int(index[0])).filter(subchapter=int(index[1])).filter(page=int(index[2]))[0].title
            result.append((t, x[1][:-3], x[2][:-3], x[3], x[0], ks, title_text))
        # 0: title, 1: start time, 2: end time, 3: trans, 4: video name, 5: ks, 6: title_text
        return render(request, 'lecture/search.html', {'p': p//10, 'q': request.GET['q'], 'num': num, 'result': result, 'page': range(max(1, p//10-13), min(p//10+13, (num//10)+2)), 'last': num//10+1, 'keyterm_attr': getkeytermattr(keyterms)})
    else:
        slide_list = mk_slide_list()
        return render(request, 'lecture/index.html', {'slide_list': slide_list})

def index(request):
    slide_list = mk_slide_list()
    return render(request, 'lecture/index.html', {'slide_list': slide_list})

def subchapter(request, slide):
    slide_list = mk_slide_list()
    title_text = SumPageTitle.objects.filter(title=slide)[0].title_text
    video_attr = getvideoattr(slide+'-1')
    keyterms, keyterm_attr = getkeyterm(slide)
    index = slide.split('-')
    chv_attr = ChapVideoAttr.objects.filter(title=slide)[0]
    return render(request, 'lecture/subchapter.html', {'slide_list': slide_list, 'ch': int(index[0]), 'subch': int(index[1]), 'title': index[0]+'.'+index[1], 'keyterms': keyterms, 'keyterm_attr': keyterm_attr, 'v': video_attr, 'title_text': title_text, 'slide': slide, 'chv_attr': chv_attr} )

def chapter(request, slide):
    slide_list = mk_slide_list()
    title_text = SumPageTitle.objects.filter(title=slide)[0].title_text
    chv_attr = ChapVideoAttr.objects.filter(title=slide)[0]
    video_attr = getvideoattr(slide+'-1-1')
    keyterms, keyterm_attr = getkeyterm(slide)
    return render(request, 'lecture/chapter.html', {'slide_list': slide_list, 'ch': int(slide), 'title': slide, 'keyterms': keyterms, 'keyterm_attr': keyterm_attr, 'v': video_attr, 'title_text': title_text, 'chv_attr': chv_attr} )

def content(request, slide):
    slide_list = mk_slide_list()
    keyterms, keyterm_attr = getkeyterm(slide)
    video_attr = getvideoattr(slide)
    index = slide.split('-')
    title_text = Slide.objects.filter(chapter=int(index[0])).filter(subchapter=int(index[1])).filter(page=int(index[2]))[0].title
    summary_attr = getsummaryattr(slide)
    return render(request, 'lecture/course.html', {'slide_list': slide_list, 'ch': int(index[0]), 'title': index[1]+'-'+index[2], 'subch': int(index[1]), 'page': int(index[2]), 'keyterms': keyterms, 'keyterm_attr': keyterm_attr, 'v': video_attr, 'title_text': title_text, 'summary_attr': summary_attr})
