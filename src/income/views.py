from datetime import date, datetime

from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.decorators import method_decorator
from django.conf import settings

from income.forms import CuentasCobrarPromotorForm, CuentasCobrarPadresForm, CuentasCobrarPromotorDetalleForm
from django.db.models import Q
from income.models import calculo_ingresos_promotor, obtener_mes, calculo_ingresos_alumno, calculo_por_nivel_promotor
from django.views.generic import FormView, TemplateView
from django.shortcuts import render
from register.models import Cajero
from enrollment.models import Cuentascobrar, Matricula
from register.models import Sucursal, Alumno, Apoderado, Promotor, PersonalSucursal, Personal
from profiles.models import Profile
from income.models import Cobranza, DetalleCobranza
from cash.models import CajaCajero
from utils.middleware import get_current_colegio, get_current_user, validar_roles

from utils.views import MyLoginRequiredMixin
from django.http import HttpResponseRedirect
from django.conf import settings

import logging
logger = logging.getLogger("project")

class FiltrarCuentas(MyLoginRequiredMixin, TemplateView):
    """

    """
    template_name = "filtrar_cuentas.html"
    cuentas = []

    #@method_decorator(permission_required('income.Registrar_Pago_List', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['cajero']

        if validar_roles(roles=roles):
            logger.info("Se tienen los permisos de cajero")
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        try:
            usuario = get_current_user()
            mov = CajaCajero.objects.get(estado=True, usuario_modificacion= str(usuario.id))
            alerta = False
        except:
            alerta = True
        dato = 1
        logger.info("Estoy en income pagos")
        try:
            dato = request.GET['dato']
            logger.info("Ver si existe un GET")
            print(request.GET['filter'])
            if request.GET['filter'] == 'DNI':
                print("filtro DNI")
                alumnos = Alumno.objects.filter(numero_documento=request.GET['dato'])
            else:
                alumnos = Alumno.objects.filter(apellido_pa__icontains = request.GET['dato'].upper())
        except:

            self.cuentas = []
            alumnos = []

        alumnos1 = []
        for alumno in alumnos:
            try:
                matricula = Matricula.objects.get(colegio=get_current_colegio(), activo=True, alumno= alumno)
                alumnos1.append(alumno)
            except:
                logger.info("no pertenece al colegio")

        return render(request, template_name=self.template_name, context={
            'alerta':alerta,
            'dato':dato,
            'alumnos': alumnos1,
        })



class RegistrarPagoListView(MyLoginRequiredMixin, TemplateView):
    """

    """
    template_name = "registrarpago_form.html"
    cuentas = []

    #@method_decorator(permission_required('income.Registrar_Pago_List', login_url=settings.REDIRECT_PERMISOS,
    #                                      raise_exception=False))
    def get(self, request, *args, **kwargs):
        """tiposervicio = self.model.objects.get(pk = int(request.GET['tiposervicio']))
        for servicio in tiposervicio.getServiciosAsociados():
            servicio.activo = False
            servicio.save()
        tiposervicio.activo = False
        tiposervicio.save()
        """
        #cuentas = Cuentascobrar.objects.all()
        roles = ['cajero']

        if validar_roles(roles=roles):
            logger.info("Se tienen los permisos de cajero")
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        try:
            usuario = get_current_user()
            mov = CajaCajero.objects.get(estado=True, usuario_modificacion= str(usuario.id))
            alerta = False
        except:
            alerta = True
        dato = 1
        logger.info("Estoy en income pagos")
        cuentas_totales = Cuentascobrar.objects.filter(
            matricula__colegio__id_colegio=self.request.session.get('colegio'), estado=True, activo=True)
        try:
            dato = request.GET['dato']
            logger.info("Ver si existe un GET")
            print(request.GET['filter'])
            if request.GET['filter'] == 'DNI':
                print("filtro DNI")
                self.cuentas = cuentas_totales.filter(matricula__alumno__numero_documento=request.GET['dato'].upper(),activo=True, estado=True).order_by("fecha_ven")
                alumno = Alumno.objects.get(numero_documento=request.GET['dato'])
            else:
                self.cuentas = cuentas_totales.filter(matricula__alumno__apellido_pa__icontains=  request.GET['dato'].upper(),activo=True, estado=True).order_by("fecha_ven")
                alumno = Alumno.objects.get(apellido_pa__icontains = request.GET['dato'].upper())
        except:

            self.cuentas = []
        logger.info(self.cuentas)

        try:
            pknum = alumno.id_alumno
        except:
            pknum = None
        return render(request, template_name=self.template_name, context={
            'alerta':alerta,
            'dato':dato,
            'cuentascobrar': self.cuentas,
            'pknum': pknum,
        })
        #return HttpResponseRedirect(reverse('enrollments:tiposervicio_list'))

    def post(self, request, *args, **kwargs):

        logger.info("Estoy en el POST")
        logger.info(request.POST)
        data_post = request.POST
        self.cuentas = Cuentascobrar.objects.filter(matricula__alumno__id_alumno=request.POST['persona'], activo=True, estado=True).order_by("fecha_ven")
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
                    lista_montos.append(cuenta.deuda)
                    logger.info('Monto {0}'.format(cuenta.deuda))
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
        datos_contexto['colegio'] = Sucursal.objects.get(pk = self.request.session.get('colegio'))
        colegio = Sucursal.objects.get(pk = self.request.session.get('colegio'))
        #colegio.numero_recibo = colegio.numero_recibo + 1
        colegio.save()
        datos_contexto['alumno'] = lista_cuentas[0].matricula.alumno
        datos_contexto['tiposervicio'] = lista_cuentas[0].matricula.tipo_servicio
        datos_contexto['fecha'] = datetime.today()
        datos_contexto['cajero'] = Profile.objects.get(user=self.request.user)
        datos_contexto['servicios'] = DetalleCobranza.objects.filter(cobranza=cobranza_actual)
        datos_contexto['cobranza'] = cobranza_actual.id_cobranza
        datos_contexto['subtotal'] = total
        datos_contexto['descuento'] = 0
        datos_contexto['total'] = total
        return datos_contexto


    def CrearDetallesCobranza(self,lista_cuentas,lista_montos,total):
        logger.info("Estoy en crear detalles")
        #logger.info(CajaCajero.objects.get(estado=True,personal_colegio__personal__user=self.request.user))
        usuario = get_current_user()
        cobranza_actual = Cobranza(
            movimiento= CajaCajero.objects.get(estado=True,usuario_creacion=str(usuario.id)),
            fecha_pago = date.today(),
            monto = total,
            medio_pago = 1,
            num_operacion = "1234"
        )

        cobranza_actual.save()
        movi= CajaCajero.objects.get(estado=True,usuario_creacion=str(usuario.id))
        movi.ventas = movi.ventas + total
        movi.save()
        for k in range(len(lista_cuentas)):
            cuenta = lista_cuentas[k]
            print(k)
            monto = lista_montos[k]
            detalle_actual = DetalleCobranza(
                cuentascobrar=cuenta,
                cobranza=cobranza_actual,
                monto=monto
            )
            detalle_actual.save()
            if monto is cuenta.deuda:
                cuenta.deuda = 0
                cuenta.estado = False
            else:
                cuenta.deuda = cuenta.deuda - monto
            cuenta.save()

        return cobranza_actual




"""
PADRES: PAGOS REALIZADOS POR HIJO, AÑO, MES Y ESTADO
"""

class ControlIngresosPadresView(FormView):

    model = Cuentascobrar
    template_name = "control_ingresos_padres.html"
    form_class = CuentasCobrarPadresForm

    def cargarformPadres(self, request):

        # Obtiene el colegio en cuestión
        id_colegio = get_current_colegio()
        colegio = Sucursal.objects.get(pk=id_colegio)
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
            # 1. Verificamos que el usuario sea un apoderado
            apoderado = Apoderado.objects.get(persona=profile)
            logger.debug("apoderado: " + str(apoderado.id_apoderado))

            # 2. Verificamos los alumnos que tienen el apoderado y el colegio de la sesión
            matriculas = Matricula.objects.filter(colegio=colegio, alumno__apoderados=apoderado)

            if matriculas.count() == 0:
                sw_error = True
                mensaje_error = "No es un apoderado de un alumno asociado al colegio"
            else:
                sw_error = False

        except Apoderado.DoesNotExist:
            sw_error = True
            mensaje_error = "No es un apoderado"

        if sw_error != True:

            # Cargamos los alumnos
            alumnos = []
            for apo_alu in matriculas:
                alumnos.append(apo_alu.alumno)

            # Cargamos los años
            anio = datetime.today().year
            anios = []
            for i in range(0, 3):
                anios.append(anio - i)

            # Cargamos los meses
            meses_todos = ["Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                           "Setiembre", "Octubre", "Noviembre", "Diciembre"]
            num_mes = datetime.today().month
            meses = []
            for i in range(0, num_mes + 1):
                meses.append(meses_todos[i])

            # Cargamos los estados
            estados = ["Todos", "Pagado", "No pagado"]

            return {'alumnos': alumnos, 'anios': anios, 'meses': meses_todos, 'estados': estados}

        else:
            return {'mensaje_error': mensaje_error}  # return context

    @method_decorator(permission_required('enrollment.control_ingresos_padres', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        super(ControlIngresosPadresView, self).get(request, *args, **kwargs)

        contexto = self.cargarformPadres(request)

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context

    @method_decorator(permission_required('enrollment.control_ingresos_padres', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get_queryset(self):
        return []

    @method_decorator(permission_required('enrollment.control_ingresos_padres', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
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

        id_colegio = get_current_colegio()
        cuenta_padres = calculo_ingresos_alumno(id_colegio, alumno, anio, mes, estado)

        contexto = self.cargarformPadres(request)

        if len(cuenta_padres) != 0:
            contexto['object_list'] = cuenta_padres

            return render(request, template_name=self.template_name, context=contexto)
        else:
            contexto['object_list'] = []
            return render(request, template_name=self.template_name,context=contexto)


"""
PROMOTOR: DEUDAS Y COBROS POR AÑO, MES Y NIVEL
"""

class ControlIngresosPromotorView(FormView):

    model = Cuentascobrar
    template_name = "control_ingresos_director.html"
    form_class = CuentasCobrarPromotorForm

    def cargarformPromotor(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos los años
            anio = datetime.today().year
            anios = []
            anios.append(anio + 1)
            for i in range(0, 3):
                anios.append(anio - i)

            # Cargamos los meses
            meses_todos = ["Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                           "Setiembre", "Octubre", "Noviembre", "Diciembre"]
            num_mes = datetime.today().month
            meses = []
            for i in range(0, num_mes + 1):
                meses.append(meses_todos[i])

            return {'anios': anios, 'meses': meses_todos}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context


    @method_decorator(
        permission_required('enrollment.control_ingresos_promotor', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def get(self, request, *args, **kwargs):
        super(ControlIngresosPromotorView, self).get(request, *args, **kwargs)

        contexto = self.cargarformPromotor(request)

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context

    @method_decorator(
        permission_required('enrollment.control_ingresos_promotor', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def get_queryset(self):
        return []

    @method_decorator(
        permission_required('enrollment.control_ingresos_promotor', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def post(self, request, *args, **kwargs):

        id_colegio = get_current_colegio()
        anio = request.POST["anio"]
        mes = request.POST["mes"]

        logger.info(anio)
        logger.info(mes)

        if anio == str(date.today().year):
            num_mes = date.today().month
        else:
            num_mes = 12

        anio = int(anio)

        por_cobrar_total, cobro_total, deuda_total = calculo_ingresos_promotor(id_colegio, anio, mes)
        por_cobrar_grado, cobro_total_grado, deuda_total_grado = calculo_por_nivel_promotor(id_colegio, anio, mes)

        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre",
                 "Noviembre", "Diciembre"]

        mes_labels = []
        for i in range(0, num_mes):
            mes_labels.append(meses[i])
        logger.info(mes_labels)

        contexto = self.cargarformPromotor(request)
        contexto['por_cobrar_grado'] = por_cobrar_grado
        contexto['cobro_total_grado'] = cobro_total_grado
        contexto['deuda_total_grado'] = deuda_total_grado
        contexto['por_cobrar_total'] = por_cobrar_total
        contexto['cobro_total'] = cobro_total
        contexto['deuda_total'] = deuda_total
        contexto['mes_labels'] = mes_labels
        contexto['mes_llega'] = mes
        contexto['anio_llega'] = anio

        return render(request, template_name=self.template_name, context = contexto)


"""
PROMOTOR: DETALLE DE PAGOS REALIZADOS POR HIJO, AÑO, MES Y ESTADO
"""

class ControlIngresosPromotorDetallesView(FormView):

    model = Cuentascobrar
    template_name = "control_ingresos_promotor_detalle.html"
    form_class = CuentasCobrarPromotorDetalleForm

    def cargarformPromotordetalle(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos los años
            anio = datetime.today().year
            anios = []
            anios.append(anio + 1)
            for i in range(0, 3):
                anios.append(anio - i)

            # Cargamos los meses
            meses_todos = ["Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                           "Setiembre", "Octubre", "Noviembre", "Diciembre"]
            num_mes = datetime.today().month
            meses = []
            for i in range(0, num_mes + 1):
                meses.append(meses_todos[i])

            # Cargamos los estados
            estados = ["Todos", "Pagado", "No pagado"]

            return {'anios': anios, 'meses': meses_todos, 'estados': estados}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context

    @method_decorator(
        permission_required('enrollment.control_ingresos_promotor_detalle', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def get(self, request, *args, **kwargs):
        super(ControlIngresosPromotorDetallesView, self).get(request, *args, **kwargs)

        contexto = self.cargarformPromotordetalle(request)

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context

    @method_decorator(
        permission_required('enrollment.control_ingresos_promotor_detalle', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def get_queryset(self):
        return []

    @method_decorator(
        permission_required('enrollment.control_ingresos_promotor_detalle', login_url=settings.REDIRECT_PERMISOS,
                            raise_exception=False))
    def post(self, request, *args, **kwargs):

        alumno = request.POST["alumno"]
        anio = request.POST["anio"]
        mes = request.POST["mes"]
        estado = request.POST["estado"]

        logger.info(alumno)
        colegio = get_current_colegio()

        # Proceso de filtrado según el colegio
        cuentas_cobrar_colegio = self.model.objetos.filter(matricula__colegio__id_colegio=colegio, activo=True).order_by('fecha_ven')

        # Proceso de filtrado según el alumno
        if alumno == "":
            por_cobrar1 = cuentas_cobrar_colegio
        else:
            por_cobrar1 = cuentas_cobrar_colegio.filter(Q(matricula__alumno__nombre__icontains=alumno.upper()) |
                                                        Q(matricula__alumno__segundo_nombre__icontains=alumno.upper()) |
                                                        Q(matricula__alumno__apellido_pa__icontains=alumno.upper()) |
                                                        Q(matricula__alumno__apellido_ma__icontains=alumno.upper()))

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
        else:
            por_cobrar = por_cobrar3.filter(estado=True)

        contexto = self.cargarformPromotordetalle(request)

        contexto['object_list']=por_cobrar
        contexto['form']=CuentasCobrarPromotorDetalleForm
        return render(request, template_name=self.template_name, context=contexto)




########################################################
#       Generacion de PDF
########################################################


from reportlab.lib.pagesizes import letter, A5, A6
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import date
from register.models import Telefono, Direccion

def recibo_A6(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recibo_A6_{0}.pdf"'.format(datetime.today())
    p = canvas.Canvas(response, pagesize=A6)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 8)

    id_cobranza_actual = request.POST["cobranza"]
    id_alumno = request.POST["alumno"]
    cobranza_actual = Cobranza.objects.get(id_cobranza=id_cobranza_actual)

    colegio = Sucursal.objects.get(pk=get_current_colegio())
    detalle_cobranza = DetalleCobranza.objects.filter(cobranza=cobranza_actual)
    alumno = Alumno.objects.get(id_alumno=id_alumno)
    cajero = Profile.objects.get(user=get_current_user())

    nombre = alumno
    monto = [(str(p.monto)) for p in detalle_cobranza]
    total = sum([(p.monto) for p in detalle_cobranza])
    descripcion = [(str(p.cuentascobrar.servicio.nombre) + " " + str(p.cuentascobrar.servicio.tipo_servicio)) for p in
                   detalle_cobranza]
    fecha = date.today()


    dire = Direccion.objects.get(colegio=colegio)
    dir_colegio = dire.calle

    departamento = dire.get_departamento + " - PERU"

    dire_alumno = Direccion.objects.get(persona=alumno.persona)
    direccion_alumno = dire_alumno.calle



    numero_recibo = colegio.numero_recibo - 1

    p.line(20, 390, 270, 390)
    p.setFont('Helvetica', 8)
    p.drawString(70, 360, '{0}'.format(colegio))
    p.drawString(70, 350, '{0}'.format(dir_colegio))
    try:
        telefono_colegio = Telefono.objects.get(colegio=colegio)
        p.drawString(70, 340, 'Telf.: {0}'.format(telefono_colegio))
        p.drawString(70, 330, '{0}'.format(departamento))
    except:
        p.drawString(70, 340, '{0}'.format(departamento))
    p.drawString(195, 360, 'RECIBO {0}'.format(numero_recibo))
    p.drawString(195, 350, 'FECHA:  {0}'.format(fecha))
    p.setFont('Helvetica', 6)
    p.drawString(20, 310, 'Sr(a):   {0}'.format(nombre))
    p.drawString(20, 300, 'Dirección:  {0}'.format(direccion_alumno))
    p.setFont('Helvetica', 8)
    p.line(20, 265, 270, 265)
    p.line(20, 283, 270, 283)
    p.line(195, 265, 195, 283)
    p.drawString(20, 270, 'Descripción:')
    p.drawString(200, 270, 'Importe S/.')

    p.setFont('Helvetica', 6)
    for k in range(len(descripcion)):
        p.drawString(20, 250 - 15 * k, '{0}'.format(descripcion[k]))
        p.drawString(200, 250 - 15 * k, '{0}'.format(monto[k]))

    p.line(20, 250 - 15 * len(descripcion) - 3, 270, 250 - 15 * len(descripcion) - 3)
    p.line(20, 250 - 15 * len(descripcion) - 18, 270, 250 - 15 * len(descripcion) - 18)
    p.drawString(130, 250 - 15 * len(descripcion) - 15, 'TOTAL S/.:')
    p.drawString(200, 250 - 15 * len(descripcion) - 15, '{0}'.format(total))

    p.showPage()
    p.save()

    return response


def boleta_A6(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="boleta_A6_{0}.pdf"'.format(datetime.today())
    p = canvas.Canvas(response, pagesize=A6)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 8)

    id_cobranza_actual = request.POST["cobranza"]
    id_alumno = request.POST["alumno"]
    cobranza_actual = Cobranza.objects.get(id_cobranza=id_cobranza_actual)

    colegio = Sucursal.objects.get(pk=get_current_colegio())
    detalle_cobranza = DetalleCobranza.objects.filter(cobranza=cobranza_actual)
    alumno = Alumno.objects.get(id_alumno=id_alumno)
    cajero = Profile.objects.get(user=get_current_user())

    nombre = alumno
    monto = [(str(p.monto)) for p in detalle_cobranza]
    total = sum([(p.monto) for p in detalle_cobranza])
    descripcion = [(str(p.cuentascobrar.servicio.nombre) + " " + str(p.cuentascobrar.servicio.tipo_servicio)) for p in
                   detalle_cobranza]
    fecha = date.today()


    dire = Direccion.objects.get(colegio=colegio)
    dir_colegio = dire.calle

    departamento = dire.get_departamento + " - PERU"

    dire_alumno = Direccion.objects.get(persona=alumno.persona)
    direccion_alumno = dire_alumno.calle
    ruc_colegio = colegio.ruc
    numero_recibo = colegio.numero_recibo - 1

    p.line(20, 390, 270, 390)
    p.setFont('Helvetica', 8)
    p.drawString(70, 360, '{0}'.format(colegio))
    p.drawString(70, 350, '{0}'.format(dir_colegio))
    try:
        telefono_colegio = Telefono.objects.get(colegio=colegio)
        p.drawString(70, 340, 'Telf.: {0}'.format(telefono_colegio))
        p.drawString(70, 330, '{0}'.format(departamento))
    except:
        p.drawString(70, 340, '{0}'.format(departamento))
    p.drawString(195, 360, 'RUC: {0}'.format(ruc_colegio))
    p.drawString(195, 350, 'BOLETA DE VENTA')
    p.drawString(195, 340, '001 - N° {0}'.format(numero_recibo))
    p.setFont('Helvetica', 6)
    p.drawString(20, 310, 'Sr(a):   {0}'.format(nombre))
    p.drawString(20, 300, 'Dirección:  {0}'.format(direccion_alumno))
    p.drawString(195, 310, 'Fecha:  {0}'.format(fecha))

    p.setFont('Helvetica', 8)
    p.line(20, 265, 270, 265)
    p.line(20, 283, 270, 283)
    p.line(195, 265, 195, 283)
    p.drawString(20, 270, 'Descripción:')
    p.drawString(200, 270, 'Importe S/.')

    p.setFont('Helvetica', 6)
    for k in range(len(descripcion)):
        p.drawString(20, 250 - 15 * k, '{0}'.format(descripcion[k]))
        p.drawString(200, 250 - 15 * k, '{0}'.format(monto[k]))

    p.line(20, 250 - 15 * len(descripcion) - 3, 270, 250 - 15 * len(descripcion) - 3)
    p.line(20, 250 - 15 * len(descripcion) - 18, 270, 250 - 15 * len(descripcion) - 18)
    p.drawString(130, 250 - 15 * len(descripcion) - 15, 'TOTAL S/.:')
    p.drawString(200, 250 - 15 * len(descripcion) - 15, '{0}'.format(total))

    p.showPage()
    p.save()

    return response

def recibo_A5(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recibo_A5_{0}.pdf"'.format(datetime.today())
    p = canvas.Canvas(response, pagesize=A5)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 8)

    id_cobranza_actual = request.POST["cobranza"]
    id_alumno = request.POST["alumno"]
    cobranza_actual = Cobranza.objects.get(id_cobranza=id_cobranza_actual)

    colegio = Sucursal.objects.get(pk=get_current_colegio())
    detalle_cobranza = DetalleCobranza.objects.filter(cobranza=cobranza_actual)
    alumno = Alumno.objects.get(id_alumno=id_alumno)
    cajero = Profile.objects.get(user=get_current_user())

    nombre = alumno
    monto = [(str(p.monto)) for p in detalle_cobranza]
    total = sum([(p.monto) for p in detalle_cobranza])
    descripcion = [(str(p.cuentascobrar.servicio.nombre) + " " + str(p.cuentascobrar.servicio.tipo_servicio)) for p in
                   detalle_cobranza]
    fecha = date.today()

    dire = Direccion.objects.get(colegio=colegio)
    dir_colegio = dire.calle

    departamento = dire.get_departamento + " - PERU"

    dire_alumno = Direccion.objects.get(persona=alumno.persona)
    direccion_alumno = dire_alumno.calle

    numero_recibo = colegio.numero_recibo - 1


    p.line(40, 510, 370, 510)
    p.setFont('Helvetica', 10)
    p.drawString(90, 490, '{0}'.format(colegio))
    p.drawString(90, 480, '{0}'.format(dir_colegio))
    try:
        telefono_colegio = Telefono.objects.get(colegio=colegio)
        p.drawString(90, 470, 'Telf.: {0}'.format(telefono_colegio))
        p.drawString(90, 460, '{0}'.format(departamento))
    except:
        p.drawString(90, 470, '{0}'.format(departamento))
    p.drawString(270, 490, 'RECIBO {0}'.format(numero_recibo))
    p.drawString(270, 480, 'FECHA:  {0}'.format(fecha))
    p.setFont('Helvetica', 8)
    p.drawString(40, 440, 'Sr(a):   {0}'.format(nombre))
    p.drawString(40, 430, 'Dirección:  {0}'.format(direccion_alumno))
    p.setFont('Helvetica', 10)
    p.line(40, 395, 370, 395)
    p.line(40, 413, 370, 413)
    p.line(295, 395, 295, 413)
    p.drawString(40, 400, 'Descripción:')
    p.drawString(300, 400, 'Importe S/.')

    p.setFont('Helvetica', 8)
    for k in range(len(descripcion)):
        p.drawString(40, 370 - 15 * k, '{0}'.format(descripcion[k]))
        p.drawString(300, 370 - 15 * k, '{0}'.format(monto[k]))

    p.line(40, 370 - 15 * len(descripcion) - 3, 370, 370 - 15 * len(descripcion) - 3)
    p.line(40, 370 - 15 * len(descripcion) - 18, 370, 370 - 15 * len(descripcion) - 18)
    p.drawString(230, 370 - 15 * len(descripcion) - 15, 'TOTAL S/.:')
    p.drawString(300, 370 - 15 * len(descripcion) - 15, '{0}'.format(total))

    p.showPage()
    p.save()

    return response


def boleta_A5(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="boleta_A5_{0}.pdf"'.format(datetime.today())
    p = canvas.Canvas(response, pagesize=A5)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 8)

    id_cobranza_actual = request.POST["cobranza"]
    id_alumno = request.POST["alumno"]
    cobranza_actual = Cobranza.objects.get(id_cobranza=id_cobranza_actual)

    colegio = Sucursal.objects.get(pk=get_current_colegio())
    detalle_cobranza = DetalleCobranza.objects.filter(cobranza=cobranza_actual)
    alumno = Alumno.objects.get(id_alumno=id_alumno)
    cajero = Profile.objects.get(user=get_current_user())

    nombre = alumno
    monto = [(str(p.monto)) for p in detalle_cobranza]
    total = sum([(p.monto) for p in detalle_cobranza])
    descripcion = [(str(p.cuentascobrar.servicio.nombre) + " " + str(p.cuentascobrar.servicio.tipo_servicio)) for p in
                   detalle_cobranza]
    fecha = date.today()


    dire = Direccion.objects.get(colegio=colegio)
    dir_colegio = dire.calle

    departamento = dire.get_departamento + " - PERU"

    dire_alumno = Direccion.objects.get(persona=alumno.persona)
    direccion_alumno = dire_alumno.calle
    ruc_colegio = colegio.ruc
    numero_recibo = colegio.numero_recibo - 1

    p.line(40, 510, 370, 510)
    p.setFont('Helvetica', 10)
    p.drawString(90, 490, '{0}'.format(colegio))
    p.drawString(90, 480, '{0}'.format(dir_colegio))
    try:
        telefono_colegio = Telefono.objects.get(colegio=colegio)
        p.drawString(90, 470, 'Telf.: {0}'.format(telefono_colegio))
        p.drawString(90, 460, '{0}'.format(departamento))
    except:
        p.drawString(90, 470, '{0}'.format(departamento))
    p.drawString(270, 490, 'RUC: {0}'.format(ruc_colegio))
    p.drawString(270, 480, 'BOLETA DE VENTA')
    p.drawString(270, 470, '001 - N° {0}'.format(numero_recibo))
    p.setFont('Helvetica', 8)
    p.drawString(40, 440, 'Sr(a):   {0}'.format(nombre))
    p.drawString(270, 440, 'Fecha:  {0}'.format(fecha))
    p.drawString(40, 430, 'Dirección:  {0}'.format(direccion_alumno))
    p.setFont('Helvetica', 10)
    p.line(40, 395, 370, 395)
    p.line(40, 413, 370, 413)
    p.line(295, 395, 295, 413)
    p.drawString(40, 400, 'Descripción:')
    p.drawString(300, 400, 'Importe S/.')

    p.setFont('Helvetica', 8)
    for k in range(len(descripcion)):
        p.drawString(40, 370 - 15 * k, '{0}'.format(descripcion[k]))
        p.drawString(300, 370 - 15 * k, '{0}'.format(monto[k]))

    p.line(40, 370 - 15 * len(descripcion) - 3, 370, 370 - 15 * len(descripcion) - 3)
    p.line(40, 370 - 15 * len(descripcion) - 18, 370, 370 - 15 * len(descripcion) - 18)
    p.drawString(230, 370 - 15 * len(descripcion) - 15, 'TOTAL S/.:')
    p.drawString(300, 370 - 15 * len(descripcion) - 15, '{0}'.format(total))

    p.showPage()
    p.save()

    return response



"""

XD XD XD XD XD
"""

"""
PROMOTOR: DETALLE DE PAGOS REALIZADOS POR HIJO, AÑO, MES Y ESTADO
"""


class ControlIngresosPromotorDetallesView2(TemplateView):
    model = Cuentascobrar
    template_name = "control_ingresos_promotor_detalle2.html"
    #form_class = CuentasCobrarPromotorDetalleForm

    def cargarformPromotordetalle(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos los años
            anio = datetime.today().year
            anios = []
            for i in range(0, 3):
                anios.append(anio - i)

            # Cargamos los meses
            meses_todos = ["Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                           "Setiembre", "Octubre", "Noviembre", "Diciembre"]
            num_mes = datetime.today().month
            meses = []
            for i in range(0, num_mes + 1):
                meses.append(meses_todos[i])

            # Cargamos los estados
            estados = ["Todos", "Pagado", "No pagado"]

            return {'anios': anios, 'meses': meses_todos, 'estados': estados}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context

    def get(self, request, *args, **kwargs):
        super(ControlIngresosPromotorDetallesView2, self).get(request, *args, **kwargs)

        contexto = self.cargarformPromotordetalle(request)
        contexto['object_list'] = []

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context

    def post(self, request, *args, **kwargs):

        alumno = request.POST["alumno"]
        anio = request.POST["anio"]
        mes = request.POST["mes"]
        estado = request.POST["estado"]

        logger.info(alumno)
        colegio = get_current_colegio()

        # Proceso de filtrado según el colegio
        cuentas_cobrar_colegio = self.model.objetos.filter(matricula__colegio__id_colegio=colegio)

        # Proceso de filtrado según el alumno
        if alumno == "":
            por_cobrar1 = cuentas_cobrar_colegio
        else:
            por_cobrar1 = cuentas_cobrar_colegio.filter(
                Q(matricula__alumno__nombre=alumno) | Q(matricula__alumno__apellido_pa=alumno) | Q(
                    matricula__alumno__apellido_ma=alumno))

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

        contexto = self.cargarformPromotordetalle(request)

        paginator = Paginator(por_cobrar.order_by('fecha_ven'), 4)

        page = request.GET.get('page', 1)

        try:
            buscados = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            buscados = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            buscados = paginator.page(paginator.num_pages)

        contexto['object_list'] = buscados
        #contexto['form'] = CuentasCobrarPromotorDetalleForm

        return render(request, self.template_name, contexto)