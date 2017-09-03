from datetime import date
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from utils.views import MyLoginRequiredMixin
from discounts.models import Descuento

import logging

# Create your views here.

logger = logging.getLogger("project")

# logger.info(dato) para mostrar los reportes de eventos
# logger.debug("usuario logueado: " + str(request.user.is_authenticated()))
# logger.debug("colegio: " + str(request.session.get('colegio')))
#################################################
#       Solicitar Descuentos
#################################################







#################################################
#       Aprobar Descuentos
#################################################

class AprobarDescuentoView(ListView):

    model = Descuento
    template_name = "aprobar_descuento.html"



    """
    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):

        anio = request.POST["anio"]
        logger.debug("El año ingresado es {0}".format(anio))
        tipo_pago = request.POST["tipo_pago"]
        logger.debug("El tipo o estado ingresado es {0}".format(tipo_pago))
        mes = request.POST["mes"]
        logger.debug("El mes ingresado es {0}".format(mes))

        pagos_colegio = calculo_pagos_total(anio, tipo_pago, mes)

        anio = int(anio)
        if anio == date.today().year:
            rango_mes = date.today().month
        else:
            rango_mes = 12
        logger.debug("El rango de meses es {0}".format(rango_mes))

        # CALCULO DE MONTO TOTAL DE PAGOS POR MES SEGÚN AÑO ESCOGIDO
        monto_mes_total = []  # Lista de Montos totales por mes
        for mes in range (0, rango_mes):
            pagos_mes = pagos_colegio.filter(fecha__month=mes + 1)
            monto_mes_total.append(0)  # Declara las Montos totales iniciales de un mes como '0'
            for pagos in pagos_mes:
                monto_mes_total[mes] = monto_mes_total[mes] + pagos.monto  # Cálculo de los montos totales del mes
        logger.debug("El monto del año por mes es {0}".format(monto_mes_total))

        paginator = Paginator(pagos_colegio, 3)  # Show 25 contacts per page

        if pagos_colegio != []:
            page = request.GET.get('page')
            try:
                pagos = paginator.page(page)
            except PageNotAnInteger:
                pagos = paginator.page(1)
            except EmptyPage:
                pagos = paginator.page(paginator.num_pages)

        if len(pagos_colegio) != 0:
            return render(request, template_name=self.template_name, context={
                'pagos_colegio': pagos,
                'monto_mes_total': monto_mes_total,
                'form': ControlPagosPromotorForm,
            })
        else:
            return render(request, template_name=self.template_name, context={
                'pagos_colegio': [],
                'monto_mes_total': [],
                'form': ControlPagosPromotorForm,
            })
            """
