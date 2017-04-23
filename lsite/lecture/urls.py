from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.content, {'slide': '1-0-1'}),
    url(r'^(?P<slide>[0-9]+-[0-9]+-[0-9]+)/$', views.content, name='content'),
    url(r'^(?P<slide>[0-9]+-[0-9]+)/$', views.subchapter, name='chapter'),
    url(r'^(?P<slide>[0-9]+)/$', views.chapter, name='chapter'),
    url(r'^search/$', views.search),
]
