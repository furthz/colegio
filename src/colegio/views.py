from django.http import HttpResponse
from django.views import generic
from django.views.defaults import page_not_found

import locale
import sys


class HomePage(generic.TemplateView):
    template_name = "home.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"


def mi_error_404(request):
    nombre_template = '404.html'

    return page_not_found(request, template_name=nombre_template)


def view_locale(request):
    loc_info = "getlocale: " + str(locale.getlocale()) + \
               "<br/>getdefaultlocale(): " + str(locale.getdefaultlocale()) + \
               "<br/>fs_encoding: " + str(sys.getfilesystemencoding()) + \
               "<br/>sys default encoding: " + str(sys.getdefaultencoding()) + \
               "<br/>sys default encoding: " + str(sys.getdefaultencoding())
    return HttpResponse(loc_info)
