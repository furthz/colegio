import logging

from dal import autocomplete
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.db.models import Q
from django.conf import settings
from django.views.generic import UpdateView

from enrollment.models import Matricula
from profiles.models import Profile

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from register.forms import PersonaForm, AlumnoForm, ApoderadoForm, PersonalForm, PromotorForm, DirectorForm, CajeroForm, \
    TesoreroForm, ProveedorForm, ColegioForm, SistemasForm
from register.models import Alumno, Apoderado, Personal, Promotor, Director, Cajero, Tesorero, Colegio, Proveedor, \
    ProveedorColegio, PersonalColegio, Administrativo, Direccion, Telefono, Sistemas
from utils.middleware import get_current_colegio, validar_roles, get_current_user
from utils.views import SaveGeneric, MyLoginRequiredMixin
from payments.models import CajaChica

logger = logging.getLogger("project")


class AlumnoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Alumno.objects.none()

        qs = Alumno.objects.all()

        if self.q:
            qs = qs.filter(apellido_pa__istartswith=self.q)

        return qs

class CreatePersonaView(MyLoginRequiredMixin, CreateView):
    """
    Vista para poder crear una persona
    """
    model = Profile
    form_class = PersonaForm
    template_name = "registro_create.html"

    @method_decorator(permission_required('register.persona_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'coordinador', 'tesorero', 'sistemas']

        if validar_roles(roles=roles):
            return super(CreatePersonaView, self).get(request, args, kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.persona_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def form_valid(self, form):

        roles = ['promotor', 'director', 'coordinador', 'tesorero', 'sistemas']

        if validar_roles(roles=roles):
            return super(CreatePersonaView, self).form_valid(form)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class PersonaDetail(MyLoginRequiredMixin, DetailView):
    model = Profile
    template_name = "persona_detail.html"

    @method_decorator(permission_required('register.persona_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'coordinador', 'tesorero', 'sistemas']

        if validar_roles(roles=roles):
            return super(PersonaDetail, self).get(request, args, kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.persona_detail', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def form_valid(self, form):

        roles = ['promotor', 'director', 'coordinador', 'tesorero', 'sistemas']

        if validar_roles(roles=roles):
            return super(PersonaDetail, self).form_valid(form)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class AlumnoCreateView(MyLoginRequiredMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = "registro_create.html"

    @method_decorator(permission_required('register.alumno_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):
            return super(AlumnoCreateView, self).get(request, args, kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.alumno_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def form_valid(self, form):

        logger.debug("Alumno a crear con DNI: " + form.cleaned_data["numero_documento"])

        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):
            alu = SaveGeneric().saveGeneric(padre=Profile, form=form, hijo=Alumno)
            logger.debug("Se creó el alumno en la vista")

            als = Alumno.objects.all()

            logger.info("Se creó el alumno")
            return HttpResponseRedirect(reverse('enrollments:filtrar_alumno'))
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class AlumnoDetail(MyLoginRequiredMixin, DetailView):
    model = Alumno
    template_name = "alumno_detail.html"

    @method_decorator(permission_required('register.alumno_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):
            return super(AlumnoDetail, self).get(request, args, kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class ApoderadoCreateView(MyLoginRequiredMixin, CreateView):
    model = Apoderado
    form_class = ApoderadoForm
    template_name = "registro_create.html"

    @method_decorator(permission_required('register.apoderado_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'coordinador']

        if validar_roles(roles=roles):
            return super(ApoderadoCreateView, self).get(request, args, kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.apoderado_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def form_valid(self, form):
        logger.debug("Apoderado a crear con DNI: " + form.cleaned_data["numero_documento"])

        roles = ['promotor', 'director', 'coordinador']

        if validar_roles(roles=roles):
            apoderado = SaveGeneric().saveGeneric(padre=Profile, form=form, hijo=Apoderado)
            logger.debug("Se creó el apoderado en la vista")

            logger.debug("Se creó el apoderado")
            return HttpResponseRedirect(apoderado.get_absolute_url())

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class ApoderadoDetailView(MyLoginRequiredMixin, DetailView):
    model = Apoderado
    template_name = "apoderado_detail.html"

    @method_decorator(permission_required('register.apoderado_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'coordinador']

        if validar_roles(roles=roles):

            return super(ApoderadoDetailView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class PersonalCreateView(MyLoginRequiredMixin, CreateView):
    model = Personal
    form_class = PersonalForm
    template_name = "personal_create.html"

    @method_decorator(permission_required('register.personal_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            return super(PersonalCreateView, self).get(request, args, kwargs)

        else:

            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.personal_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def form_valid(self, form):
        logger.debug("Personal a crear con DNI: " + form.cleaned_data["numero_documento"])

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            personal = SaveGeneric().saveGeneric(padre=Profile, form=form, hijo=Personal)
            logger.debug("Se creó el personal en la vista")

            logger.info("Se creó el personal")
            return HttpResponseRedirect(personal.get_absolute_url())

        else:

            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class PersonalDetailView(MyLoginRequiredMixin, DetailView):
    model = Personal
    template_name = "personal_detail.html"

    @method_decorator(permission_required('register.personal_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):
            return super(PersonalDetailView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class SistemasCreateView(MyLoginRequiredMixin, CreateView):
    model = Sistemas
    form_class = SistemasForm
    template_name = "registro_create.html"

    @method_decorator(permission_required('register.sistemas_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['sistemas', 'promotor']

        if validar_roles(roles=roles):
            return super(SistemasCreateView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.sistemas_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def form_valid(self, form):
        logger.debug("Sistemas a crear con DNI: " + form.cleaned_data["numero_documento"])

        roles = ['sistemas', 'promotor']

        if validar_roles(roles=roles):
            personal = SaveGeneric().saveGeneric(padre=Personal, form=form, hijo=Sistemas)
            logger.debug("Se creó el usuario de sistemas en la vista")

            logger.info("Se creó el usuario de sistemas")
            return HttpResponseRedirect(personal.get_absolute_url())

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class SistemasDetailView(MyLoginRequiredMixin, DetailView):
    model = Sistemas
    template_name = "sistemas_detail.html"

    @method_decorator(permission_required('register.sistemas_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['sistemas', 'promotor']

        if validar_roles(roles=roles):
            return super(SistemasDetailView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)



class PromotorCreateView(MyLoginRequiredMixin, CreateView):
    model = Promotor
    form_class = PromotorForm
    template_name = "registro_create.html"

    @method_decorator(permission_required('register.promotor_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['sistemas']

        if validar_roles(roles=roles):
            return super(PromotorCreateView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.promotor_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=True))
    def form_valid(self, form):
        logger.debug("Promotor a crear con DNI: " + form.cleaned_data["numero_documento"])

        roles = ['sistemas']

        if validar_roles(roles=roles):
            personal = SaveGeneric().saveGeneric(padre=Personal, form=form, hijo=Promotor)
            logger.debug("Se creó el promotor en la vista")

            logger.info("Se creó el promotor")
            return HttpResponseRedirect(personal.get_absolute_url())

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class PromotorDetailView(MyLoginRequiredMixin, DetailView):
    model = Promotor
    template_name = "promotor_detail.html"

    @method_decorator(permission_required('register.promotor_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['sistemas']

        if validar_roles(roles=roles):
            return super(PromotorDetailView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class DirectorCreateView(MyLoginRequiredMixin, CreateView):
    model = Director
    form_class = DirectorForm
    template_name = "registro_create.html"

    @method_decorator(permission_required('register.director_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['sistemas', 'promotor']

        if validar_roles(roles=roles):
            return super(DirectorCreateView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.director_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def form_valid(self, form):
        logger.debug("Director a crear con DNI: " + form.cleaned_data["numero_documento"])

        roles = ['sistemas', 'promotor']

        if validar_roles(roles=roles):
            personal = SaveGeneric().saveGeneric(padre=Personal, form=form, hijo=Director)
            logger.debug("Se creó el director en la vista")

            logger.info("Se creó el director")
            return HttpResponseRedirect(personal.get_absolute_url())

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class DirectorDetailView(MyLoginRequiredMixin, DetailView):
    model = Director
    template_name = "director_detail.html"

    @method_decorator(permission_required('register.director_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['sistemas', 'promotor']

        if validar_roles(roles=roles):
            return super(DirectorDetailView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class CajeroCreateView(MyLoginRequiredMixin, CreateView):
    model = Cajero
    form_class = CajeroForm
    template_name = "registro_create.html"

    @method_decorator(permission_required('register.cajero_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'tesorero']

        if validar_roles(roles=roles):
            return super(CajeroCreateView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.cajero_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def form_valid(self, form):
        logger.debug("Cajero a crear con DNI: " + form.cleaned_data["numero_documento"])

        roles = ['promotor', 'director', 'tesorero']

        if validar_roles(roles=roles):
            personal = SaveGeneric().saveGeneric(padre=Personal, form=form, hijo=Cajero)
            logger.debug("Se creó el cajero en la vista")

            logger.info("Se creó el Cajero")
            return HttpResponseRedirect(personal.get_absolute_url())

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class CajeroDetailView(MyLoginRequiredMixin, DetailView):
    model = Cajero
    template_name = "cajero_detail.html"

    @method_decorator(permission_required('register.cajero_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'tesorero']

        if validar_roles(roles=roles):
            return super(CajeroDetailView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class TesoreroCreateView(MyLoginRequiredMixin, CreateView):
    model = Tesorero
    form_class = TesoreroForm
    template_name = "registro_create.html"

    @method_decorator(permission_required('register.tesorero_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'sistemas']

        if validar_roles(roles=roles):
            return super(TesoreroCreateView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.tesorero_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def form_valid(self, form):
        logger.debug("Tesorero a crear con DNI: " + form.cleaned_data["numero_documento"])

        roles = ['promotor', 'director', 'sistemas']

        if validar_roles(roles=roles):
            personal = SaveGeneric().saveGeneric(padre=Personal, form=form, hijo=Tesorero)
            logger.debug("Se creó el tesorero en la vista")

            logger.info("Se creó el tesorero")
            return HttpResponseRedirect(personal.get_absolute_url())

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class TesoreroDetailView(MyLoginRequiredMixin, DetailView):
    model = Tesorero
    template_name = "tesorero_detail.html"

    @method_decorator(permission_required('register.tesorero_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'sistemas']

        if validar_roles(roles=roles):
            return super(TesoreroDetailView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedor_create.html"

    @method_decorator(permission_required('register.proveedor_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'tesorero']

        if validar_roles(roles=roles):
            return super(ProveedorCreateView, self).get(request, args, kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    #@method_decorator(permission_required('register.proveedor_create', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=True))
    def form_valid(self, form):

        roles = ['promotor', 'director', 'tesorero']

        if validar_roles(roles=roles):
            instance = form.save()
            instance.save()

            try:
                id_colegio = self.request.session.get('colegio')
                cole = Colegio.objects.get(pk=id_colegio)

                prov_col = ProveedorColegio()
                prov_col.colegio = cole
                prov_col.proveedor = instance
                prov_col.save()
            except Colegio.DoesNotExist:
                pass

            return HttpResponseRedirect(instance.get_absolute_url())

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class ProveedorUpdateView(MyLoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedor_create.html"

    @method_decorator(permission_required('register.proveedor_update', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):
            return super(ProveedorUpdateView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_success_url(self):
        return reverse_lazy('registers:proveedor_list')


class ProveedorDeleteView(MyLoginRequiredMixin, TemplateView):
    model = Profile

    @method_decorator(permission_required('register.proveedor_delete', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):
            proveedor = Proveedor.objects.get(pk=int(request.GET['idproveedor']))

            id_colegio = get_current_colegio()

            if id_colegio is None:

                provs = ProveedorColegio.objects.filter(proveedor=proveedor)

                for prov in provs:
                    prov.activo = False
                    prov.save()

            else:

                try:
                    prov = ProveedorColegio.objects.get(proveedor=proveedor, colegio__id_colegio=id_colegio, activo=True)

                    prov.activo = False
                    prov.save()

                except ProveedorColegio.DoesNotExist:
                    pass

            return HttpResponseRedirect(reverse('registers:proveedor_list'))

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class ProveedorDetailView(MyLoginRequiredMixin, DetailView):
    model = Proveedor
    template_name = "proveedor_detail.html"

    @method_decorator(permission_required('register.proveedor_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'tesorero']

        if validar_roles(roles=roles):
            return super(ProveedorDetailView, self).get(request, args, kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class PersonaDetailView(MyLoginRequiredMixin, DetailView):
    # model = Profile
    queryset = Profile.objects.select_related()
    template_name = "registro_detail.html"

    @method_decorator(permission_required('register.personal_detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'coordinador', 'tesorero', 'sistemas']

        if validar_roles(roles=roles):
            return super(PersonaDetailView, self).get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class PersonalDeleteView(MyLoginRequiredMixin, TemplateView):
    model = Profile

    @method_decorator(permission_required('register.personal_delete', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):
            persona = Profile.objects.get(id_persona=int(request.GET['idpersona']))
            perfil = request.GET['perfil']

            id_colegio = get_current_colegio()

            if id_colegio is None:

                if perfil == "Alumno":
                    alus = Matricula.objects.filter(alumno__persona=persona)

                    for alu in alus:
                        alu.activo = False
                        alu.save()
                else:
                    personales = PersonalColegio.objects.filter(personal__id_persona=persona.id_persona)

                    for personal in personales:
                        personal.activo = False
                        personal.save()
            else:

                if perfil == "Alumno":
                    alu = Matricula.objects.get(alumno__id_persona=persona.id_persona, colegio__id_colegio=id_colegio)

                    alu.activo = False
                    alu.save()
                else:
                    personal = PersonalColegio.objects.get(personal__id_persona=persona.id_persona, colegio__id_colegio=id_colegio)

                    personal.activo = False
                    personal.save()

            return HttpResponseRedirect(reverse('registers:personal_list'))

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class PersonalUpdateView(MyLoginRequiredMixin, UpdateView):
    model = Profile
    form_class = PersonaForm
    template_name = "registro_form.html"

    @method_decorator(permission_required('register.personal_update', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):
            return super(PersonalUpdateView, self).get(request, args, kwargs)

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    # @method_decorator(permission_required('register.personal_update', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def get_object(self, queryset=None):

        obj = Profile.objects.prefetch_related("direcciones").get(pk=self.kwargs['pk'])

        return obj

    def get_success_url(self):
        return reverse_lazy('registers:personal_list')


class ProveedorListView(MyLoginRequiredMixin, TemplateView):
    template_name = "proveedor_list.html"

    @method_decorator(permission_required('register.proveedor_list', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def post(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):
            colegio = get_current_colegio()

            nombres = request.POST["nombres"]


            if nombres:
                if colegio is None:
                    proveedores = Proveedor.objects.filter(Q(razon_social__icontains=nombres.upper()))

                else:
                    proveedores = Proveedor.objects.filter(
                                                       Q(razon_social__icontains=nombres.upper())
                                                       ).filter(proveedores__colegio=colegio, proveedores__activo=True)


            else:
                return self.get(request)

            paginator = Paginator(proveedores, 5)

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
                          {'proveedores': buscados,
                           'nombres': nombres})

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    @method_decorator(permission_required('register.proveedor_list', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):

            logger.debug("get_context")

            # Obtener el id del colegio
            id_colegio = get_current_colegio()
            logger.debug("colegio id: " + str(id_colegio))

            try:
                colegio = Colegio.objects.get(pk=id_colegio)
                logger.debug("colegio: " + str(colegio))

                # Obtener los empleados del colegio
                proveedores = Proveedor.objects.filter(proveedores__activo=True, proveedores__colegio=colegio).order_by('razon_social')
                logger.debug("cantidad de proveedores: " + str(proveedores.count()))

            except Colegio.DoesNotExist:
                # Obtener los empleados del colegio
                proveedores = Proveedor.objects.all().order_by('razon_social')
                logger.debug("cantidad de empleados: " + str(proveedores.count()))

            #for p in proveedores:
            #    result.append(p.proveedor)

            page = request.GET.get('page', 1)

            paginator = Paginator(proveedores, 5)

            try:
                provs = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                provs = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                provs = paginator.page(paginator.num_pages)

            logger.debug("Se cargo el contexto")
            return render(request, self.template_name, {'proveedores': provs})  # return context
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class PersonaListView(MyLoginRequiredMixin, TemplateView):
    template_name = "persona_list.html"

    @method_decorator(permission_required('register.personal_list', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def post(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):
            colegio = get_current_colegio()

            numero_documento = request.POST["numero_documento"]

            nombres = request.POST["nombres"]

            if numero_documento and not nombres:
                if colegio is None:
                    empleados = Profile.objects.filter(numero_documento=numero_documento,
                                                   personal__Colegios__activo=True)

                    alumnos = Matricula.objects.filter(alumno__numero_documento=numero_documento,
                                                       activo=True)

                else:
                    empleados = Profile.objects.filter(numero_documento=numero_documento,
                                                   personal__Colegios__id_colegio=colegio,
                                                   personal__Colegios__activo=True)

                    alumnos = Matricula.objects.filter(alumno__numero_documento=numero_documento,
                                                       activo=True, colegio__id_colegio=colegio)

            elif numero_documento and nombres:
                if colegio is None:
                    empleados = Profile.objects.filter(Q(numero_documento=numero_documento),
                                                       Q(nombre__icontains=nombres.upper()) |
                                                       Q(apellido_pa__icontains=nombres.upper()) |
                                                       Q(apellido_ma__icontains=nombres.upper())).filter(
                                                                personal__Colegios__activo=True)

                    alumnos = Matricula.objects.filter(Q(alumno__numero_documento=numero_documento),
                                                       Q(alumno__nombre__icontains=nombres.upper()) |
                                                       Q(alumno__apellido_pa__icontains=nombres.upper()) |
                                                       Q(alumno__pellido_ma__icontains=nombres.upper())).filter(activo=True)
                else:
                    empleados = Profile.objects.filter(Q(numero_documento=numero_documento),
                                                       Q(nombre__icontains=nombres.upper()) |
                                                       Q(apellido_pa__icontains=nombres.upper()) |
                                                       Q(apellido_ma__icontains=nombres.upper())).filter(personal__Colegios__id_colegio=colegio,
                                                                                                         personal__Colegios__activo=True)

                    alumnos = Matricula.objects.filter(Q(alumno__numero_documento=numero_documento),
                                                       Q(alumno__nombre__icontains=nombres.upper()) |
                                                       Q(alumno__apellido_pa__icontains=nombres.upper()) |
                                                       Q(alumno__apellido_ma__icontains=nombres.upper())).filter(colegio__id_colegio=colegio,
                                                                                                         activo=True)

            elif not numero_documento and nombres:
                if colegio is None:
                    empleados = Profile.objects.filter(Q(nombre__icontains=nombres.upper()) |
                                                       Q(apellido_pa__icontains=nombres.upper()) |
                                                       Q(apellido_ma__icontains=nombres.upper())).filter(
                                                                            personal__Colegios__activo=True)

                    alumnos = Matricula.objects.filter(Q(alumno__nombre__icontains=nombres.upper()) |
                                                       Q(alumno__apellido_pa__icontains=nombres.upper()) |
                                                       Q(alumno__apellido_ma__icontains=nombres.upper())).filter(activo=True)
                else:
                    empleados = Profile.objects.filter(Q(nombre__icontains=nombres.upper()) |
                                                       Q(apellido_pa__icontains=nombres.upper()) |
                                                       Q(apellido_ma__icontains=nombres.upper())).filter(personal__Colegios__id_colegio=colegio,
                                                                                                         personal__Colegios__activo=True)

                    alumnos = Matricula.objects.filter(Q(alumno__nombre__icontains=nombres.upper()) |
                                                       Q(alumno__apellido_pa__icontains=nombres.upper()) |
                                                       Q(alumno__apellido_ma__icontains=nombres.upper())).filter(colegio__id_colegio=colegio,activo=True)
            else:
                return self.get(request)

            resultado = []

            for al in alumnos:
                al.rol = "Alumno"
                resultado.append(al.alumno)

            for em in empleados:

                rol = ""

                try:
                    if em.personal.promotor:
                        rol = "Promotor "
                except Promotor.DoesNotExist:
                    pass

                try:
                    if em.personal.director:
                        rol = "Director "
                except Director.DoesNotExist:
                    pass

                try:
                    if em.personal.cajero:
                        rol = "Cajero "
                except Cajero.DoesNotExist:
                    pass

                try:
                    if em.personal.administrativo:
                        rol = "Administrativo "
                except Administrativo.DoesNotExist:
                    pass

                try:
                    if em.personal.tesorero:
                        rol = "Tesorero "
                except Tesorero.DoesNotExist:
                    pass

                em.rol = rol
                resultado.append(em)

            paginator = Paginator(resultado, 5)

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

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    @method_decorator(permission_required('register.personal_list', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):

        roles = ['promotor', 'director', 'coordinador', 'sistemas']

        if validar_roles(roles=roles):

            logger.debug("get_context")

            # Obtener el id del colegio
            id_colegio = get_current_colegio()
            logger.debug("colegio id: " + str(id_colegio))

            alumnos = []
            try:
                colegio = Colegio.objects.get(pk=id_colegio)
                logger.debug("colegio: " + str(colegio))

                # Obtener los empleados del colegio
                empleados = PersonalColegio.objects.filter(colegio=colegio, activo=True).all()
                logger.debug("cantidad de empleados: " + str(empleados.count()))

                alumnos = Matricula.objects.filter(colegio=colegio, activo=True).all()
                logger.debug("Cantidad de alumnos: " + str(alumnos.count()))

            except Colegio.DoesNotExist:
                # Obtener los empleados del colegio
                empleados = PersonalColegio.objects.filter(activo=True).all()
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


            # verificamos los alumnos matriculados
            for alumno in alumnos:
                alumno.alumno.persona.rol = "Alumno"
                personal.append(alumno.alumno.persona)
                # personal.append(alumno.alumno.apoderado)

            personal.sort(key=lambda x: x.getNombreCompleto.lower())

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
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class ColegioCreateView(MyLoginRequiredMixin, TemplateView):
    """

    """
    template_name = "colegio_create.html"
    model = Colegio
    form_class = ColegioForm

    @method_decorator(permission_required('register.colegio_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={
            'form': self.form_class,
        })

    @method_decorator(permission_required('register.colegio_create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        logger.info("En el POST")
        logger.info(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            logger.info(data_form)
            logger.info(form.data)

            colegio = Colegio(
                nombre=data_form['nombre'],
                ruc=data_form['ruc'],
                ugel=data_form['ugel']
            )
            colegio.save()
            direccion = Direccion(
                colegio= colegio,
                dpto= data_form['departamento'],
                calle= data_form['direccion'],
                referencia= data_form['referencia'],
                provincia= data_form['provincia'],
                distrito= data_form['distrito']
            )
            direccion.save()
            try:
                celulares = form.data['nros']
                lst_celulares = celulares.split(',')
                lista_numeros = []
                for cel in lst_celulares:
                    telef = Telefono(
                        colegio= colegio,
                        numero=cel,
                        tipo="Celular"
                    )
                    telef.save()
            except:
                logger.info("no se registraron numeros del colegio")
            logger.info("El formulario es valido")
            caja_chica = CajaChica(
                colegio= colegio,
                presupuesto= 0,
                saldo= 0,
                periodo=1,
            )
            caja_chica.save()
            return HttpResponseRedirect(reverse('registers:colegio_list'))
        return HttpResponseRedirect(reverse('registers:colegio_list'))


class ColegioListView(MyLoginRequiredMixin, TemplateView):
    model = Colegio
    template_name = 'colegio_list.html'

    @method_decorator(permission_required('register.colegio_list', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        colegios = Colegio.objects.all()

        return render(request, template_name=self.template_name, context={
            'colegios': colegios,
        })

