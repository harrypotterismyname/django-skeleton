from django.views.generic import TemplateView


class HomeIndex(TemplateView):
    template_name = "mylist/home.html"