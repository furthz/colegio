import logging

from django.http import HttpResponseRedirect
from django.views.generic import DetailView

from profiles.models import Profile

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from register.forms import PersonaForm, AlumnoForm, ApoderadoForm, PersonalForm, PromotorForm, DirectorForm, CajeroForm, \
    TesoreroForm
from register.models import Alumno, Apoderado, Personal, Promotor, Director, Cajero, Tesorero
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
    template_name = "registro_create.html"

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
    template_name = "registro_create.html"

    def form_valid(self, form):
        logger.debug("Apoderado a crear con DNI: " + form.cleaned_data["numero_documento"])

        apoderado = SaveGeneric().saveGeneric(padre=Profile, form=form, hijo=Apoderado)
        logger.debug("Se creó el apoderado en la vista")

        return HttpResponseRedirect(apoderado.get_absolute_url())


class ApoderadoDetailView(DetailView):
    model = Apoderado
    template_name = "apoderado_detail.html"


class PersonalCreateView(CreateView):
    model = Personal
    form_class = PersonalForm
    template_name = "personal_create.html"

    def form_valid(self, form):
        logger.debug("Personal a crear con DNI: " + form.cleaned_data["numero_documento"])

        personal = SaveGeneric().saveGeneric(padre=Profile, form=form, hijo=Personal)
        logger.debug("Se creó el personal en la vista")

        return HttpResponseRedirect(personal.get_absolute_url())


class PersonalDetailView(DetailView):
    model = Personal
    template_name = "personal_detail.html"


class PromotorCreateView(CreateView):
    model = Promotor
    form_class = PromotorForm
    template_name = "registro_create.html"

    def form_valid(self, form):
        logger.debug("Promotor a crear con DNI: " + form.cleaned_data["numero_documento"])

        personal = SaveGeneric().saveGeneric(padre=Personal, form=form, hijo=Promotor)
        logger.debug("Se creó el promotor en la vista")

        return HttpResponseRedirect(personal.get_absolute_url())


class PromotorDetailView(DetailView):
    model = Promotor
    template_name = "promotor_detail.html"



class DirectorCreateView(CreateView):

    model = Director
    form_class = DirectorForm
    template_name = "registro_create.html"

    def form_valid(self, form):
        logger.debug("Director a crear con DNI: " + form.cleaned_data["numero_documento"])

        personal = SaveGeneric().saveGeneric(padre=Personal, form=form, hijo=Director)
        logger.debug("Se creó el director en la vista")

        return HttpResponseRedirect(personal.get_absolute_url())


class DirectorDetailView(DetailView):
    model = Director
    template_name = "director_detail.html"


class CajeroCreateView(CreateView):

    model = Cajero
    form_class = CajeroForm
    template_name = "registro_create.html"

    def form_valid(self, form):
        logger.debug("Cajero a crear con DNI: " + form.cleaned_data["numero_documento"])

        personal = SaveGeneric().saveGeneric(padre=Personal, form=form, hijo=Cajero)
        logger.debug("Se creó el cajero en la vista")

        return HttpResponseRedirect(personal.get_absolute_url())


class CajeroDetailView(DetailView):
    model = Cajero
    template_name = "cajero_detail.html"


class TesoreroCreateView(CreateView):

    model = Tesorero
    form_class = TesoreroForm
    template_name = "registro_create.html"

    def form_valid(self, form):
        logger.debug("Tesorero a crear con DNI: " + form.cleaned_data["numero_documento"])

        personal = SaveGeneric().saveGeneric(padre=Personal, form=form, hijo=Tesorero)
        logger.debug("Se creó el cajero en la vista")

        return HttpResponseRedirect(personal.get_absolute_url())


class TesoreroDetailView(DetailView):
    model = Tesorero
    template_name = "tesorero_detail.html"

