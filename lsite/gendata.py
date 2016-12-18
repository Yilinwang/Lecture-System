import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lsite.settings')
django.setup()
from lecture.models import Slide
from lecture.models import SIndex

def clean():
    Slide.objects.all().delete()

def addSlide(t, k):
    tmp = Slide(title=t, keyterm=k)
    tmp.save()

def main():

if __name__ == '__main__':
    main()
