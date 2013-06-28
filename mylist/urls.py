from django.conf.urls import patterns, url
from qna.views import HomeIndex

urlpatterns = patterns('qna.views',
    url('^$', HomeIndex.as_view(), name='index'),
)