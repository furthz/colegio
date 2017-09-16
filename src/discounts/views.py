from datetime import date, datetime
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
from django.views import View
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse

from payments.models import TipoPago
from utils.views import MyLoginRequiredMixin
from discounts.models import Descuento
from discounts.models import TipoDescuento
from enrollment.models import Matricula
from enrollment.models import Cuentascobrar
from income.models import obtener_mes
from register.models import Colegio, Personal, Promotor
from register.models import PersonalColegio
from discounts.forms import SolicitarDescuentoForm
from discounts.forms import TipoDescuentForm
from discounts.forms import DetalleDescuentosForm
from utils.middleware import get_current_colegio, get_current_userID, get_current_user
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

class SolicitarDescuentoView(MyLoginRequiredMixin,TemplateView):
    model = Descuento
    template_name = "solicitar_descuento.html"
    form_class = SolicitarDescuentoForm

    def post(self, request, *args, **kwargs):
        form = SolicitarDescuentoForm(initial={'matricula':Matricula.objects.get(pk=request.POST['matricula'])})
        return render(request, template_name=self.template_name, context={
            'form': form,
        })

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
        form = self.form_class(colegio=get_current_colegio())
        return render(request, template_name=self.template_name, context={
            'form': form,
        })

#################################################
#       Aprobar Descuentos
#################################################

class AprobarDescuentoView(ListView):

    model = Descuento
    template_name = "aprobar_descuento.html"

    def cargarformPromotordescuentos(self, request):

        # Obtiene el colegio en cuestión
        id_colegio = get_current_colegio()
        colegio = Colegio.objects.get(pk=id_colegio)
        # logger.debug("Colegio: " + colegio.nombre)

        # Obtiene el usuario que ha iniciado sesión
        user = get_current_user()
        logger.debug("Usuario: " + user.name)

        try:
            profile = Profile.objects.get(user=user)
            logger.debug("profile: " + str(profile.id_persona))
        except Profile.DoesNotExist:
            sw_error = True
            mensaje_error = "No existe la Persona asociada al usuario"

        try:
            # 1. Verificamos que el usuario sea un personal
            personal = Personal.objects.get(persona=profile)
            logger.debug("personal: " + str(personal.id_personal))

            # 2. Verificamos que el usuario sea un personal asociado al colegio
            personal_colegio = PersonalColegio.objects.get(personal=personal, colegio=colegio)

            # 3. Verificamos que sea un promotor
            promotor = Promotor.objects.filter(empleado=personal_colegio.personal)
            #logger.debug()
            if promotor.count() == 0:
                sw_error = True
                mensaje_error = "No es un promotor de un alumno asociado al colegio"
            else:
                sw_error = False

        except Personal.DoesNotExist:
            sw_error = True
            mensaje_error = "No es un personal asociado al colegio"

        if sw_error != True:
            return {}
        else:
            return {'mensaje_error': mensaje_error}  # return context

    def post(self, request, *args, **kwargs):
        logger.info("Estoy en el POST")
        logger.info("Los datos de llegada son {0}".format(request.POST))
        data_post = request.POST

        id_colegio = get_current_colegio()
        self.descuentos = Descuento.objects.filter(matricula__colegio__id_colegio=id_colegio).filter(estado=1).order_by("id_descuento")
        n = 0
        for descuento in self.descuentos:
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
                            cuenta.precio = cuenta.precio - cuenta.descuento
                            cuenta.deuda = cuenta.deuda - cuenta.descuento
                            cuenta.save()

                else:
                    descuento.estado = 3
                    descuento.comentario = "No aprobado"
                    descuento.save()
            except:
                logger.info("No se realizan cambios")

        contexto = self.cargarformPromotordescuentos(request)
        contexto['object_list'] = self.descuentos
        return render(request, template_name=self.template_name, context=contexto)


class DetalleDescuentoView(FormView):

    model = Descuento
    template_name = "detalle_descuento.html"
    form_class = DetalleDescuentosForm

    def cargarformPromotordescuentos(self, request):

        # Obtiene el colegio en cuestión
        id_colegio = get_current_colegio()
        colegio = Colegio.objects.get(pk=id_colegio)
        # logger.debug("Colegio: " + colegio.nombre)

        # Obtiene el usuario que ha iniciado sesión
        user = get_current_user()
        logger.debug("Usuario: " + user.name)

        try:
            profile = Profile.objects.get(user=user)
            logger.debug("profile: " + str(profile.id_persona))
        except Profile.DoesNotExist:
            sw_error = True
            mensaje_error = "No existe la Persona asociada al usuario"

        try:
            # 1. Verificamos que el usuario sea un personal
            personal = Personal.objects.get(persona=profile)
            logger.debug("personal: " + str(personal.id_personal))

            # 2. Verificamos que el usuario sea un personal asociado al colegio
            personal_colegio = PersonalColegio.objects.get(personal=personal, colegio=colegio)

            # 3. Verificamos que sea un promotor
            promotor = Promotor.objects.filter(empleado=personal_colegio.personal)
            #logger.debug()
            if promotor.count() == 0:
                sw_error = True
                mensaje_error = "No es un promotor de un alumno asociado al colegio"
            else:
                sw_error = False

        except Personal.DoesNotExist:
            sw_error = True
            mensaje_error = "No es un personal asociado al colegio"

        if sw_error != True:

            # Cargamos los años
            anio = datetime.today().year
            anios = []
            for i in range(0, 3):
                anios.append(anio - i)

            # Cargamos los estados
            estados = ["Todos", "Pagado", "No pagado"]

            return {'anios': anios, 'estados': estados}

        else:
            return {'mensaje_error': mensaje_error}  # return context

    def get(self, request, *args, **kwargs):
        super(DetalleDescuentoView, self).get(request, *args, **kwargs)

        contexto = self.cargarformPromotordescuentos(request)

        return render(request, self.template_name, contexto)  # return context


    def get_queryset(self):
        return []

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