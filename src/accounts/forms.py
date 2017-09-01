from __future__ import unicode_literals
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from authtools import forms as authtoolsforms
from django.contrib.auth import forms as authforms
from django.core.urlresolvers import reverse

from enrollment.models import Matricula
from profiles.models import Profile
from register.models import Personal, Apoderado, Colegio

import logging

logger = logging.getLogger("project")


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["username"].widget.input_type = "email"  # ugly hack
        self.fields["username"].widget.attrs.update({'class': 'form-control'})
        self.fields["password"].widget.attrs.update({'class': 'form-control'})

        self.helper.layout = Layout(
            Field('username', placeholder="Enter Email", autofocus="", css_class="form-control"),
            Field('password', placeholder="Enter Password"),
            HTML('<a href="{}">Forgot Password?</a>'.format(
                reverse("accounts:password-reset"))),
            Field('remember_me'),
            Submit('sign_in', 'Log in',
                   css_class="btn btn-primary btn-block btn-flat"),
        )


class AsignColegioForm(forms.Form):

    colegios = forms.ModelChoiceField(
        label='Colegios',
        queryset=None,
        required=True,)

    def __init__(self, *args, **kwargs):

        if kwargs.get('user'):
            self.user = kwargs.pop('user', None)

        super(AsignColegioForm, self).__init__(*args, **kwargs)

        try:
            user = self.user
            logger.debug("Usuario: " + user.name)

            profile = Profile.objects.get(user=user)
            logger.debug("profile: " + str(profile.id_persona))

            logger.info("Se logueo el usuario: " + str(user))

        except Profile.DoesNotExist:
            logger.error("Perfil no existe para el usuario: " + str(user))
            raise ValueError("No existe los datos del usuario vinculados a una Persona")

        try:
            personal = Personal.objects.get(persona=profile)
            logger.debug("personal: " + str(personal.id_personal))

            colegios = personal.Colegios.all()
            logger.debug("colegios: " + str(colegios.count()))

        except Personal.DoesNotExist:
            logger.info("El usuario no es un personal")

            #Verificar que sea un apoderado
            apoderado = Apoderado.objects.get(persona=profile)
            logger.debug("Apoderado: " + str(apoderado.id_apoderado))

            alumnos = apoderado.alumnos.all()
            logger.debug("Se obtienen los alumnos: " + str(alumnos.count()))

            coles = []
            for alu in alumnos:
                mat = Matricula.objects.get(alumno=alu)
                logger.debug("Matrícula recuperada: " + str(mat.id_matricula))
                coles.append(mat.colegio.id_colegio)

            colegios = Colegio.objects.filter(pk__in=coles).all()
            logger.debug("Se consultaron los colegios: " + str(colegios))

        self.helper = FormHelper()
        self.helper.form_id = "idcolegios"
        self.helper.form_method = "post"

        self.fields['colegios'].queryset=colegios
        self.fields['colegios'].widget.attrs.update({'class': 'form-control'})

        #self.helper.add_input(Submit('submit', 'Asignar', css_class="btn btn-primary btn-block btn-flat"))

        logger.info("Se asignaron los colegios para ser logueados")

class SignupForm(authtoolsforms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["email"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(
            Field('email', placeholder="Enter Email", autofocus=""),
            Field('name', placeholder="Enter Full Name"),
            Field('password1', placeholder="Enter Password"),
            Field('password2', placeholder="Re-enter Password"),
            Submit('sign_up', 'Sign up', css_class="btn-warning"),
        )


class PasswordChangeForm(authforms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('old_password', placeholder="Enter old password",
                  autofocus=""),
            Field('new_password1', placeholder="Enter new password"),
            Field('new_password2', placeholder="Enter new password (again)"),
            Submit('pass_change', 'Change Password', css_class="btn-warning"),
        )


class PasswordResetForm(authtoolsforms.FriendlyPasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('email', placeholder="Enter email",
                  autofocus=""),
            Submit('pass_reset', 'Reset Password', css_class="btn-warning"),
        )


class SetPasswordForm(authforms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('new_password1', placeholder="Enter new password",
                  autofocus=""),
            Field('new_password2', placeholder="Enter new password (again)"),
            Submit('pass_change', 'Change Password', css_class="btn-warning"),
        )
