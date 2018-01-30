from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('name', label='Usuario'),
            )

        if self.fields.get('name'):
            self.fields.get('name').label = 'Usuario'

    class Meta:
        model = User
        fields = ['name']


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('picture'),
            Field('bio'),
            Field('nombre'),
            Field('segundo_nombre'),
            Field('apellido_pa'),
            Field('apellido_ma'),
            Submit('update', 'Actualizar', css_class="btn-success"),
            )

    class Meta:
        model = models.Profile
        fields = ['picture', 'bio','nombre', 'segundo_nombre','apellido_pa','apellido_ma']
        labels = {
            'picture': 'Imagen de Perfil',
            'bio': 'Información sobre ti',
            'apellido_pa': 'Apellido Paterno',
            'apellido_ma': 'Apellido Materno',
        }
