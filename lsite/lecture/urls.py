from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<slide>[0123456789-]+)/$', views.content, name='content'),
]
