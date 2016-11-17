from django.shortcuts import render
from django.http import HttpResponse
import os
from lsite.settings import BASE_DIR
from .models import Slide

def index(request):
    slide_list = Slide.objects.order_by('id')
    return render(request, 'lecture/index.html', {'slide_list': slide_list, 'content': '#main page content'})

def content(request, slide):
    slide_list = Slide.objects.order_by('id')
    content = 'not found'
    for s in slide_list:
        if s.title == slide:
            content = s.content
    return render(request, 'lecture/index.html', {'slide_list': slide_list, 'content': content})
