from django.http import HttpResponse
from django.views import generic
from django.views.defaults import page_not_found
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import locale
import sys

from profiles.models import Profile


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


class Login_api_general(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(Login_api_general, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        perfil = Profile.objects.values('pk').filter(user_id=user.id)[0]['pk']
        return Response({
            'token': token.key,
            'idUsuario': user.id,
            'idPersona': perfil

        })
