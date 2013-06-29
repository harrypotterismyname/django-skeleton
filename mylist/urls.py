from django.conf.urls import patterns, url
from mylist.views import HomeIndex, PublicView, DetailView

urlpatterns = patterns('mylist.views',
    url('^$', HomeIndex.as_view(), name='index'),
    url('^public/$', PublicView.as_view(), name='public'),

    url('^checklist/(?P<slug>.*)/$', DetailView.as_view(), name='detail'),

)