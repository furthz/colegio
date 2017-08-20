import logging

from django.http import HttpResponseRedirect
from django.views.generic import DetailView

from profiles.models import Profile

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from register.forms import PersonaForm, AlumnoForm, ApoderadoForm
from register.models import Alumno, Apoderado
from utils.views import SaveGeneric

logger = logging.getLogger("project")


class CreatePersonaView(CreateView):
    model = Profile
    form_class = PersonaForm
    template_name = "persona_create.html"

    def form_valid(self, form):
        return super(CreatePersonaView, self).form_valid(form)


class PersonaDetail(DetailView):
    model = Profile
    template_name = "persona_detail.html"


class AlumnoCreateView(CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = "alumno_create.html"

    def form_valid(self, form):

        logger.debug("Alumno a crear con DNI: " + form.cleaned_data["numero_documento"])

        alu = SaveGeneric().saveGeneric(padre=Profile, form=form, hijo=Alumno)
        logger.debug("Se creó el alumno en la vista")

        return HttpResponseRedirect(alu.get_absolute_url())


class AlumnoDetail(DetailView):
    model = Alumno
    template_name = "alumno_detail.html"


class ApoderadoCreateView(CreateView):
    model = Apoderado
    form_class = ApoderadoForm
    template_name = "apoderado_create.html"

    def form_valid(self, form):
        logger.debug("Apoderado a crear con DNI: " + form.cleaned_data["numero_documento"])

        apoderado = SaveGeneric().saveGeneric(padre=Profile, form=form, hijo=Apoderado)
        logger.debug("Se creó el apoderado en la vista")

        return HttpResponseRedirect(apoderado.get_absolute_url())


class ApoderadoDetailView(DetailView):
    model = Apoderado
    template_name = "apoderado_detail.html"

