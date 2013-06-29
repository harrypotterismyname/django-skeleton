from django.views.generic import TemplateView


class HomeIndex(TemplateView):
    template_name = "mylist/home.html"


class PublicView(TemplateView):
    template_name = "mylist/public.html"


class DetailView(TemplateView):
    template_name = "mylist/detail.html"