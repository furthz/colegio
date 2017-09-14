from __future__ import unicode_literals

from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib import messages

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

from utils.middleware import get_current_user, get_current_colegio
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
        redirect = super(LoginView, self).form_valid(form)
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

        #rol = Roles()

        if 'roles' in cache:
            roles = cache.get('roles')
        else:
            roles = Roles.get_roles()
            cache.set('roles', roles, timeout=CACHE_TTL)



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
