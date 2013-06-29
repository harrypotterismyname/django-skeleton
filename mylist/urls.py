from django.conf.urls import patterns, url
from mylist.views import HomeIndex

urlpatterns = patterns('mylist.views',
    url('^$', HomeIndex.as_view(), name='index'),
)