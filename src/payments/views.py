from django.shortcuts import render
from payments.forms import ControlPagosPromotorForm
from payments.models import Pago, calculo_pagos_total
# Create your views here.
from django.views.generic import FormView
import logging
from datetime import date

logger = logging.getLogger("project")

"""
PROMOTOR: PAGOS REALIZADOS POR HIJO, AÑO, MES Y ESTADO
"""
class ControlPagosPromotorView(FormView):

    model = Pago
    template_name = "control_pagos_promotor.html"
    form_class = ControlPagosPromotorForm

    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):

        anio = request.POST["anio"]
        logger.debug("El año ingresado es {0}".format(anio))
        tipo_pago = request.POST["tipo_pago"]
        logger.debug("El tipo o estado ingresado es {0}".format(tipo_pago))
        numero_comprobante = request.POST["numero_comprobante"]
        logger.debug("El tipo o estado ingresado es {0}".format(numero_comprobante))

        fecha_inicio = date.today()
        fecha_final = date.today()

        pagos_colegio = calculo_pagos_total(anio, tipo_pago, numero_comprobante)

        pagos_rango = pagos_colegio.filter(fecha__gte=fecha_inicio).filter(fecha__lte=fecha_final)

        anio = int(anio)
        if anio == date.today().year:
            mes_rango = date.today().month
        else:
            mes_rango = 12
        logger.debug("El rango de meses es {0}".format(mes_rango))

        # CALCULO DE MONTO TOTAL DE PAGOS POR MES SEGÚN AÑO ESCOGIDO
        monto_mes_total = []  # Lista de Montos totales por mes
        for mes in range (0, mes_rango):
            pagos_mes = pagos_colegio.filter(fecha__month=mes + 1)
            monto_mes_total.append(0)  # Declara las Montos totales iniciales de un mes como '0'
            for pagos in pagos_mes:
                monto_mes_total[mes] = monto_mes_total[mes] + pagos.monto  # Cálculo de los montos totales del mes

        # CALCULO DE MONTO TOTAL DE PAGOS POR RANGO
        monto_total_rango = 0  # Lista de Montos totales por mes
        for pagos_1 in pagos_rango:
            monto_total_rango = monto_total_rango + pagos_1.monto  # Cálculo de los montos totales del mes

        # CALCULO DE MONTO POR MES PARA UN RANGO
        mes_inicio = 1
        mes_final = 5
        rango_mes = mes_final - mes_inicio
        monto_rango_mes = []
        for mes in range(0, rango_mes):
            monto_rango_mes.append(0)
            pagos_mes = pagos_colegio.filter(fecha__month=mes + mes_inicio)
            for pagos in pagos_mes:
                monto_rango_mes[mes] = monto_rango_mes[mes] + pagos.monto

        logger.debug("El monto de rango por mes es {0}".format(monto_rango_mes))

        if len(pagos_colegio) != 0:
            return render(request, template_name=self.template_name, context={
                'object_list': pagos_colegio,
                'form': ControlPagosPromotorForm,
            })
        else:
            return render(request, template_name=self.template_name,context={
                'object_list': [],
                'form': ControlPagosPromotorForm,
            })
