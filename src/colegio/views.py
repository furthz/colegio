from django.views import generic
from django.views.defaults import page_not_found

class HomePage(generic.TemplateView):
    template_name = "home.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"


def mi_error_404(request):
    nombre_template = '404.html'

    return page_not_found(request, template_name=nombre_template)