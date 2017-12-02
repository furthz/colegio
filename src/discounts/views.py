from datetime import date, datetime
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse

from payments.models import TipoPago
from utils.views import MyLoginRequiredMixin
from discounts.models import Descuento
from discounts.models import TipoDescuento
from enrollment.models import Servicio
from enrollment.models import Matricula
from enrollment.models import Cuentascobrar
from income.models import obtener_mes
from register.models import Colegio, Personal, Promotor
from register.models import PersonalColegio
from discounts.forms import SolicitarDescuentoForm
from discounts.forms import TipoDescuentForm
from discounts.forms import DetalleDescuentosForm
from utils.middleware import get_current_colegio, get_current_userID, get_current_user, validar_roles
from profiles.models import Profile
import logging

# Create your views here.

logger = logging.getLogger("project")

# logger.info(dato) para mostrar los reportes de eventos
# logger.debug("usuario logueado: " + str(request.user.is_authenticated()))
# logger.debug("colegio: " + str(request.session.get('colegio')))
#################################################
#       Solicitar Descuentos
#################################################
"""
class SolicitarDescuentoView(MyLoginRequiredMixin,TemplateView):
    model = Descuento
    template_name = "solicitar_descuento.html"
    form_class = SolicitarDescuentoForm



    def post(self, request, *args, **kwargs):

        descuentos = TipoDescuento.objects.filter(colegio__id_colegio=get_current_colegio(),activo = True)
        cole = Colegio.objects.get(id_colegio=get_current_colegio())
        logger.info("Solicitar descuentos")
        return render(request, template_name=self.template_name, context={
            #'form': self.form_class,


            'hola':cole,
            #'hola':cole,
            'descuentos':descuentos,
            #'alumno': Matricula.objects.get(pk=request.POST['matricula']),
        })

"""

class CrearSolicitudView(MyLoginRequiredMixin,TemplateView):
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

class TipoDescuentoCreateView(MyLoginRequiredMixin,CreateView):
    model = TipoDescuento
    template_name = "tipo_descuento.html"
    form_class = TipoDescuentForm
    #success_url = reverse('enrollments:matricula_list')
    def get_success_url(self):
        return reverse_lazy('enrollments:matricula_list')

    def form_valid(self, form):
        form.instance.colegio = Colegio.objects.get(pk = self.request.session.get('colegio'))
        return super(TipoDescuentoCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director','administrativo']

        if validar_roles(roles=roles):
            form = self.form_class(colegio=get_current_colegio())
            servicios = Servicio.objects.filter(tipo_servicio__colegio__id_colegio=get_current_colegio(), activo=True)
            return render(request, template_name=self.template_name, context={
                'form': form,
                'servicios': servicios,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class TipoDescuentoListView(MyLoginRequiredMixin, ListView):

    model = TipoDescuento
    template_name = "tipo_descuento_list.html"

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'cajero']

        if validar_roles(roles=roles):
            descuentos = TipoDescuento.objects.filter(colegio_id=get_current_colegio(), activo=True)

            return render(request, template_name=self.template_name, context={
                'descuentos': descuentos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class TipoDescuentoUpdateView(MyLoginRequiredMixin, UpdateView):
    model = TipoDescuento
    template_name = "tipo_descuento_update.html"
    form_class = TipoDescuentForm

    def post(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'cajero']

        if validar_roles(roles=roles):
            form = self.form_class(colegio=get_current_colegio())
            servicios = Servicio.objects.filter(tipo_servicio__colegio__id_colegio=get_current_colegio(), activo=True)
            tipo_descuento = TipoDescuento.objects.get(id_tipo_descuento=request.POST["id_descuento"])
            return render(request, template_name=self.template_name, context={
                'form': form,
                'servicios': servicios,
                'tipo_descuento': tipo_descuento,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class TipoDescuentoUpdateEndView(MyLoginRequiredMixin, UpdateView):
    model = TipoDescuento
    template_name = "tipo_descuento_update.html"
    form_class = TipoDescuentForm

    def post(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'cajero']

        if validar_roles(roles=roles):

            tipo_descuento = TipoDescuento.objects.get(id_tipo_descuento=request.POST["id_tipo_descuento"])
            tipo_descuento.servicio = Servicio.objects.get(id_servicio= request.POST["servicio"])
            tipo_descuento.descripcion = request.POST["descripcion"]
            tipo_descuento.porcentaje = request.POST["porcentaje"]
            tipo_descuento.save()
            return HttpResponseRedirect(reverse("discounts:tipo_descuento_list"))
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class TipoDescuentoDeleteView(MyLoginRequiredMixin, TemplateView):
    """

    """
    model = TipoDescuento
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



#################################################
#       Aprobar Descuentos
#################################################

class AprobarDescuentoView(ListView):

    model = Descuento
    template_name = "aprobar_descuento.html"

    @method_decorator(
        permission_required('discounts.aprobar_descuento', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def get(self, request, *args, **kwargs):
        super(AprobarDescuentoView, self).get(request, *args, **kwargs)
        id_colegio = get_current_colegio()
        descuentos = self.model.objects.filter(matricula__colegio__id_colegio=id_colegio).filter(estado=1).order_by(
            "id_descuento")
        contexto = {}
        contexto['object_list'] = descuentos
        return render(request, self.template_name, contexto)  # return context

    @method_decorator(
        permission_required('discounts.aprobar_descuento', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def post(self, request, *args, **kwargs):
        logger.info("Estoy en el POST")
        logger.info("Los datos de llegada son {0}".format(request.POST))
        data_post = request.POST

        id_colegio = get_current_colegio()
        descuentos = self.model.objects.filter(matricula__colegio__id_colegio=id_colegio).filter(estado=1).order_by("id_descuento")
        n = 0
        for descuento in descuentos:
            n = n + 1
            try:
                logger.info("Iniciando el Try por {0} vez".format(n))

                descuento_id = "gender{0}".format(descuento.id_descuento)
                logger.info("El dato de llegada para {0} es {1}".format(descuento_id, data_post[descuento_id]))

                if data_post[descuento_id] == "aprobar":
                    # Guardar el estado de descuento como "Aprobado"
                    descuento.estado = 2
                    descuento.comentario = "Aprobado"
                    descuento.fecha_aprobacion = date.today()
                    descuento.save()

                    # Generando los descuentos en las cuentas por cobrar
                    matricula_id = descuento.matricula.id_matricula
                    logger.debug("La matrícula asociada al descuento es {0}".format(matricula_id))
                    porcentaje_descuento = float(descuento.tipo_descuento.porcentaje)
                    logger.debug("El porcentaje de descuento es {0}".format(porcentaje_descuento))
                    servicio_id = descuento.tipo_descuento.servicio.id_servicio
                    logger.debug("El servicio asociado al descuento tiene id = {0}".format(servicio_id))
                    cuenta_descuento1 = Cuentascobrar.objects.filter(matricula__id_matricula=matricula_id)
                    cuenta_descuento2 = cuenta_descuento1.filter(servicio__id_servicio=servicio_id)
                    cuenta_descuento = cuenta_descuento2.filter(fecha_ven__year=date.today().year) #Se realizan descuentos para el presente año

                    for cuenta in cuenta_descuento:
                        if cuenta.estado == True:
                            cuenta.descuento = cuenta.precio*porcentaje_descuento
                            if cuenta.deuda - cuenta.descuento > 0:
                                cuenta.deuda = cuenta.deuda - cuenta.descuento
                            else:
                                cuenta.deuda = 0
                            cuenta.save()

                else:
                    descuento.estado = 3
                    descuento.comentario = "No aprobado"
                    descuento.save()
            except:
                logger.info("No se realizan cambios")

        contexto = {}
        contexto['object_list'] = descuentos
        contexto['id_colegio'] = id_colegio
        return render(request, template_name=self.template_name, context=contexto)


class DetalleDescuentoView(FormView):

    model = Descuento
    template_name = "detalle_descuento.html"
    form_class = DetalleDescuentosForm

    def cargarformPromotordescuentos(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos los años
            anio = datetime.today().year
            anios = []
            for i in range(0, 3):
                anios.append(anio - i)

            # Cargamos los estados
            estados = ["Todos", "Pagado", "No pagado"]

            return {'anios': anios, 'estados': estados}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context

    @method_decorator(
        permission_required('discounts.detalle_descuento', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def get(self, request, *args, **kwargs):
        super(DetalleDescuentoView, self).get(request, *args, **kwargs)

        contexto = self.cargarformPromotordescuentos(request)

        return render(request, self.template_name, contexto)  # return context

    @method_decorator(
        permission_required('discounts.detalle_descuento', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def get_queryset(self):
        return []

    @method_decorator(
        permission_required('discounts.detalle_descuento', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def post(self, request, *args, **kwargs):

        alumno = request.POST["alumno"]
        anio = request.POST["anio"]
        numero_expediente = request.POST["numero_expediente"]
        estado = request.POST["estado"]

        logger.info("Los datos de llegada son {0}".format(request.POST))

        id_colegio = get_current_colegio()

        # Proceso de filtrado según el colegio
        descuentos_0 = self.model.objects.filter(matricula__colegio__id_colegio=id_colegio)

        # Proceso de filtrado según el alumno
        if alumno == "":
            descuentos_1 = descuentos_0
        else:
            descuentos_1 = descuentos_0.filter(Q(matricula__alumno__nombre=alumno) | Q(matricula__alumno__apellido_pa=alumno) | Q(matricula__alumno__apellido_ma=alumno))

        # Proceso de filtrado según el año
        descuentos_2 = descuentos_1.filter(fecha_modificacion__year=anio)

        # Proceso de filtrado según el número de expediente
        if numero_expediente == "":
            descuentos_3 = descuentos_2
        else:
            descuentos_3 = descuentos_2.filter(numero_expediente=int(numero_expediente))

        # Proceso de filtrado según el estado o tipo
        if estado == "Todos":
            descuentos = descuentos_3
        elif estado == "Pendiente":
            descuentos = descuentos_3.filter(estado=1)
        elif estado == "Aprobado":
            descuentos = descuentos_3.filter(estado=2)
        else:
            descuentos = descuentos_3.filter(estado=3)

        contexto = self.cargarformPromotordescuentos(request)

        if len(descuentos) != 0:
            contexto['object_list']=descuentos
            return render(request, template_name=self.template_name, context=contexto)
        else:
            contexto['object_list'] = []
            return render(request, template_name=self.template_name, context=contexto)
