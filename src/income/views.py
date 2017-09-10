from datetime import date, datetime

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.conf import settings

from income.forms import CuentasCobrarPromotorForm, CuentasCobrarPadresForm, CuentasCobrarPromotorDetalleForm
from django.db.models import Q
from income.models import calculo_ingresos_promotor, obtener_mes, calculo_ingresos_alumno, calculo_por_nivel_promotor
from django.views.generic import FormView, TemplateView
from django.shortcuts import render
from enrollment.models import Cuentascobrar
from register.models import Colegio, Alumno, Apoderado, ApoderadoAlumno
from profiles.models import Profile
from income.models import Cobranza, DetalleCobranza
from cash.models import CajaCajero
from utils.middleware import get_current_colegio, get_current_user

from utils.views import MyLoginRequiredMixin

import logging
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
        cuentas_totales = Cuentascobrar.objects.filter(
            matricula__colegio__id_colegio=self.request.session.get('colegio'), estado=True)
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




"""
PADRES: PAGOS REALIZADOS POR HIJO, AÑO, MES Y ESTADO
"""
#@method_decorator(permission_required('Cuentascobrar.control_ingresos_padres', login_url=settings.REDIRECT_PERMISOS,
#                                          raise_exception=False))
class ControlIngresosPadresView(FormView):

    model = Cuentascobrar
    template_name = "control_ingresos_padres.html"
    form_class = CuentasCobrarPadresForm

    def get(self, request, *args, **kwargs):
        super(ControlIngresosPadresView, self).get(request, *args, **kwargs)

        id_colegio = get_current_colegio()
        colegio = Colegio.objects.get(pk=id_colegio)

        user = get_current_user()
        logger.debug("Usuario: " + user.name)

        try:
            profile = Profile.objects.get(user=user)
            logger.debug("profile: " + str(profile.id_persona))
        except Profile.DoesNotExist:
            sw_error = True
            mensaje_error = "No existe la Persona asociada al usuario"

        try:
            #1 verificamos que el usuario sea un apoderado
            apoderado = Apoderado.objects.get(persona=profile)
            logger.debug("apoderado: " + str(apoderado.id_apoderado))

            #2 verificamos que el apoderado tenga un alumno registrado en el colegio
            apoderado_alumno = ApoderadoAlumno.objects.filter(al, apoderado=apoderado)

            if apoderado_alumno.count() == 0:
                sw_error = True
                mensaje_error = "No es un apoderado de un alumno asociado al colegio"

        except Apoderado.DoesNotExist:
            sw_error = True
            mensaje_error = "No es un apoderado"


        if sw_error != True:
            #cargamos los alumnos
            alumnos = []
            for apo_alu in apoderado_alumno:
                alumnos.append(apo_alu.alumno)

            return render(request, self.template_name, {'alumnos': alumnos})  # return context
        else:
            return render(request, self.template_name, {'mensaje_error': mensaje_error})  # return context



    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):

        alumno = request.POST["alumno"]
        logger.info("El alumno ingresado es {0}".format(alumno))
        anio = request.POST["anio"]
        logger.debug("El año ingresado es {0}".format(anio))
        mes = request.POST["mes"]
        logger.debug("El mes ingresado es {0}".format(mes))
        estado = request.POST["estado"]
        logger.debug("El tipo o estado ingresado es {0}".format(estado))

        # Validación de hijos asociados a un apoderado
        alumno = int(alumno)

        cuenta_padres = calculo_ingresos_alumno(alumno, anio, mes, estado)

        if len(cuenta_padres) != 0:
            return render(request, template_name=self.template_name, context={
                'object_list': cuenta_padres,
                'form': CuentasCobrarPadresForm,
            })
        else:
            return render(request, template_name=self.template_name,context={
                'object_list': [],
                'form': CuentasCobrarPadresForm,
            })

"""
PROMOTOR: DEUDAS Y COBROS POR AÑO, MES Y NIVEL
"""
class ControlIngresosPromotorView(FormView):

    model = Cuentascobrar
    template_name = "control_ingresos_director.html"
    form_class = CuentasCobrarPromotorForm

    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):

        anio = request.POST["anio"]
        mes = request.POST["mes"]

        logger.info(anio)
        logger.info(mes)

        if anio == str(date.today().year):
            num_mes = date.today().month
        else:
            num_mes = 12

        por_cobrar_total, cobro_total, deuda_total = calculo_ingresos_promotor(int(anio))
        logger.info(por_cobrar_total)
        por_cobrar_nivel, cobro_total_nivel, deuda_total_nivel = calculo_por_nivel_promotor(int(anio), mes)

        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre",
                 "Noviembre", "Diciembre"]

        mes_labels = []
        for i in range(0, num_mes):
            mes_labels.append(meses[i])
        logger.info(mes_labels)

        return render(request, template_name=self.template_name, context = {
            "por_cobrar_nivel": por_cobrar_nivel,
            "cobro_total_nivel": cobro_total_nivel,
            "deuda_total_nivel": deuda_total_nivel,
            "por_cobrar_total": por_cobrar_total,
            "cobro_total": cobro_total,
            "deuda_total": deuda_total,
            "mes_labels": mes_labels,
            'mes': mes,
            'form': CuentasCobrarPromotorForm,
        })


"""
PROMOTOR: DETALLE DE PAGOS REALIZADOS POR HIJO, AÑO, MES Y ESTADO
"""
class ControlIngresosPromotorDetallesView(FormView):

    model = Cuentascobrar
    template_name = "control_ingresos_promotor_detalle.html"
    form_class = CuentasCobrarPromotorDetalleForm

    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):

        alumno = request.POST["alumno"]
        anio = request.POST["anio"]
        mes = request.POST["mes"]
        estado = request.POST["estado"]

        logger.info(alumno)

        # Proceso de filtrado según el alumno
        por_cobrar1 = self.model.objetos.filter(Q(matricula__alumno__nombre=alumno) | Q(matricula__alumno__apellido_pa=alumno) | Q(matricula__alumno__apellido_ma=alumno))


        # Proceso de filtrado según el año
        if anio == "Todos":
            por_cobrar2 = por_cobrar1
        else:
            anio = int(anio)
            por_cobrar2 = por_cobrar1.filter(fecha_ven__year=anio)

        # Proceso de filtrado según el mes
        if mes == "Todos":
            por_cobrar3 = por_cobrar2
        else:
            num_mes = obtener_mes(mes)
            por_cobrar3 = por_cobrar2.filter(fecha_ven__month=num_mes)

        # Proceso de filtrado según el estado o tipo
        if estado == "Todos":
            por_cobrar = por_cobrar3
        elif estado == "Pagado":
            por_cobrar = por_cobrar3.filter(estado=False)
        elif estado == "No_pagado":
            por_cobrar = por_cobrar3.filter(estado=True)


        if len(por_cobrar) != 0:
            return render(request, template_name=self.template_name, context={
                'object_list': por_cobrar,
                'form': CuentasCobrarPromotorDetalleForm,
            })
        else:
            return render(request, template_name=self.template_name, context={
                'object_list': [],
                'form': CuentasCobrarPromotorDetalleForm,
            })
