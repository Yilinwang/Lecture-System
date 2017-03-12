import os
import django
import subprocess
from collections import defaultdict
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lsite.settings')
django.setup()
from lecture.models import Slide
from lecture.models import Slidekeyterm
from lecture.models import KeytermRelation
from lecture.models import VideoAttr

from glob import glob

def clean():
    Slide.objects.all().delete()

def init(num):
    for x in glob('./lecture/static/lecture/slides/'+num+'/*'):
        a = x.split(num+'/')[1][:-4]
        b = a.split('-')
        print(b)
        tmp = Slide(chapter=int(num), subchapter=int(b[0]), page=int(b[1]))
        tmp.save()

def addkeyterm(t, k):
    tmp = Slidekeyterm(title=t, keyterm=k)
    tmp.save()

def addrelation(a, b):
    tmp = KeytermRelation(k1=a, k2=b)
    tmp.save()
    tmp = KeytermRelation(k1=b, k2=a)
    tmp.save()

def percentage(a):
    if a == 0:
        return 0
    p = round(a*100)
    return p if p > 0 else 1

def video():
    d = defaultdict(lambda: defaultdict(list))
    for x in glob('./lecture/static/lecture/videos/*'):
        title = x.split('/')[-1].split('.')[0]
        time = subprocess.run(['ffprobe', x], stderr=subprocess.PIPE).stderr.strip().split(b'Duration: ')[1].split(b',')[0].split(b'.')[0].split(b':', 1)[1].decode('ascii')
        sec = int(time.split(':')[0])*60+int(time.split(':')[1])
        d[int(title.split('-')[0])][int(title.split('-')[1])].append((title, time, sec))

    allsum = 0
    chsum = defaultdict(int)
    subchsum = defaultdict(lambda: defaultdict(int))
    for x in d:
        for y in d[x]:
            d[x][y] = sorted(d[x][y], key=lambda k: int(k[0].split('-')[2]))
            s = sum([k[2] for k in d[x][y]])
            chsum[x] += s
            subchsum[x][y] += s
            allsum += s
    prev_ch = 0
    for x in d:
        prev_subch = 0
        for y in d[x]:
            prev = 0
            for z in d[x][y]:
                print(z[0], percentage(prev_ch/allsum), percentage(chsum[x]/allsum), str(timedelta(seconds=chsum[x])), percentage(prev_subch/chsum[x]), percentage(subchsum[x][y]/chsum[x]), str(timedelta(seconds=subchsum[x][y])), percentage(prev/subchsum[x][y]), percentage(z[2]/subchsum[x][y]), z[1])
                tmp = VideoAttr(title=z[0], prev_ch=percentage(prev_ch/allsum), cur_ch=percentage(chsum[x]/allsum), ch_time=str(timedelta(seconds=chsum[x])), prev_subch=percentage(prev_subch/chsum[x]), cur_subch=percentage(subchsum[x][y]/chsum[x]), subch_time=str(timedelta(seconds=subchsum[x][y])), prev=percentage(prev/subchsum[x][y]), cur=percentage(z[2]/subchsum[x][y]), time=z[1])
                tmp.save()
                prev += z[2]
            prev_subch += subchsum[x][y]
        prev_ch += chsum[x]

def m():
    tmp = VideoAttr(title='1', prev_ch=1, cur_ch=1, ch_time='1', prev_subch=1, cur_subch=1, subch_time='1', prev = 1, cur = 1, time='1')

def main():
    addkeyterm('1-0-3', 'k1')

if __name__ == '__main__':
    main()
