from __future__ import unicode_literals

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib import messages

from django.views.generic import CreateView, ListView, DetailView, UpdateView

from utils.models import TipoDocumento
from .forms import RegistroUsuarioForm

from rest_framework import generics
from authtools.models import User as Userss
from .serializers import UserSerializer

from django.contrib.auth.models import Group

from authtools import views as authviews
from braces import views as bracesviews
from django.conf import settings
from django.views.decorators.cache import cache_page

from accounts.services import Roles
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from django.contrib.auth.decorators import permission_required
from utils.middleware import validar_roles
from register.models import Profile
from . import forms

import logging

User = get_user_model()
logger = logging.getLogger("project")

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def UsuarioSinPerfil(request):
    return render(request, 'error_falta_perfil.html')


class LoginView(bracesviews.AnonymousRequiredMixin,
                authviews.LoginView):
    """
    Método que permite realizar el Login de un usuario
    """
    template_name = "accounts/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        logger.debug("Inicio LoginView")
        superuser = form.user_cache.is_superuser

        redirect = super(LoginView, self).form_valid(form)
        logger.info("Se logueo")

        if superuser:
            logger.info("Es un Superusuario")

            roles = Roles.get_roles()
            logger.debug("Roles: " + str(roles))

            self.request.session['roles'] = roles

            logger.debug("Fin LoginView")
            return HttpResponseRedirect('/users/me')
        else:
            remember_me = form.cleaned_data.get('remember_me')
            logger.debug("Remember: " + str(remember_me))

            if remember_me is True:
                ONE_MONTH = 30 * 24 * 60 * 60
                expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
                self.request.session.set_expiry(expiry)

            logger.debug("Fin LoginView")
            return redirect


class AsignColegioView(LoginRequiredMixin, View):
    """
    Vista que permite mostrar la asignación del colegio
    """
    template_name = "accounts/asign_colegio.html"

    def get(self, request, *args, **kwargs):
        logger.debug("Inicio GET AsignColegioView")
        user_id = request.user
        try:
            profile = Profile.objects.get(user=user_id)
            logger.debug("Inicio GET AsignColegioView")
            form = forms.AsignColegioForm(request.POST, user=user_id)
            logger.debug("Formulario para mostrar selección de colegios")
            return render(request, self.template_name, {'form': form})

        except Profile.DoesNotExist:
            return HttpResponseRedirect(
                "/error_usuario_sin_perfil/")

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request, **kwargs):
        logger.debug("Inicio POST AsignColegioView")

        form = forms.AsignColegioForm(request.POST, user=request.user)
        logger.info("Se asignó el colegio")

        if form.is_valid():
            colegios = form.cleaned_data['colegios']
            logger.debug("Colegio seleccionado: " + str(colegios.id_colegio))

            request.session['colegio'] = colegios.id_colegio
            request.session['colegio_name'] = colegios.nombre
            logger.info("Se asignó a las variables de session el colegio")

        logger.info("Usuario Logueado")

        try:
            if request.session['roles']:
                roles = request.session['roles']
                logger.debug("Se asignaron los roles desde la sesion")
        except:
            roles = Roles.get_roles()
            request.session['roles'] = roles
            logger.debug("Se obtuvieron los roles desde la BD")

        return HttpResponseRedirect('/users/me')


class LogoutView(authviews.LogoutView):
    url = reverse_lazy('home')


class SignUpView(bracesviews.AnonymousRequiredMixin,
                 bracesviews.FormValidMessageMixin,
                 generic.CreateView):
    form_class = forms.SignupForm
    model = User
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')
    form_valid_message = "You're signed up!"

    def form_valid(self, form):
        r = super(SignUpView, self).form_valid(form)
        username = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = auth.authenticate(email=username, password=password)
        auth.login(self.request, user)
        return r


class PasswordChangeView(authviews.PasswordChangeView):
    form_class = forms.PasswordChangeForm
    template_name = 'accounts/password-change.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request,
                         "Your password was changed, "
                         "hence you have been logged out. Please relogin")
        return super(PasswordChangeView, self).form_valid(form)


class PasswordResetView(authviews.PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = 'accounts/password-reset.html'
    success_url = reverse_lazy('accounts:password-reset-done')
    subject_template_name = 'accounts/emails/password-reset-subject.txt'
    email_template_name = 'accounts/emails/password-reset-email.html'


class PasswordResetDoneView(authviews.PasswordResetDoneView):
    template_name = 'accounts/password-reset-done.html'


class PasswordResetConfirmView(authviews.PasswordResetConfirmAndLoginView):
    template_name = 'accounts/password-reset-confirm.html'
    form_class = forms.SetPasswordForm


#################################################
#####          CRUD DE USUARIOS             #####
#################################################

class RegistroUsarioListView(ListView):
    model = Userss
    template_name = 'register_accounts/register_accounts_list.html'


class RegistroUsarioDetailView(DetailView):
    model = Userss
    template_name = 'register_accounts/register_accounts_detail.html'


class RegistroUsarioUpdateView(UpdateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('accounts:register_accounts_list')

    # Sistemas, Director, Cajero, Tesorero----------------------------------------------


class RegistroUsuario(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:persona_create')

    def get(self, request, *args, **kwargs):
        logger.debug("Inicio GET RegistroUsuario")

        roles = ['sistemas', 'director', 'promotor']
        logger.info("Roles: " + str(roles))

        if request.user.is_superuser:
            logger.info("Es super usuario")

            grupos = []
            grup = Group.objects.get(id=10)
            grupos.append(grup)
            logger.debug("Grupo con permiso: " + str(grup.name))

            logger.info("Se asignó el usuario al grupo: " + str(grup.name))
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'grupos': grupos,
            })
        elif validar_roles(roles):
            logger.debug("No es super usuario")

            lista_roles = [2, 3, 4, 5, 6, 11]
            grupos = []
            for rol in lista_roles:
                grup = Group.objects.get(id=rol)
                logger.debug("Grupo: " + str(grup.name))

                grupos.append(grup)

            logger.info("Se asignó el usuario a los grupos: " + str(lista_roles))
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'grupos': grupos,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        logger.debug("Inicio POST RegistroUsuario")
        roles = ['sistemas', 'director', 'promotor']
        usuario = Userss()
        form = self.form_class(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            usuario.name = data_form['name']
            usuario.email = data_form['email']
            usuario.set_password(data_form['password1'])

            tipo_documento_val = data_form.get('select_documento')

            usuario.save()

            grupos = data_form['groups']

            # from django.contrib.auth.models import Group

            for g in grupos:
                g.user_set.add(usuario)

            request.session['usuario_creado'] = usuario.id
            request.session['tipo_documento_value'] = tipo_documento_val
            request.session['num_documento'] = usuario.name
            request.session['correo'] = usuario.email

            # print ('id_usuario: ' + str(request.session['usuario_creado']))
            # print ("=======================================================")
            # print ('tipo_documento_val: ' + str(request.session['tipo_documento_value']))
            # print ("=======================================================")
            # print ('num_documento: ' + str(request.session['num_documento']))
            # print ("=======================================================")
            # print ('correo_mail: ' + str(request.session['correo']))

            #            request.session['docu_num'] = documento_num
            #           print(documento_num)
            # request['grupos'] = grupos

            return HttpResponseRedirect(self.success_url)

        else:

            if request.user.is_superuser:
                logger.info("Es super usuario")

                grupos = []
                grup = Group.objects.get(id=10)
                grupos.append(grup)
                logger.debug("Grupo con permiso: " + str(grup.name))

                logger.info("Se asignó el usuario al grupo: " + str(grup.name))

            elif validar_roles(roles):
                logger.debug("No es super usuario")

                lista_roles = [2, 3, 4, 5, 6, 11]
                grupos = []
                for rol in lista_roles:
                    grup = Group.objects.get(id=rol)
                    logger.debug("Grupo: " + str(grup.name))

                    grupos.append(grup)

                logger.info("Se asignó el usuario a los grupos: " + str(lista_roles))

            return render(request=request, template_name=self.template_name, context={'form': form, 'grupos': grupos})


class RegistroUsarioCreationViewSistema(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:sistemas_create')

    @method_decorator(permission_required('register.sistemas_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        if request.user.is_superuser:
            return super(RegistroUsarioCreationViewSistema, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class RegistroUsarioCreationViewDirector(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:director_create')

    @method_decorator(permission_required('register.director_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['sistemas', 'promotor']

        if validar_roles(roles=roles):
            return super(RegistroUsarioCreationViewDirector, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class RegistroUsarioCreationViewCajero(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:cajero_create')

    @method_decorator(permission_required('register.cajero_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'tesorero']

        if validar_roles(roles=roles):
            return super(RegistroUsarioCreationViewCajero, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class RegistroUsarioCreationViewTesorero(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:tesorero_create')

    @method_decorator(permission_required('register.tesorero_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'sistemas']

        if validar_roles(roles=roles):
            return super(RegistroUsarioCreationViewTesorero, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class RegistroUsarioCreationViewDocente(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:docente_create')

    @method_decorator(permission_required('register.docente_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'sistemas']

        if validar_roles(roles=roles):
            return super(RegistroUsarioCreationViewDocente, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


from django.contrib.auth.models import User as UserAPI, Group as GroupAPI
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = GroupAPI.objects.all()
    serializer_class = GroupSerializer


class RegistroUsuarioApoderado(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_apoderado_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:apoderado_create')

    def get(self, request, *args, **kwargs):
        logger.debug("Inicio GET RegistroUsuarioApoderado")
        # print("==========================")
        # print('Inicio GET RegistroUsuarioApoderado')

        roles = ['sistemas', 'director', 'promotor', 'administrativo']
        logger.info("Roles: " + str(roles))
        # print("Roles: " + str(roles))
        # print("==========================")

        if request.user.is_superuser:
            logger.info("Es super usuario")
            # print("==========================")
            # print('Es super usuario')
            # print("==========================")

            grupos = []
            grup = Group.objects.get(id=10)
            grupos.append(grup)
            logger.debug("Grupo con permiso: " + str(grup.name))

            logger.info("Se asignó el usuario al grupo: " + str(grup.name))
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'grupos': grupos,
            })
        elif validar_roles(roles):
            logger.debug("No es super usuario")
            # print('No es super usuario')
            # print("==========================")
            lista_roles = [7]
            grupos = []
            for rol in lista_roles:
                grup = Group.objects.get(id=rol)
                logger.debug("Grupo: " + str(grup.name))
                # print("Grupo: " + str(grup.name))
                # print("==========================")
                grupos.append(grup)
            logger.info("Se asignó el usuario a los grupos: " + str(lista_roles))
            # print("Se asignó el usuario a los grupos: " + str(lista_roles))
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'grupos': grupos,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        logger.debug("Inicio POST RegistroUsuario")
        # print('Inicio POST RegistroUsuario')
        # print("==========================")

        roles = ['sistemas', 'director', 'promotor', 'administrativo']

        usuario = Userss()

        form = self.form_class(request.POST)

        if form.is_valid():
            # print('Validación de form correcto')
            # print("==========================")
            data_form = form.cleaned_data
            usuario.name = data_form['name']
            usuario.email = data_form['email']
            usuario.set_password(data_form['password1'])
            tipo_documento_val = data_form.get('select_documento')

            usuario.save()

            grupos = data_form['groups']

            # from django.contrib.auth.models import Group

            for g in grupos:
                g.user_set.add(usuario)

            request.session['usuario_creado'] = usuario.id
            request.session['tipo_documento_value'] = tipo_documento_val
            request.session['num_documento'] = usuario.name
            request.session['correo'] = usuario.email

            # print ('id_usuario: ' + str(request.session['usuario_creado']))
            # print ("=======================================================")
            # print ('tipo_documento_val: ' + str(request.session['tipo_documento_value']))
            # print ("=======================================================")
            # print ('num_documento: ' + str(request.session['num_documento']))
            # print ("=======================================================")
            # print ('correo_mail: ' + str(request.session['correo']))

            # print('usuario_creado En USUARIO FORM : ' + str(request.session['usuario_creado']))
            # print("==========================")
            # request['grupos'] = grupos

            return HttpResponseRedirect(self.success_url)

        else:

            if request.user.is_superuser:
                logger.info("Es super usuario")

                grupos = []
                grup = Group.objects.get(id=10)
                grupos.append(grup)
                logger.debug("Grupo con permiso: " + str(grup.name))

                logger.info("Se asignó el usuario al grupo: " + str(grup.name))

            elif validar_roles(roles):
                logger.debug("No es super usuario")

                lista_roles = [7]
                grupos = []
                for rol in lista_roles:
                    grup = Group.objects.get(id=rol)
                    logger.debug("Grupo: " + str(grup.name))

                    grupos.append(grup)

                logger.info("Se asignó el usuario a los grupos: " + str(lista_roles))

            return render(request=request, template_name=self.template_name, context={'form': form, 'grupos': grupos})


class RegistroUsarioCreationViewApoderado(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:apoderado_create')

    @method_decorator(permission_required('register.docente_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'sistemas']

        if validar_roles(roles=roles):
            return super(RegistroUsarioCreationViewApoderado, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
