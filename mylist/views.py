import datetime
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from mylist.models import CheckList, Task
from mylist.forms import ChecklistForm


class HomeIndex(ListView):
    template_name = "mylist/home.html"
    context_object_name = 'items'
    active = ''
    queryset = CheckList.objects.filter(is_deleted=False)

    def get(self, request, *args, **kwargs):
        order = request.GET.get('order', None)
        if order == 'recent':
            self.queryset = CheckList.objects.filter(is_deleted=False, owner=request.user)
            self.active = 'recent'
        elif order == 'overdated':
            qs = CheckList.objects.filter(is_deleted=False, owner=request.user)
            items = []
            for i in qs:
                for j in i.tasks.filter(is_deleted=False):
                    if j.is_overdated():
                        items.append(i)
            self.queryset = items
            self.active = 'overdated'
        else:
            self.queryset = CheckList.objects.filter(is_deleted=False, owner=request.user)  # TODO: order
        return super(HomeIndex, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(HomeIndex, self).get_context_data(**kwargs)
        context['active'] = self.active
        return context


class PublicView(ListView):
    model = CheckList
    template_name = "mylist/public.html"
    context_object_name = 'items'


class DetailView(DetailView):
    model = CheckList
    template_name = "mylist/detail.html"
    slug_field = 'slug'
    pk_url_kwarg = 'id'
    context_object_name = 'checklist'


class AddNewView(FormView):
    model = CheckList
    template_name = "mylist/new.html"
    form_class = ChecklistForm

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title', None)
        start_at = request.POST.get('start_at', timezone.now())
        public = request.POST.get('public', False)
        num_task = request.POST.get('num_task', None)
        tasks = []
        if num_task:
            for i in range(1, int(num_task)):
                t = request.POST.get('title%d' % i, '')
                d = request.POST.get('due%d' % i, None)
                if t:
                    tasks.append([t, d])

        if title:
            start_at = datetime.datetime.combine(datetime.datetime.strptime(start_at, "%d/%m/%Y"), datetime.time(0, 0))
            new = self.model.objects.create(title=title, owner=request.user, public=public, start_at=start_at)

            # create tasks
            count = 0
            for t in tasks:
                count += 1
                if t[1]:
                    Task.objects.create(title=t[0], check_list=new, due_date=t[1], order=count)
                else:
                    Task.objects.create(title=t[0], check_list=new, order=count)

            return HttpResponseRedirect(new.get_absolute_url())

        return super(AddNewView, self).post(request)

