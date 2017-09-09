import logging

from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.db.models import Q
from django.conf import settings

from enrollment.models import Matricula
from profiles.models import Profile

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from register.forms import PersonaForm, AlumnoForm, ApoderadoForm, PersonalForm, PromotorForm, DirectorForm, CajeroForm, \
    TesoreroForm, ProveedorForm
from register.models import Alumno, Apoderado, Personal, Promotor, Director, Cajero, Tesorero, Colegio, Proveedor, \
    ProvedorColegio, PersonalColegio, Administrativo
from utils.middleware import get_current_colegio
from utils.views import SaveGeneric, MyLoginRequiredMixin

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

        als = Alumno.objects.all()

        logger.info("Se creó el alumno")
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

        logger.debug("Se creó el apoderado")
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

        logger.info("Se creó el personal")
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

        logger.info("Se creó el promotor")
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

        logger.info("Se creó el director")
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

        logger.info("Se creó el Cajero")
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
        logger.debug("Se creó el tesorero en la vista")

        logger.info("Se creó el tesorero")
        return HttpResponseRedirect(personal.get_absolute_url())


class TesoreroDetailView(DetailView):
    model = Tesorero
    template_name = "tesorero_detail.html"


class ProveedorCreateView(MyLoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedor_create.html"

    def form_valid(self, form):
        instance = form.save()
        instance.save()

        prov_col = ProvedorColegio()
        id_colegio = self.request.session.get('colegio')
        cole = Colegio.objects.get(pk=id_colegio)
        prov_col.colegio = cole
        prov_col.proveedor = instance
        prov_col.save()

        return HttpResponseRedirect(instance.get_absolute_url())


class ProveedorDetailView(DetailView):
    model = Proveedor
    template_name = "proveedor_detail.html"


class PersonaDetailView(DetailView):
    # model = Profile
    queryset = Profile.objects.select_related()
    template_name = "registro_detail.html"


class PersonaListView(TemplateView):
    template_name = "persona_list.html"

    # permission_required = ('register.list_persona',)

    def post(self, request, *args, **kwargs):

        colegio = get_current_colegio()

        numero_documento = request.POST["numero_documento"]

        nombres = request.POST["nombres"]

        if numero_documento and not nombres:
            empleados = Profile.objects.filter(numero_documento=numero_documento,
                                               personal__Colegios__id_colegio=colegio)
        elif numero_documento and nombres:
            empleados = Profile.objects.filter(Q(numero_documento=numero_documento),
                                               Q(nombre__contains=nombres) |
                                               Q(apellido_pa__contains=nombres) |
                                               Q(apellido_ma__contains=nombres))  # ,
            # personal__Colegios__id_colegio=colegio)
        elif not numero_documento and nombres:
            empleados = Profile.objects.filter(Q(nombre__contains=nombres) |
                                               Q(apellido_pa__contains=nombres) |
                                               Q(apellido_ma__contains=nombres))
        else:
            return self.get(request)

        paginator = Paginator(empleados, 5)

        page = request.GET.get('page', 1)

        try:
            buscados = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            buscados = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            buscados = paginator.page(paginator.num_pages)

        return render(request, self.template_name,
                      {'empleados': buscados,
                       'numero_documento': numero_documento,
                       'nombres': nombres})

    @method_decorator(permission_required('register.list_personal', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        logger.debug("get_context")

        # Obtener el id del colegio
        id_colegio = get_current_colegio()
        logger.debug("colegio id: " + str(id_colegio))

        colegio = Colegio.objects.get(pk=id_colegio)
        logger.debug("colegio: " + str(colegio))

        # Obtener los empleados del colegio
        empleados = PersonalColegio.objects.filter(colegio=colegio, activo=True).all()
        logger.debug("cantidad de empleados: " + str(empleados.count()))

        personal = []

        for empleado in empleados:

            rol = ""

            try:
                if empleado.personal.promotor:
                    rol = "Promotor "
            except Promotor.DoesNotExist:
                pass

            try:
                if empleado.personal.director:
                    rol = "Director "
            except Director.DoesNotExist:
                pass

            try:
                if empleado.personal.cajero:
                    rol = "Cajero "
            except Cajero.DoesNotExist:
                pass

            try:
                if empleado.personal.administrativo:
                    rol = "Administrativo "
            except Administrativo.DoesNotExist:
                pass

            try:
                if empleado.personal.tesorero:
                    rol = "Tesorero "
            except Tesorero.DoesNotExist:
                pass

            empleado.personal.persona.rol = rol

            personal.append(empleado.personal.persona)

        alumnos = Matricula.objects.filter(colegio=colegio, activo=True).all()
        logger.debug("Cantidad de alumnos: " + str(alumnos.count()))

        for alumno in alumnos:
            alumno.alumno.persona.rol = "Alumno"
            personal.append(alumno.alumno.persona)
            # personal.append(alumno.alumno.apoderado)

        page = request.GET.get('page', 1)

        paginator = Paginator(personal, 5)

        try:
            empleados = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            empleados = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            empleados = paginator.page(paginator.num_pages)

        logger.debug("Se cargo el contexto")
        return render(request, self.template_name, {'empleados': empleados})  # return context
