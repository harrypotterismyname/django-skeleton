import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
import simplejson

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



class LateTaskView(ListView):
    model = Task
    template_name = "mylist/tasks.html"
    context_object_name = 'items'

    def get(self, request, *args, **kwargs):
        self.queryset = Task.objects.filter( check_list__owner = request.user,  is_deleted=False, real_due_date__lte = timezone.now())
        return super(LateTaskView, self).get(request)



class PublicView(ListView):
    model = CheckList
    template_name = "mylist/public.html"
    context_object_name = 'items'
    queryset = CheckList.objects.filter(public=True, is_deleted=False)


class DetailView(DetailView):
    model = CheckList
    template_name = "mylist/detail.html"
    slug_field = 'slug'
    pk_url_kwarg = 'id'
    context_object_name = 'checklist'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        id = self.kwargs.get('id')
        context['tasks'] = Task.objects.filter(is_deleted=False, check_list__id=id, parent__isnull=True).order_by('due_date')

        return context



class CloneChecklistView(View):

   # model = Task
    def post(self, request, *args, **kwargs):
        checklist_id= kwargs.get('id')
        self.old_checklist = CheckList.objects.get(id=int(checklist_id))
        new_checklist = request.user.profile.clone_checklist(self.old_checklist)


        return HttpResponse(simplejson.dumps({'new_checklist_id':str(new_checklist.id)}, ensure_ascii= False))


    #model = Task
    #template_name = "mylist/ajax-result.html"


class UpdateTaskView(View):

   # model = Task
    def post(self, request, *args, **kwargs):
        task_id= kwargs.get('id')
        self.task = Task.objects.get(id= task_id)
        print task_id

        if request.POST.get('value','false') == 'true':
            self.task.is_checked = True

        else:
            self.task.is_checked = False

        self.task.save()

        return HttpResponse(simplejson.dumps({'result':'ok'}, ensure_ascii= False))


    #model = Task
    #template_name = "mylist/ajax-result.html"


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


class UpdateChecklist(FormView):
    template_name = "mylist/update.html"
    form_class = ChecklistForm
    model = CheckList
    initial = {}
    instance = None

    def get_query(self, k):
        checklist_id = k.get('id', None)
        if checklist_id:
            instance = CheckList.objects.get(pk=int(checklist_id))
            return instance
        return None

    def get_context_data(self, **kwargs):
        context = super(UpdateChecklist, self).get_context_data(**kwargs)
        if self.instance:
            context['tasks'] = self.instance.tasks.filter(is_deleted=False)
        return context

    def get(self, request, *args, **kwargs):
        instance = self.get_query(kwargs)
        self.instance = instance
        if instance:
            self.initial['title'] = instance.title
            if instance.start_at is None:
                instance.start_at = timezone.now()
                instance.save()


            self.initial['start_at'] = datetime.datetime.strftime(instance.start_at, "%d/%m/%Y")
            self.initial['public'] = instance.public
        return super(UpdateChecklist, self).get(request)

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

        instance = self.get_query(kwargs)
        if title:
            start_at = datetime.datetime.combine(datetime.datetime.strptime(start_at, "%d/%m/%Y"), datetime.time(0, 0))
            instance.title=title
            instance.public=public
            instance.start_at=start_at
            instance.save()

            return HttpResponseRedirect(instance.get_absolute_url())

        return super(UpdateChecklist, self).post(request)
