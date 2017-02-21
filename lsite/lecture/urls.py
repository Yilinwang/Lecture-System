from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.content, {'slide': '1-0-1'}),
    url(r'^(?P<slide>[0123456789-]+)/$', views.content, name='content'),
]
