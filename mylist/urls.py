from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required as LR, permission_required
from mylist.views import HomeIndex, PublicView, DetailView, AddNewView, UpdateTaskView, UpdateChecklist, CloneChecklistView, LateTaskView

urlpatterns = patterns('mylist.views',
    url('^$', LR(HomeIndex.as_view()), name='index'),
    url('^public/$', PublicView.as_view(), name='public'),
    url('^add/$', LR(AddNewView.as_view()), name='add'),
    url('^ajax/task/(?P<id>\d+)/update/$', permission_required('tasks.can_edit')(UpdateTaskView.as_view()), name='update_task'),

    url('^ajax/checklist/(?P<id>\d+)/clone/$', LR(CloneChecklistView.as_view()), name='clone_checklist'),
    url('^checklist/(?P<slug>[-_\w]+)/(?P<id>\d+)/$', DetailView.as_view(), name='detail'),
    url('^checklist/(?P<id>\d+)/update/$', UpdateChecklist.as_view(), name='update'),
    url('^tasks/late/$', LR(LateTaskView.as_view()), name='late tasks'),

)