from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('mylist.urls', namespace='mylist')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('userena.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                            url(r'', include('django.contrib.staticfiles.urls')),
    )