# coding=utf-8
# from . import forms
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.conf import settings
from datetime import date
from authtools.models import User
from discounts.forms import SolicitarDescuentoForm
from discounts.models import Descuento, TipoDescuento
from enrollment.models import Servicio
from enrollment.models import TipoServicio
from enrollment.models import Matricula
from enrollment.models import Cuentascobrar
from register.models import Colegio
from profiles.models import Profile
from register.models import Alumno
from register.models import Promotor, Administrativo, Director, PersonalColegio
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.core.urlresolvers import reverse_lazy
from enrollment.forms import ServicioRegularForm, ServicioRegularForm2, ServicioExtraCreateForm, \
    TipoServicioRegularNivelCompletoForm
from enrollment.forms import ServicioExtraForm
from enrollment.forms import TipoServicioRegularForm
from enrollment.forms import TipoServicioExtraForm
from enrollment.forms import MatriculaForm
from django.urls import reverse
from utils.models import TiposNivel
from utils.models import TiposGrados
from utils.views import get_current_colegio
from utils.middleware import get_current_user
from utils.middleware import get_current_userID
from utils.middleware import validar_roles

from utils.views import MyLoginRequiredMixin
import logging

# Create your views here.

logger = logging.getLogger("project")


# logger.info(dato) para mostrar los reportes de eventos
# logger.debug("usuario logueado: " + str(request.user.is_authenticated()))
# logger.debug("colegio: " + str(request.session.get('colegio')))
#################################################
#   CRUD (Create, Retrieve, Update, Delete)
#   Tipos de Servicios
#################################################

class TipoServicioListView(MyLoginRequiredMixin, ListView):
    """

    """
    model = TipoServicio
    template_name = "tiposervicio_list.html"

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoServicioListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):
        context = super(TipoServicioListView, self).get_context_data(**kwargs)
        tipos_de_servicios = self.model.objects.filter(colegio__id_colegio=self.request.session.get('colegio'))
        try:
            regulares = tipos_de_servicios.filter(is_ordinario=True, activo=True).order_by("nivel", "grado")
            regularesvacio = (regulares.count() is 0)
            extra = tipos_de_servicios.filter(is_ordinario=False, activo=True).order_by("nivel", "grado")
            extravacio = (extra.count() is 0)
        except:
            regulares = []
            regularesvacio = True
            extra = []
            extravacio = True

        context['serviciosregulares'] = regulares
        context['serviciosregularesvacio'] = regularesvacio
        context['serviciosextra'] = extra
        context['serviciosextravacio'] = extravacio
        return context

    def post(self, request, *args, **kwargs):
        tipos_de_servicios = self.model.objects.filter(colegio__id_colegio=self.request.session.get('colegio'))
        if request.POST['nivel'] is '4':
            regulares = tipos_de_servicios.filter(is_ordinario=True, activo=True).order_by("nivel", "grado")
        else:
            regulares = tipos_de_servicios.filter(nivel=int(request.POST['nivel']), activo=True).order_by("nivel",
                                                                                                          "grado")

        extra = tipos_de_servicios.filter(is_ordinario=False, activo=True).order_by("nivel", "grado")

        return render(request, template_name=self.template_name, context={
            'serviciosregulares': regulares,
            'serviciosextra': extra,
        })


class TipoServicioDetailView(MyLoginRequiredMixin, DetailView):
    """

    """
    model = TipoServicio
    template_name = "tiposervicio_detail.html"

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoServicioDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class TipoServicioRegularNivelCompletoCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    model = TipoServicio
    form_class = TipoServicioRegularNivelCompletoForm

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        # logger.info("En el POST")
        # logger.info(request.POST)
        # if form.is_valid():
        # data_form = form.cleaned_data
        nivel = request.POST['nivel_grados']
        nivel = int(nivel)
        cole_id = get_current_colegio()
        colegio = Colegio.objects.get(pk=cole_id)
        grados = TipoServicio.objects.filter(nivel=nivel, colegio_id=cole_id, activo=True)
        if len(grados) > 0:
            if nivel == 1:
                for k in [1, 2, 3]:
                    try:
                        grado_existente = grados.get(grado=k)
                    except:
                        tipo_servicio = TipoServicio(
                            nivel=nivel,
                            grado=k,
                            colegio=colegio,
                            is_ordinario=True,
                        )
                        tipo_servicio.save()
            elif nivel == 2:
                for k in [4, 5, 6, 7, 8, 9]:
                    try:
                        grado_existente = grados.get(grado=k)
                    except:
                        tipo_servicio = TipoServicio(
                            nivel=nivel,
                            grado=k,
                            colegio=colegio,
                            is_ordinario=True,
                        )
                        tipo_servicio.save()
            elif nivel == 3:
                for k in [10, 11, 12, 13, 14]:
                    try:
                        grado_existente = grados.get(grado=k)
                    except:
                        tipo_servicio = TipoServicio(
                            nivel=nivel,
                            grado=k,
                            colegio=colegio,
                            is_ordinario=True,
                        )
                        tipo_servicio.save()
        else:
            if nivel == 1:
                for k in [1, 2, 3]:
                    tipo_servicio = TipoServicio(
                        nivel=nivel,
                        grado=k,
                        colegio=colegio,
                        is_ordinario=True,
                    )
                    tipo_servicio.save()
            elif nivel == 2:
                for k in [4, 5, 6, 7, 8, 9]:
                    tipo_servicio = TipoServicio(
                        nivel=nivel,
                        grado=k,
                        colegio=colegio,
                        is_ordinario=True,
                    )
                    tipo_servicio.save()
            elif nivel == 3:
                for k in [10, 11, 12, 13, 14]:
                    tipo_servicio = TipoServicio(
                        nivel=nivel,
                        grado=k,
                        colegio=colegio,
                        is_ordinario=True,
                    )
                    tipo_servicio.save()

            return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))
        return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))


class TipoServicioRegularCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    model = TipoServicio
    form_class = TipoServicioRegularForm

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoServicioRegularCreateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def form_valid(self, form):
        form.instance.is_ordinario = True
        form.instance.colegio = Colegio.objects.get(pk=self.request.session.get('colegio'))
        cole_id = get_current_colegio()
        grado_prueba = form.instance.grado
        if TipoServicio.objects.filter(colegio_id=cole_id, grado=grado_prueba, activo=True).exists():
            # print("Existe. Se creo, pero no podrá ser usado")
            form.instance.activo = False
            return HttpResponse(
                "<script>alert('Este grado ya existe!!');window.history.back();</script>")

        else:
            """
            print ('No existe, fue creado con exito')
            """
            return super(TipoServicioRegularCreateView, self).form_valid(form)


class TipoServicioExtraCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    model = TipoServicio
    form_class = TipoServicioExtraForm

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoServicioExtraCreateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def form_valid(self, form):
        form.instance.is_ordinario = False
        form.instance.colegio = Colegio.objects.get(pk=self.request.session.get('colegio'))
        return super(TipoServicioExtraCreateView, self).form_valid(form)


class CargarTipoServicioCreateView(MyLoginRequiredMixin, TemplateView):
    """

    """
    template_name = "tiposervicio_form.html"
    model = TipoServicio
    form1 = TipoServicioRegularForm
    form2 = TipoServicioExtraForm
    form3 = TipoServicioRegularNivelCompletoCreateView

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            form1 = self.form1
            form2 = self.form2
            form3 = self.form3
            return render(request, template_name=self.template_name, context={
                'form1': form1,
                'form2': form2,
                'form3': form3,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class TipoServicioRegularEndUpdateView(MyLoginRequiredMixin, UpdateView):
    """

    """
    model = TipoServicio
    form_class = TipoServicioRegularForm

    # template_name = "tiposervicioregular_form.html"
    def get_success_url(self):
        return reverse_lazy('enrollments:tiposervicio_list')


class TipoServicioRegularUpdateView(MyLoginRequiredMixin, TemplateView):
    template_name = "tiposervicioregular_form.html"
    model = TipoServicio
    form_class = TipoServicioRegularForm

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            pk_tiposervicio = int(request.POST["tiposervicio"])
            grado_pk = TipoServicio.objects.values('grado').filter(pk=pk_tiposervicio)[0]['grado']
            # print('==============================')
            # print('id_tiposervicio : ' + str(pk_tiposervicio))
            # print('id_grado dentro de la tabla TipoServicio :  ' + str(grado_pk))
            # print('==============================')

            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'value': grado_pk,

            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        tiposervicio = self.model.objects.get(pk=request.POST["tiposervicio"])
        form = self.form_class(instance=tiposervicio)

        pk_tiposervicio = int(request.POST["tiposervicio"])
        grado_pk = TipoServicio.objects.values('grado').filter(pk=pk_tiposervicio)[0]['grado']
        nivel_pk = TipoServicio.objects.values('nivel').filter(pk=pk_tiposervicio)[0]['nivel']

        # print('==============================')
        # print('id_tiposervicio : ' + str(pk_tiposervicio))
        # print('id_grado dentro de la tabla TipoServicio :  ' + str(grado_pk))
        # print('id_nivel dentro de la tabla TipoServicio :  ' + str(nivel_pk))
        # print('==============================')


        return render(request, template_name=self.template_name, context={
            'form': form,
            'grado_value': grado_pk,
            'nivel_value': nivel_pk,
            'idtipo': request.POST['tiposervicio'],
        })


class TipoServicioExtraEndUpdateView(MyLoginRequiredMixin, UpdateView):
    """

    """
    model = TipoServicio
    form_class = TipoServicioExtraForm

    # template_name = "tiposervicioregular_form.html"
    def get_success_url(self):
        return reverse_lazy('enrollments:tiposervicio_list')


class TipoServicioExtraUpdateView(MyLoginRequiredMixin, TemplateView):
    template_name = "tiposervicioextra_form.html"
    model = TipoServicio
    form_class = TipoServicioExtraForm

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoServicioExtraUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        tiposervicio = self.model.objects.get(pk=request.POST["tiposervicio"])
        form = self.form_class(instance=tiposervicio)
        return render(request, template_name=self.template_name, context={
            'form': form,
            'idtipo': request.POST['tiposervicio'],
        })


class TipoServicioDeleteView(MyLoginRequiredMixin, TemplateView):
    """

    """
    model = TipoServicio
    template_name = "tiposervicio_confirm_delete.html"

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            tiposervicio = self.model.objects.get(pk=int(request.GET['tiposervicio']))
            for servicio in tiposervicio.getServiciosAsociados():
                servicio.activo = False
                servicio.save()
            tiposervicio.activo = False
            tiposervicio.save()
            return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        return render(request, template_name=self.template_name, context={
            'idtipo': request.POST['tiposervicio'],
        })


##########################################################
#   CRUD (Create, Retrieve, Update, Delete)
#   Servicios
##########################################################

class ServicioListView(MyLoginRequiredMixin, ListView):
    """

    """
    model = Servicio
    template_name = "servicio_list.html"

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(ServicioListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_queryset(self):
        return self.model.objects.filter(tipo_servicio=self.kwargs["pkts"])
        # def get_context_data(self, **kwargs):
        #    context = super(ServicioList, self).get_context_data(**kwargs)
        #    return context


class ServicioDetailView(MyLoginRequiredMixin, DetailView):
    """

    """
    model = Servicio
    template_name = "servicio_detail.html"

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(ServicioDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class ServicioRegularCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    model = Servicio
    form_class = ServicioRegularForm2
    template_name = "servicioregular_form.html"

    def form_valid(self, form):

        tipo_prueba = form.instance.tipo_servicio
        if Servicio.objects.filter(tipo_servicio=tipo_prueba, nombre=self.request.POST["nombre"], activo=True).exists():
            # print("Existe. Se creo, pero no podrá ser usado")
            form.instance.activo = False
        else:
            """
            print ('No existe, fue creado con exito')
            """
        print(self.request.POST['fecha_facturar'])
        if self.request.POST["nombre"] == 'Pension':
            form.instance.cuotas = 10
        else:
            form.instance.cuotas = 1

        if self.request.POST["nombre"] == 'Pension':
            form.instance.is_periodic = True
        else:
            form.instance.is_periodic = False
        return super(ServicioRegularCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('enrollments:tiposervicio_list')

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return render(request, template_name=self.template_name, context={
                'tiposervicio': TipoServicio.objects.filter(is_ordinario=True, activo=True,
                                                            colegio_id=get_current_colegio()).order_by("nivel",
                                                                                                       "grado"),
                'form': self.form_class,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class ServicioRegularNivelCompletoCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    model = Servicio

    # form_class = TipoServicioRegularNivelCompletoForm

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        # logger.info("En el POST")
        # logger.info(request.POST)
        # if form.is_valid():
        # data_form = form.cleaned_data
        nivel = request.POST['nivel_grados']
        nivel = int(nivel)
        nombre = request.POST['nombre']
        precio = float(request.POST['precio'])
        fecha = request.POST['fecha_facturar']
        cole_id = get_current_colegio()
        colegio = Colegio.objects.get(pk=cole_id)
        grados = TipoServicio.objects.filter(nivel=nivel, colegio_id=cole_id, activo=True)
        for grado in grados:

            if not Servicio.objects.filter(tipo_servicio=grado, nombre=nombre, activo=True).exists():

                if nombre == "Pension":
                    servicio = Servicio(
                        nombre=nombre,
                        tipo_servicio=grado,
                        precio=precio,
                        is_periodic=True,
                        fecha_facturar=fecha,
                        cuotas=10,
                    )
                    servicio.save()
                else:
                    servicio = Servicio(
                        nombre=nombre,
                        tipo_servicio=grado,
                        precio=precio,
                        is_periodic=True,
                        fecha_facturar=fecha,
                        cuotas=1,
                    )
                    servicio.save()
        return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))


class ServicioExtraCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    model = Servicio
    form_class = ServicioExtraCreateForm
    template_name = "servicioextra_form.html"

    def form_valid(self, form):
        if self.request.POST["nombre"] == 'Pension':
            form.instance.cuotas = 10
            form.instance.is_periodic = True
        else:
            form.instance.cuotas = 1
            form.instance.is_periodic = False

        return super(ServicioExtraCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('enrollments:tiposervicio_list')

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return render(request, template_name=self.template_name, context={
                'tiposervicio': TipoServicio.objects.filter(is_ordinario=False, activo=True,
                                                            colegio_id=get_current_colegio()),
                'form': self.form_class,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class ServicioRegularEndUpdateView(MyLoginRequiredMixin, TemplateView):
    """

    """
    model = Servicio
    form_class = ServicioRegularForm
    template_name = "servicioregular_update_form.html"

    def get_success_url(self):
        return reverse_lazy('enrollments:tiposervicio_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        logger.info("En el POST")
        logger.info(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            servicio = self.model.objects.get(pk=request.POST['idser'])
            servicio.cuotas = data_form['cuotas']
            servicio.nombre = data_form['nombre']
            servicio.fecha_facturar = data_form['fecha_facturar']
            servicio.precio = data_form['precio']
            servicio.save()
            logger.info("El formulario es valido")
            return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))
        return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))


class ServicioRegularUpdateView(MyLoginRequiredMixin, TemplateView):
    template_name = "servicioregular_update_form.html"
    model = Servicio
    form_class = ServicioRegularForm

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(ServicioRegularUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        servicio = self.model.objects.get(pk=request.POST["idser"])
        form = self.form_class(instance=servicio)

        pk_servicio = int(request.POST['idser'])
        Tiposervicio_pk = Servicio.objects.values('tipo_servicio_id').filter(pk=pk_servicio)[0]['tipo_servicio_id']
        grado_pk = TipoServicio.objects.values('grado').filter(pk=Tiposervicio_pk)[0]['grado']
        print('==============================')
        print('id_servicio : ' + str(pk_servicio))
        print('id_tipo_servicio dentro de la tabla servicio :  ' + str(Tiposervicio_pk))
        print('obtener el grado dentro de la tabla tipo_servicio :  ' + str(grado_pk))

        return render(request, template_name=self.template_name, context={
            'tiposervicio': servicio.tipo_servicio,
            'form': form,
            'idser': int(request.POST['idser']),
        })


class ServicioExtraEndUpdateView(MyLoginRequiredMixin, TemplateView):
    """

    """
    model = Servicio
    form_class = ServicioExtraForm
    template_name = "servicioextra_update_form.html"

    def get_success_url(self):
        return reverse_lazy('enrollments:tiposervicio_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        logger.info("En el POST")
        logger.info(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            servicio = self.model.objects.get(pk=request.POST['idser'])
            servicio.cuotas = data_form['cuotas']
            servicio.nombre = data_form['nombre']
            servicio.fecha_facturar = data_form['fecha_facturar']
            servicio.precio = data_form['precio']
            servicio.save()
            logger.info("El formulario es valido")
            return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))
        return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))


class ServicioExtraUpdateView(MyLoginRequiredMixin, TemplateView):
    model = Servicio
    form_class = ServicioExtraForm
    template_name = "servicioextra_update_form.html"

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoServicioExtraUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        servicio = self.model.objects.get(pk=request.POST["idser"])
        form = self.form_class(instance=servicio)
        return render(request, template_name=self.template_name, context={
            'tiposervicio': servicio.tipo_servicio,
            'form': form,
            'idser': (request.POST['idser']),
        })


class ServicioDeleteView(MyLoginRequiredMixin, TemplateView):
    """

    """
    model = Servicio
    template_name = "servicio_confirm_delete.html"

    @method_decorator(permission_required('enrollment.Tipo_Servicio_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            servicio = self.model.objects.get(pk=request.GET['idser'])
            servicio.activo = False
            servicio.save()
            return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        logger.info(request.POST)
        logger.info(request.POST['idser'])
        return render(request, template_name=self.template_name, context={
            'idser': int(request.POST['idser']),
        })


#################################################
#
#
#################################################

class MatriculaListView(MyLoginRequiredMixin, ListView):
    """

    """
    model = Matricula
    template_name = "matricula_list.html"

    # colegio = get_current_colegio()
    # queryset = Matricula.objects.filter(colegio=colegio)

    @method_decorator(permission_required('enrollment.Matricula_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            matriculados = Matricula.objects.filter(colegio_id=self.request.session.get('colegio'), activo=True)
            return render(request, template_name=self.template_name, context={
                'matriculados': matriculados,
            })
            return super(MatriculaListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

            # def get_queryset(self):
            #    return self.model.objects.filter(tipo_servicio = self.kwargs["pkts"])
            # def get_context_data(self,request, **kwargs):
            #    context = super(ServicioList, self).get_context_data(**kwargs)
            #    return context


class MatriculaDetailView(MyLoginRequiredMixin, DetailView):
    """

    """
    model = Matricula
    template_name = "matricula_detail.html"

    @method_decorator(permission_required('enrollment.Matricula_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(MatriculaDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class MatriculaCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    model = Matricula
    form_class = MatriculaForm
    template_name = "matricula_form.html"

    def form_valid(self, form):
        logger.info("Se ejecuto")
        form.instance.colegio = Colegio.objects.get(pk=self.request.session.get('colegio'))
        return super(MatriculaCreateView, self).form_valid(form)

    @method_decorator(permission_required('enrollment.Matricula_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):

            list_tiposervicio = []
            alumno = Alumno.objects.get(pk=request.GET["alumno"])
            matricula = Matricula.objects.filter(alumno=alumno, activo=True, colegio__tiposervicio__is_ordinario=True)
            if matricula.count() > 0:
                tiposervicios = TipoServicio.objects.filter(colegio_id=self.request.session.get('colegio'), activo=True,
                                                            is_ordinario=False)
            else:
                tiposervicios = TipoServicio.objects.filter(colegio_id=self.request.session.get('colegio'), activo=True)
            if tiposervicios.count() > 1:
                for tiposer in tiposervicios:
                    if Servicio.objects.filter(tipo_servicio=tiposer, activo=True).count() > 0:
                        list_tiposervicio.append(tiposer)
            elif tiposervicios.count() is 1:
                if Servicio.objects.filter(tipo_servicio=tiposervicios, activo=True).count() > 0:
                    list_tiposervicio.append(tiposervicios)

            return render(request, template_name=self.template_name, context={
                'alumno': alumno,
                'tiposervicio': list_tiposervicio,
                'form': self.form_class,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        logger.debug("POST")

        form = self.form_class(request.POST)
        logger.debug("leer datos request post")

        if form.is_valid():
            logger.debug("Formulario valido")

            data_form = form.cleaned_data
            logger.debug("form en dict")
            logger.debug(data_form)

            matricula = Matricula(alumno=data_form["alumno"],
                                  colegio_id=self.request.session.get('colegio'),
                                  tipo_servicio=data_form["tipo_servicio"]
                                  )
            matricula.save()
            logger.debug(matricula)
            logger.info(matricula)

            estado = self.CrearCuentasCobrar(data_form, matricula)
            logger.debug("se creo la cuantas {0}".format(estado))

            return HttpResponseRedirect(matricula.get_absolute_url())

        return HttpResponseRedirect(reverse('enrollments:matricula_create'))

    def CrearCuentasCobrar(self, data_form, matricula):
        """
        Este metodo permite generar las Cuantas por Cobrar producto de una matricula
        :param data_form: datos del formulario de matricula como diccionario
        :param matricula: objeto matricula que tiene la relacion de Alumno, Colegio, Tipo de Servicio
        :return: retorna un mensaje de exito al concluir el metodo
        """
        logger.debug("Inicio de metodo CrearCuantasCobrar")
        logger.info("Inicio de metodo CrearCuantasCobrar")

        list_servicios = Servicio.objects.filter(tipo_servicio_id=data_form["tipo_servicio"])
        logger.debug(list_servicios.all())
        logger.info(list_servicios.all())

        fecha_actual = date.today()

        for servicio in list_servicios:
            logger.debug("inicia la lecturas de las cuentas")
            logger.info(servicio)

            fecha_facturar = servicio.fecha_facturar
            if fecha_actual.year == fecha_facturar.year:
                if fecha_facturar.month < fecha_actual.month:
                    fecha_facturar = fecha_facturar.replace(month=fecha_actual.month)
                logger.info("la fecha a facturar es: {0}".format(fecha_facturar))

            if servicio.is_periodic:
                logger.debug(str(servicio.is_periodic))
                logger.info("El servicio es periodico {0}".format(servicio.is_periodic))

                if (servicio.fecha_facturar.month < fecha_actual.month) and (fecha_actual.year == fecha_facturar.year):
                    numero_cuotas = servicio.cuotas - (fecha_actual.month - servicio.fecha_facturar.month)
                else:
                    numero_cuotas = servicio.cuotas

                for cuota in range(numero_cuotas):
                    logger.info("El servicio tiene {0} cuotas".format(servicio.cuotas))
                    logger.info("El servicio cobrara {0} cuotas".format(numero_cuotas))
                    logger.debug("Cuota Nro. {0}".format(cuota))

                    if (fecha_facturar.month + cuota) < 13:
                        try:
                            fecha_vencimiento = fecha_facturar.replace(month=fecha_facturar.month + cuota)
                        except:
                            k = 1
                            dia = fecha_facturar.day
                            while True:
                                try:
                                    fecha_vencimiento = fecha_facturar.replace(month=fecha_facturar.month + cuota,
                                                                               day=(dia - k))
                                    break
                                except:
                                    k = k + 1

                        cuentas = Cuentascobrar(matricula=matricula,
                                                servicio=servicio,
                                                fecha_ven=fecha_vencimiento,
                                                estado=True,
                                                precio=servicio.precio,
                                                deuda=servicio.precio,
                                                descuento=0,
                                                )
                        logger.debug(cuentas.matricula)
                        logger.info(cuentas.matricula)

                        cuentas.save()

            else:
                logger.debug(str(servicio.is_periodic))
                logger.info("El servicio es periodico {0}".format(servicio.is_periodic))

                cuentas = Cuentascobrar(matricula=matricula,
                                        servicio=servicio,
                                        fecha_ven=servicio.fecha_facturar,
                                        estado=True,
                                        precio=servicio.precio,
                                        deuda=servicio.precio,
                                        descuento=0
                                        )
                cuentas.save()

        return "Exito"


class MatriculaUpdateView(MyLoginRequiredMixin, UpdateView):
    """

    """
    model = Matricula
    form_class = MatriculaForm
    template_name = "matricula_form.html"

    @method_decorator(permission_required('enrollment.Matricula_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(MatriculaUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        logger.debug("POST")

        form = self.form_class(request.POST)
        logger.debug("leer datos request post")
        matricula = Matricula.objects.get(id_matricula=request.POST["matricula"])
        if form.is_valid():
            logger.debug("Formulario valido")

            data_form = form.cleaned_data
            logger.debug("form en dict")
            logger.debug(data_form)

            matricula.tipo_servicio = data_form["tipo_servicio"]
            matricula.save()
            logger.debug(matricula)
            logger.info(matricula)

            estado = self.CrearCuentasCobrar(data_form, matricula)
            logger.debug("se creo la cuantas {0}".format(estado))

            return HttpResponseRedirect(matricula.get_absolute_url())

        return HttpResponseRedirect(reverse('enrollments:matricula_create'))

    def CrearCuentasCobrar(self, data_form, matricula):
        """
        Este metodo permite generar las Cuantas por Cobrar producto de una matricula
        :param data_form: datos del formulario de matricula como diccionario
        :param matricula: objeto matricula que tiene la relacion de Alumno, Colegio, Tipo de Servicio
        :return: retorna un mensaje de exito al concluir el metodo
        """
        logger.debug("Inicio de metodo CrearCuantasCobrar")
        logger.info("Inicio de metodo CrearCuantasCobrar")

        list_servicios = Servicio.objects.filter(tipo_servicio_id=data_form["tipo_servicio"])
        logger.debug(list_servicios.all())
        logger.info(list_servicios.all())

        fecha_actual = date.today()

        for servicio in list_servicios:
            logger.debug("inicia la lecturas de las cuentas")
            logger.info(servicio)

            fecha_facturar = servicio.fecha_facturar
            if fecha_facturar.month < fecha_actual.month:
                fecha_facturar = fecha_facturar.replace(month=fecha_actual.month)
            logger.info("la fecha a facturar es: {0}".format(fecha_facturar))

            if servicio.is_periodic:
                logger.debug(str(servicio.is_periodic))
                logger.info("El servicio es periodico {0}".format(servicio.is_periodic))

                if servicio.fecha_facturar.month < fecha_actual.month:
                    numero_cuotas = servicio.cuotas - (fecha_actual.month - servicio.fecha_facturar.month)
                else:
                    numero_cuotas = servicio.cuotas

                for cuota in range(numero_cuotas):
                    logger.info("El servicio tiene {0} cuotas".format(servicio.cuotas))
                    logger.info("El servicio cobrara {0} cuotas".format(numero_cuotas))
                    logger.debug("Cuota Nro. {0}".format(cuota))

                    if (fecha_facturar.month + cuota) < 13:
                        fecha_vencimiento = fecha_facturar.replace(month=fecha_facturar.month + cuota)
                        cuentas = Cuentascobrar(matricula=matricula,
                                                servicio=servicio,
                                                fecha_ven=fecha_vencimiento,
                                                estado=True,
                                                precio=servicio.precio,
                                                deuda=servicio.precio,
                                                descuento=0,
                                                )
                        logger.debug(cuentas.matricula)
                        logger.info(cuentas.matricula)

                        cuentas.save()

            else:
                logger.debug(str(servicio.is_periodic))
                logger.info("El servicio es periodico {0}".format(servicio.is_periodic))

                cuentas = Cuentascobrar(matricula=matricula,
                                        servicio=servicio,
                                        fecha_ven=servicio.fecha_facturar,
                                        estado=True,
                                        precio=servicio.precio,
                                        deuda=servicio.precio,
                                        descuento=0
                                        )
                cuentas.save()

        return "Exito"


class CargarMatriculaUpdateView(MyLoginRequiredMixin, TemplateView):
    template_name = "matricula_form_update.html"
    model = Matricula
    form_class = MatriculaForm

    @method_decorator(permission_required('enrollment.Matricula_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(CargarMatriculaUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        matricula = self.model.objects.get(pk=request.POST["matricula"])
        form = self.form_class(instance=matricula)
        tiposervicios = TipoServicio.objects.filter(colegio_id=self.request.session.get('colegio'), activo=True)
        list_tiposervico = []
        for tiposer in tiposervicios:
            if Servicio.objects.filter(tipo_servicio=tiposer, activo=True).count() > 0:
                list_tiposervico.append(tiposer)

        return render(request, template_name=self.template_name, context={
            'form': form,
            'alumno': matricula.alumno,
            'tiposerviciolist': list_tiposervico,
            'matricula': matricula,
        })


class MatriculaDeleteView(MyLoginRequiredMixin, DeleteView):
    """

    """
    model = Matricula
    template_name = "matricula_confirm_delete.html"

    @method_decorator(permission_required('enrollment.Matricula_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            matricula = self.model.objects.get(pk=request.GET['matricula'])
            matricula.activo = False
            matricula.save()
            fecha_actual = date.today()
            cuentas = Cuentascobrar.objects.filter(matricula=matricula)
            for cuenta in cuentas:
                if cuenta.fecha_ven.month >= fecha_actual.month:
                    cuenta.activo = False
                    cuenta.save()
            return HttpResponseRedirect(reverse('enrollments:matricula_list'))

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_success_url(self):
        # tiposervicio = self.object.tipo_servicio
        return reverse('enrollments:matricula_list')


class FiltrarAlumnoView(ListView):
    """
    Este View permite filtrar a los alumnos por nombre y/o apellido
    """
    model = Alumno
    template_name = "alumno_form.html"

    def get(self, request, *args, **kwargs):
        personas = Profile.objects.filter(personal__Colegios__id_colegio=get_current_colegio())
        id_personas = []
        for persona in personas:
            id_personas.append(persona.user_id)
        print(id_personas)
        lista_alumnos = []
        for id_persona in id_personas:
            lista_alumnos.extend(Alumno.objects.filter(usuario_creacion_persona=id_persona))
        # usuarios = personas.user_id
        return render(request, template_name=self.template_name, context={
            'object_list': lista_alumnos,
            # 'object_list': Alumno.objects.all(),
        })

    def post(self, request, *args, **kwargs):

        # object_list_alumnos1 =  self.model.objects.filter(nombre=request.POST["nombre"])
        nombre = request.POST["nombre"]
        object_list_alumnos1 = []
        object_list_alumnos1.extend(Alumno.objects.filter(nombre__icontains=nombre.upper()))
        object_list_alumnos1.extend(Alumno.objects.filter(segundo_nombre__icontains=nombre.upper()))
        apellido_pa = request.POST["nombre"]
        # object_list_alumnos2 = self.model.objects.filter(apellido_pa=request.POST["apellido_pa"])
        object_list_alumnos2 = []
        object_list_alumnos2.extend(Alumno.objects.filter(apellido_pa__icontains=apellido_pa.upper()))
        object_list_alumnos2.extend(Alumno.objects.filter(apellido_ma__icontains=apellido_pa.upper()))
        dni = request.POST["dni"]
        object_list_alumnos3 = Alumno.objects.filter(numero_documento=dni)
        # object_list_alumnos3 = self.model.objects.filter(nombre=request.POST["nombre"],apellido_pa=request.POST["apellido_pa"])

        if len(object_list_alumnos3) is not 0:
            return render(request, template_name=self.template_name, context={
                'object_list': object_list_alumnos3,
                'dni': dni,
                'nombre': nombre,
            })
        elif len(object_list_alumnos1) is not 0:
            return render(request, template_name=self.template_name, context={
                'object_list': object_list_alumnos1,
                'dni': dni,
                'nombre': nombre,
            })
        elif len(object_list_alumnos2) is not 0:
            return render(request, template_name=self.template_name, context={
                'object_list': object_list_alumnos2,
                'dni': dni,
                'nombre': nombre,
            })
        else:
            return render(request, template_name=self.template_name, context={
                'object_list': [],
                'dni': dni,
                'nombre': nombre,
            })


class CargarMatriculaCreateView(TemplateView):
    template_name = "matricula_form.html"
    model = Alumno
    form_class = MatriculaForm

    def post(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):

            list_tiposervicio = []
            alumno = Alumno.objects.get(pk=request.POST["alumno"])
            matricula = Matricula.objects.filter(alumno=alumno, activo=True, colegio__tiposervicio__is_ordinario=True)
            if matricula.count() > 0:
                tiposervicios = TipoServicio.objects.filter(colegio_id=self.request.session.get('colegio'), activo=True,
                                                            is_ordinario=False).order_by("nivel", "grado")
            else:
                tiposervicios = TipoServicio.objects.filter(colegio_id=self.request.session.get('colegio'),
                                                            activo=True).order_by("nivel", "grado")
            if tiposervicios.count() > 1:
                for tiposer in tiposervicios:
                    if Servicio.objects.filter(tipo_servicio=tiposer, activo=True).count() > 0:
                        list_tiposervicio.append(tiposer)
            elif tiposervicios.count() is 1:
                if Servicio.objects.filter(tipo_servicio=tiposervicios, activo=True).count() > 0:
                    list_tiposervicio = tiposervicios

            return render(request, template_name=self.template_name, context={
                'alumno': alumno,
                'tiposerviciolist': list_tiposervicio,
                'form': self.form_class,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


#######################################################
#       Descuentos
#######################################################

class SolicitarDescuentoView(MyLoginRequiredMixin, TemplateView):
    model = Descuento
    template_name = "solicitar_descuento.html"
    form_class = SolicitarDescuentoForm

    def post(self, request, *args, **kwargs):
        descuentos = TipoDescuento.objects.filter(colegio__id_colegio=get_current_colegio(), activo=True)
        logger.info("Solicitar descuentos")
        return render(request, template_name=self.template_name, context={
            'form': self.form_class,

            'descuentos': descuentos,
            'alumno': Matricula.objects.get(pk=request.POST['matricula']),
        })


class CrearSolicitudView(MyLoginRequiredMixin, TemplateView):
    model = Descuento
    form_class = SolicitarDescuentoForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        logger.info(form)

        data_form = form.cleaned_data
        logger.info(data_form)
        solicitud = Descuento(
            personal_colegio=PersonalColegio.objects.get(personal__user=request.user),
            estado=1,
            fecha_solicitud=date.today(),
            matricula=data_form['matricula'],
            comentario=data_form['comentario'],
            tipo_descuento=data_form['tipo_descuento'],
            numero_expediente=data_form['numero_expediente'],
            fecha_aprobacion=date.today()
        )
        solicitud.save()

        return HttpResponseRedirect(reverse('enrollments:matricula_list'))


########################################################
#       Generacion de PDF
########################################################

from io import BytesIO

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A6
from reportlab.platypus import Table


def generar_pdf(request):
    print("Genero el PDF")
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "clientes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A6,
                            rightMargin=0,
                            leftMargin=0,
                            topMargin=0,
                            bottomMargin=0,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Clientes", styles['Heading1'])
    clientes.append(header)
    headings = ('Activo', 'Fecha Creacion', 'Fecha Modificacion')
    allclientes = [(p.activo, p.fecha_creacion, p.fecha_modificacion) for p in TipoServicio.objects.all()]
    print(allclientes)

    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response
