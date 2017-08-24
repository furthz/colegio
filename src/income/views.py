
from django.views.generic import TemplateView

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from enrollment.models import Cuentascobrar
from register.models import Colegio
from register.models import Cajero

from profiles.models import Profile
from register.models import Personal
from register.models import Alumno
from register.models import PersonalColegio
from enrollment.models import Matricula
from enrollment.models import Servicio
from enrollment.models import TipoServicio
from income.models import Cobranza
from income.models import DetalleCobranza

from cash.models import Caja
from cash.models import CajaCajero

from utils.views import MyLoginRequiredMixin
import logging

from datetime import datetime
from datetime import date

logger = logging.getLogger("project")


class RegistrarPagoListView(MyLoginRequiredMixin, TemplateView):
    """

    """
    template_name = "registrarpago_form.html"
    cuentas = []
    def get(self, request, *args, **kwargs):
        """tiposervicio = self.model.objects.get(pk = int(request.GET['tiposervicio']))
        for servicio in tiposervicio.getServiciosAsociados():
            servicio.activo = False
            servicio.save()
        tiposervicio.activo = False
        tiposervicio.save()
        """
        #cuentas = Cuentascobrar.objects.all()
        logger.info("Estoy en income pagos")
        cuentas_totales = Cuentascobrar.objects.filter(matricula__colegio__id_colegio=self.request.session.get('colegio'),estado=True)
        try:
            logger.info("Ver si existe un GET")
            if request.GET['filter'] is 'DNI':
                self.cuentas = cuentas_totales.filter(matricula__alumno__numero_documento=request.GET['dato']).order_by("fecha_ven")
                alumno = Alumno.objects.get(numero_documento=request.GET['dato'])
            else:
                self.cuentas = cuentas_totales.filter(matricula__alumno__apellido_pa = request.GET['dato']).order_by("fecha_ven")
                alumno = Alumno.objects.get(apellido_pa=request.GET['dato'])
        except:
            self.cuentas = []
        logger.info(self.cuentas)

        try:
            pknum = alumno.id_alumno
        except:
            pknum = None
        return render(request, template_name=self.template_name, context={
            'cuentascobrar': self.cuentas,
            'pknum': pknum,
        })
        #return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))

    def post(self, request, *args, **kwargs):
        logger.info("Estoy en el POST")
        logger.info(request.POST)
        data_post = request.POST
        self.cuentas = Cuentascobrar.objects.filter(matricula__alumno__id_alumno=request.POST['persona']).order_by("fecha_ven")
        lista_cuentas = []
        lista_montos = []
        logger.info(self.cuentas)
        for cuenta in self.cuentas:
            try:
                logger.info('Iniciando el Try')
                texto_seleccion = "seleccionado{0}".format(cuenta.id_cuentascobrar)
                logger.info(data_post[texto_seleccion])
                text1 = "optionsRadios{0}".format(cuenta.id_cuentascobrar)
                text2 = "montoparcial{0}".format(cuenta.id_cuentascobrar)
                logger.info('Iniciando el If')
                logger.info(data_post[text1] is "1")
                if data_post[text1] is "1":
                    logger.info('Pago Completo')
                    lista_cuentas.append(cuenta)
                    logger.info(lista_cuentas)
                    lista_montos.append(cuenta.precio)
                    logger.info('Monto {0}'.format(cuenta.precio))
                else:
                    logger.info('Pago Parcial')
                    lista_cuentas.append(cuenta)
                    lista_montos.append(float(data_post[text2]))
                    logger.info('Monto {0}'.format(float(data_post[text2])))
            except:
                logger.info("no pude registrar")
        logger.info(lista_cuentas)
        logger.info(lista_montos)
        datos_contexto = self.detalles(lista_cuentas,lista_montos)

        return render(request, template_name="detalles_pago.html", context=datos_contexto)

    def detalles(self,lista_cuentas,lista_montos):
        total = 0
        for monto in lista_montos:
            total = total + monto

        logger.info("Estoy en Detalles")
        logger.info(self.request.user)
        cobranza_actual =self.CrearDetallesCobranza(lista_cuentas,lista_montos,total)
        datos_contexto = {}
        datos_contexto['colegio'] = Colegio.objects.get(pk = self.request.session.get('colegio'))
        datos_contexto['alumno'] = lista_cuentas[0].matricula.alumno
        datos_contexto['tiposervicio'] = lista_cuentas[0].matricula.tipo_servicio
        datos_contexto['fecha'] = datetime.today()
        datos_contexto['cajero'] = Profile.objects.get(user=self.request.user)
        datos_contexto['servicios'] = DetalleCobranza.objects.filter(cobranza=cobranza_actual)

        datos_contexto['subtotal'] = total
        datos_contexto['descuento'] = 0
        datos_contexto['total'] = total
        return datos_contexto


    def CrearDetallesCobranza(self,lista_cuentas,lista_montos,total):
        logger.info("Estoy en crear detalles")
        logger.info(CajaCajero.objects.get(estado=True))
        cobranza_actual = Cobranza(
            movimiento= CajaCajero.objects.get(estado=True),
            fecha_pago = date.today(),
            monto = total,
            medio_pago = 1,
            num_operacion = "1234"
        )

        cobranza_actual.save()

        for k in range(len(lista_cuentas)):
            cuenta = lista_cuentas[k]
            monto = lista_montos[k]
            detalle_actual = DetalleCobranza(
                cuentascobrar=cuenta,
                cobranza=cobranza_actual,
                monto=monto
            )
            detalle_actual.save()
            if monto is cuenta.deuda:
                cuenta.deuda = 0
            else:
                cuenta.deuda = cuenta.deuda - monto
            cuenta.save()

        return cobranza_actual
