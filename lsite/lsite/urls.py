from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^lecture/', include('lecture.urls')),
    url(r'^admin/', admin.site.urls),
]
