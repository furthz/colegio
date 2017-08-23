from datetime import date
from enrollment.models import Cuentascobrar
from income.forms import CuentasCobrarPromotorForm, CuentasCobrarPadresForm, CuentasCobrarPromotorDetalleForm
from django.db.models import Q
import logging
from income.models import calculo_ingresos_promotor, obtener_mes, calculo_ingresos_alumno, calculo_por_nivel_promotor
from django.views.generic import FormView

from django.shortcuts import render

logger = logging.getLogger("project")

"""
PADRES: PAGOS REALIZADOS POR HIJO, AÑO, MES Y ESTADO
"""
class ControlIngresosPadresView(FormView):

    model = Cuentascobrar
    template_name = "control_ingresos_padres.html"
    form_class = CuentasCobrarPadresForm

    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):

        alumno = request.POST["alumno"]
        anio = request.POST["anio"]
        mes = request.POST["mes"]
        estado = request.POST["estado"]

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
        por_cobrar1 = self.model.objetos.filter(Q(matricula__alumno__nombre=alumno) | Q(matricula__alumno__apellido_pa=alumno))

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
            por_cobrar = por_cobrar3.filter(estado=True)
        elif estado == "No_pagado":
            por_cobrar = por_cobrar3.filter(estado=False)


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
