from __future__ import unicode_literals

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib import messages

from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .forms import RegistroUsuarioForm
from authtools.models import User as Userss




from authtools import views as authviews
from braces import views as bracesviews
from django.conf import settings
from django.views.decorators.cache import cache_page

from accounts.services import Roles
from enrollment.models import Matricula
from profiles.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from register.models import Personal, Colegio, Promotor, Director, Cajero, Tesorero, Administrativo, Apoderado
from django.shortcuts import render
from django.views import View

from . import forms

import logging

User = get_user_model()
logger = logging.getLogger("project")

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class LoginView(bracesviews.AnonymousRequiredMixin,
                authviews.LoginView):
    """
    Método que permite realizar el Login de un usuario
    """
    template_name = "accounts/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        superuser = form.user_cache.is_superuser
        redirect = super(LoginView, self).form_valid(form)
        if superuser:
            roles = Roles.get_roles()
            self.request.session['roles'] = roles
            return HttpResponseRedirect('/users/me')
        else:

            remember_me = form.cleaned_data.get('remember_me')
            if remember_me is True:
                ONE_MONTH = 30 * 24 * 60 * 60
                expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
                self.request.session.set_expiry(expiry)
            return redirect


class AsignColegioView(LoginRequiredMixin, View):
    """
    Vista que permite mostrar la asignación del colegio
    """
    template_name = "accounts/asign_colegio.html"

    def get(self, request, *args, **kwargs):
        logger.debug("GET formulario")

        form = forms.AsignColegioForm(request.POST, user=request.user)
        logger.debug("Formulario para mostrar selección de colegios")

        return render(request, self.template_name, {'form': form})

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request, *args, **kwargs):

        form = forms.AsignColegioForm(request.POST, user=request.user)

        if form.is_valid():
            colegios = form.cleaned_data['colegios']
            logger.debug("Colegio seleccionado: " + str(colegios.id_colegio))
            request.session['colegio'] = colegios.id_colegio

        logger.info("Usuario Logueado")

        try:
            if request.session['roles']:
                roles = request.session['roles']
        except:
            roles = Roles.get_roles()
            request.session['roles'] = roles

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
class RegistroUsarioCreationViewSistema(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:sistemas_create')

class RegistroUsarioCreationViewDirector(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:director_create')

class RegistroUsarioCreationViewCajero(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:cajero_create')

class RegistroUsarioCreationViewTesorero(CreateView):
    model = Userss
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('registers:tesorero_create')


