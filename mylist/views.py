from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from mylist.models import CheckList


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


class AddNewView(CreateView):
    model = CheckList
    template_name = "mylist/new.html"

