from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView

from payments.models import TipoPago
from payments.models import CajaChica

from register.models import PersonalColegio, Tesorero, Colegio, Personal, Promotor
from payments.forms import TipoPagoForm
from profiles.models import Profile
from payments.forms import PagoForm

from django.utils.timezone import now as timezone_now
from _datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

from payments.forms import ControlPagosPromotorForm
from payments.models import Pago, calculo_pagos_total

from django.views.generic import FormView
import logging
from datetime import date
from django.conf import settings
from utils.middleware import get_current_colegio, get_current_user, validar_roles


logger = logging.getLogger("project")


#################################################
#####          CRUD DE TIPO PAGO            #####
#################################################

class TipoPagoListView(ListView):
    model = TipoPago
    template_name = 'TipoPago/tipopago_list.html'

    @method_decorator(permission_required('payments.Tipo_Pago_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'tesorero', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoPagoListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class TipoPagoDetailView(DetailView):
    template_name = 'TipoPago/tipopago_detail.html'
    model = TipoPago

    @method_decorator(permission_required('payments.Tipo_Pago_Detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'tesorero', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoPagoDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class TipoPagoCreationView(CreateView):
    model = TipoPago
    form_class = TipoPagoForm
    success_url = reverse_lazy('payments:tipopago_list')
    template_name = 'TipoPago/tipopago_form.html'

    @method_decorator(permission_required('payments.Tipo_Pago_Creation', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['tesorero', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoPagoCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class TipoPagoUpdateView(UpdateView):
    model = TipoPago
    form_class = TipoPagoForm
    success_url = reverse_lazy('payments:tipopago_list')
    template_name = 'TipoPago/tipopago_form.html'

    @method_decorator(permission_required('payments.Tipo_Pago_Update', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['tesorero', 'administrativo']

        if validar_roles(roles=roles):
            return super(TipoPagoUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class TipoPagoDeleteView(UpdateView):
    model = TipoPago
    form_class = TipoPagoForm
    success_url = reverse_lazy('payments:tipopago_list')
    template_name = 'TipoPago/tipopago_confirm_delete.html'


@method_decorator(permission_required('payments.Tipo_Pago_Delete', login_url=settings.REDIRECT_PERMISOS,
                                      raise_exception=False))
def get(self, request, *args, **kwargs):
    roles = ['tesorero', 'administrativo']

    if validar_roles(roles=roles):
        return super(TipoPagoDeleteView, self).get(request, *args, **kwargs)
    else:
        return HttpResponseRedirect(settings.REDIRECT_PERMISOS)



#########################################################
#   Registrar Pago
#########################################################

class RegistrarPagoCreateView(CreateView):
    model = Pago
    form_class = PagoForm
    success_url = reverse_lazy('payments:registrarpago_create')
    template_name = 'RegistrarPago/registrarpago_form.html'

    @method_decorator(permission_required('payments.Registrar_Pago_Create', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['tesorero']

        if validar_roles(roles=roles):
            return super(RegistrarPagoCreateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


    def form_valid(self, form):
        form.instance.personal = PersonalColegio.objects.get(pagos__proveedor__user=self.request.user)
        form.instance.caja_chica = CajaChica.objects.get(colegio__id_colegio = self.request.session.get('colegio'))
        form.instance.fecha = datetime.today()
        return super(RegistrarPagoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegistrarPagoCreateView, self).get_context_data(**kwargs)
        cajachica_actual = CajaChica.objects.get(colegio__id_colegio = self.request.session.get('colegio'))
        saldo = cajachica_actual.saldo
        context['saldo'] = saldo
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        logger.info(form)
        if form.is_valid():
            data_form = form.cleaned_data
            logger.info(data_form)
            cajachica_actual = CajaChica.objects.get(colegio__id_colegio=self.request.session.get('colegio'))
            if (cajachica_actual.saldo - data_form['monto']) > 0:

                pago = self.model(proveedor=data_form['proveedor'],
                                  caja_chica=cajachica_actual,
                                  personal=PersonalColegio.objects.get(personal__tesorero__user=self.request.user),
                                  tipo_pago=data_form['tipo_pago'],
                                  descripcion=data_form['descripcion'],
                                  monto=data_form['monto'],
                                  fecha=timezone_now(),
                                  numero_comprobante=data_form['numero_comprobante'])
                pago.save()

                cajachica_actual.saldo = cajachica_actual.saldo - pago.monto
                cajachica_actual.save()
            else:

                return render(request, template_name=self.template_name, context={
                    'form': form,

                    'saldo':CajaChica.objects.get(colegio__id_colegio = self.request.session.get('colegio')).saldo
                })
            return render(request, template_name='RegistrarPago/registrarpago_detail.html', context={
                'pago':pago,
                'fecha':timezone_now(),
            })
        return HttpResponseRedirect(reverse('payments:registrarpago_create'))







"""
PROMOTOR: PAGOS REALIZADOS POR AÑO, MES Y TIPO DE PAGO
"""

class ControlPagosPromotorView(FormView):

    model = Pago
    template_name = "control_pagos_promotor.html"
    form_class = ControlPagosPromotorForm

    def cargarformPromotorpagos(self, request):

        roles = ['promotor', 'director', 'tesorero']

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

            # Cargamos los tipos de pago
            id_colegio = get_current_colegio()
            logger.debug("El id del colegio es {0}".format(id_colegio))
            colegio = Colegio.objects.get(pk=id_colegio)
            tipos = TipoPago.objects.filter(colegio=colegio)
            tipos_pagos = []
            tipos_pagos.append("Todos")
            for tipo in tipos:
                tipos_pagos.append(tipo)

            return {'anios': anios, 'meses': meses_todos, 'tipos_pagos': tipos_pagos}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context

    @method_decorator(permission_required('payments.control_pagos', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        super(ControlPagosPromotorView, self).get(request, *args, **kwargs)

        contexto = self.cargarformPromotorpagos(request)
        logger.debug(contexto.keys())

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context

    @method_decorator(permission_required('payments.control_pagos', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get_queryset(self):
        return []

    @method_decorator(permission_required('payments.control_pagos', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def post(self, request, *args, **kwargs):

        anio = request.POST["anio"]
        logger.debug("El año ingresado es {0}".format(anio))
        tipo_pago = request.POST["tipo_pago"]
        logger.debug("El tipo o estado ingresado es {0}".format(tipo_pago))
        mes = request.POST["mes"]
        logger.debug("El mes ingresado es {0}".format(mes))

        id_colegio = get_current_colegio()
        pagos_colegio = calculo_pagos_total(id_colegio, anio, tipo_pago, mes)

        anio = int(anio)
        if anio == date.today().year:
            rango_mes = date.today().month
        else:
            rango_mes = 12
        logger.debug("El rango de meses es {0}".format(rango_mes))

        # CALCULO DE MONTO TOTAL DE PAGOS POR MES SEGÚN AÑO ESCOGIDO
        monto_mes_total = []  # Lista de Montos totales por mes
        for mes_i in range (0, rango_mes):
            pagos_mes = pagos_colegio.filter(fecha__month=mes_i + 1)
            monto_mes_total.append(0)  # Declara las Montos totales iniciales de un mes como '0'
            for pagos in pagos_mes:
                monto_mes_total[mes_i] = monto_mes_total[mes_i] + pagos.monto  # Cálculo de los montos totales del mes
        logger.debug("El monto del año por mes es {0}".format(monto_mes_total))

        mes_labels = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]

        contexto = self.cargarformPromotorpagos(request)
        contexto['mes_labels'] = mes_labels
        contexto['mes_llega'] = mes
        contexto['anio_llega'] = anio
        contexto['tipo_llega'] = tipo_pago

        if len(pagos_colegio) != 0:
            contexto['pagos_colegio']=pagos_colegio
            contexto['monto_mes_total']=monto_mes_total
            return render(request, template_name=self.template_name, context=contexto)
        else:
            contexto['pagos_colegio'] = []
            contexto['monto_mes_total'] = []
            return render(request, template_name=self.template_name,context=contexto)




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


"""
PROMOTOR: PAGOS REALIZADOS POR AÑO, MES Y TIPO DE PAGO (PAGINACIÓN INCLUÍDA)
"""
class ControlPagosDirectorView(FormView):

    model = Pago
    template_name = "list.html"
    form_class = ControlPagosPromotorForm

    def cargarformPromotorpagos(self, request):

        roles = ['promotor', 'director', 'tesorero']

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

            # Cargamos los tipos de pago
            id_colegio = get_current_colegio()
            logger.debug("El id del colegio es {0}".format(id_colegio))
            colegio = Colegio.objects.get(pk=id_colegio)
            tipos = TipoPago.objects.filter(colegio=colegio)
            tipos_pagos = []
            tipos_pagos.append("Todos")
            for tipo in tipos:
                tipos_pagos.append(tipo)

            return {'anios': anios, 'meses': meses_todos, 'tipos_pagos': tipos_pagos}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context

    def get(self, request, *args, **kwargs):
        super(ControlPagosDirectorView, self).get(request, *args, **kwargs)
        contexto = self.cargarformPromotorpagos(request)

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context

    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):

        #form = ControlPagosPromotorForm(request.POST)
        #form.save()

        anio = request.POST["anio"]
        logger.debug("El año ingresado es {0}".format(anio))
        tipo_pago = request.POST["tipo_pago"]
        logger.debug("El tipo o estado ingresado es {0}".format(tipo_pago))
        mes = request.POST["mes"]
        logger.debug("El mes ingresado es {0}".format(mes))

        id_colegio = get_current_colegio()
        pagos_colegio = calculo_pagos_total(id_colegio, anio, tipo_pago, mes)

        anio = int(anio)
        if anio == date.today().year:
            rango_mes = date.today().month
        else:
            rango_mes = 12
        logger.debug("El rango de meses es {0}".format(rango_mes))

        # CALCULO DE MONTO TOTAL DE PAGOS POR MES SEGÚN AÑO ESCOGIDO
        monto_mes_total = []  # Lista de Montos totales por mes
        for mes_i in range (0, rango_mes):
            pagos_mes = pagos_colegio.filter(fecha__month=mes_i + 1)
            monto_mes_total.append(0)  # Declara las Montos totales iniciales de un mes como '0'
            for pagos in pagos_mes:
                monto_mes_total[mes_i] = monto_mes_total[mes_i] + pagos.monto  # Cálculo de los montos totales del mes
        logger.debug("El monto del año por mes es {0}".format(monto_mes_total))

        contexto = self.cargarformPromotorpagos(request)
        contexto['mes_llega'] = mes
        contexto['anio_llega'] = anio
        contexto['tipo_llega'] = tipo_pago

        page = request.GET.get('page', 1)
        paginator = Paginator(pagos_colegio, 5)  # Número de elementos por tabla

        try:
            pagos_colegio = paginator.page(page)
        except PageNotAnInteger:
            pagos_colegio = paginator.page(1)
        except EmptyPage:
            pagos_colegio = paginator.page(paginator.num_pages)

        if len(pagos_colegio) != 0:
            contexto['pagos_colegio']=pagos_colegio
            contexto['monto_mes_total']=monto_mes_total
            return render(request, template_name=self.template_name, context=contexto)
        else:
            contexto['pagos_colegio'] = []
            contexto['monto_mes_total'] = []
            return render(request, template_name=self.template_name,context=contexto)
