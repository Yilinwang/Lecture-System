import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lsite.settings')
django.setup()
from lecture.models import Slide

def clean():
    Slide.objects.all().delete()

def add(t, k):
    tmp = Slide(title=t, keyterm=k)
    tmp.save()

def main():
    for i in range(1, 60):
        add('1-'+str(i), '')
    add('1-1', 'signal')
    add('1-1', 'system')
    add('1-2', 'signal')
    add('1-3', 'signal')

if __name__ == '__main__':
    main()
