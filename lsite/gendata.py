import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lsite.settings')
django.setup()
from lecture.models import Slide
from lecture.models import Slidekeyterm
from lecture.models import KeytermRelation

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

def main():
    Slidekeyterm.objects.filter(title="k2").delete()
    Slidekeyterm.objects.filter(title="k3").delete()
    Slidekeyterm.objects.filter(title="k4").delete()
    Slidekeyterm.objects.filter(title="k5").delete()

if __name__ == '__main__':
    main()
