from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required as LR
from mylist.views import HomeIndex, PublicView, DetailView, AddNewView

urlpatterns = patterns('mylist.views',
    url('^$', HomeIndex.as_view(), name='index'),
    url('^public/$', PublicView.as_view(), name='public'),
    url('^add/$', LR(AddNewView.as_view()), name='add'),

    url('^checklist/(?P<slug>[-_\w]+)/$', DetailView.as_view(), name='detail'),

)