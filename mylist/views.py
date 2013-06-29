from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from mylist.models import CheckList


class HomeIndex(ListView):
    template_name = "mylist/home.html"
    context_object_name = 'items'
    queryset = CheckList.objects.filter(is_deleted=False)   # TODO: order by upcoming tasks

    def get(self, request, *args, **kwargs):
        order = request.GET.get('order', None)
        if order == 'recent':
            self.queryset = CheckList.objects.filter(is_deleted=False)
        return super(HomeIndex, self).get(request)


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

