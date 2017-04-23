import os

from django.shortcuts import render
from django.http import HttpResponse
from lsite.settings import BASE_DIR
from .models import Slidekeyterm
from .models import Slide
from .models import KeytermRelation
from .models import VideoAttr
from .models import SumAttr
from .models import SumPageTitle

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
        attr = sorted(set([x.title for x in Slidekeyterm.objects.filter(keyterm=k)]))
        keyterm_attr[k] = (attr[0], attr[1:])
    return keyterms, keyterm_attr

def search(request):
    if 'q' in request.GET:
        p = Popen(['/bin/echo', request.GET['q']], stdout=PIPE)
        stdout, stderr = p.communicate()
        num = 2
        result = ['1-0-1', '1-0-2']
        video_time = {}
        for x in result:
            video_time[x] = '00:'+getvideoattr(x).time
        return render(request, 'lecture/search.html', {'q': request.GET['q'], 'out': stdout, 'num': num, 'result': result, 'video_time': video_time})
    else:
        slide_list = mk_slide_list()
        return render(request, 'lecture/index.html', {'slide_list': slide_list})

def subchapter(request, slide):
    pass

def chapter(request, slide):
    slide_list = mk_slide_list()
    title_text = SumPageTitle.objects.filter(title=slide)[0]
    video_attr = getvideoattr(slide+'-1-1')
    #return render(request, 'lecture/course.html', {'slide_list': slide_list, 'ch': int(slide.strip()), 'title': 

def content(request, slide):
    slide_list = mk_slide_list()
    keyterms, keyterm_attr = getkeyterm(slide)
    video_attr = getvideoattr(slide)
    index = slide.split('-')
    title_text = Slide.objects.filter(chapter=int(index[0])).filter(subchapter=int(index[1])).filter(page=int(index[2]))[0].title
    summary_attr = getsummaryattr(slide)
    return render(request, 'lecture/course.html', {'slide_list': slide_list, 'ch': int(index[0]), 'title': index[1]+'-'+index[2], 'subch': int(index[1]), 'page': int(index[2]), 'keyterms': keyterms, 'keyterm_attr': keyterm_attr, 'v': video_attr, 'title_text': title_text, 'summary_attr': summary_attr})
