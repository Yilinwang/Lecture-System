from django.shortcuts import render
from django.http import HttpResponse
import os
from lsite.settings import BASE_DIR

def index(request):
    fpath = os.path.join(BASE_DIR, 'assets/chapter')
    content = []
    with open(fpath) as fp:
        for line in fp:
            content.append(line)
    return render(request, 'lecture/index.html', {'chapter': content})

def content(request, chapter):
    return HttpResponse('#content of '+chapter)
