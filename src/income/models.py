from django.db import models
from enrollment.models import Cuentascobrar
from cash.models import CajaCajero
from utils.models import CreacionModificacionUserMixin
from utils.models import CreacionModificacionFechaMixin
from utils.models import CreacionModificacionUserCajeroMixin
from datetime import datetime, date
from django.db.models import Q


class Cobranza(CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    id_cobranza = models.AutoField(primary_key=True)
    movimiento = models.ForeignKey(CajaCajero, models.DO_NOTHING, db_column='id_movimiento')
    fecha_pago = models.DateField()
    monto = models.FloatField()
    comentario = models.CharField(max_length=500, blank=True, null=True)
    medio_pago = models.IntegerField()
    num_operacion = models.CharField(max_length=10)
    # estado = models.IntegerField()

    @property
    def getMedioPago(self):

        from utils.models import TiposMedioPago

        tipomedio = TiposMedioPago.objects.get(self.medio_pago)

        return tipomedio.descripcion

    class Meta:
        managed = False
        db_table = 'cobranza'


class DetalleCobranza(models.Model):
    id_detalle_cobranza = models.AutoField(primary_key=True)
    cobranza = models.ForeignKey(Cobranza, models.DO_NOTHING, db_column='id_cobranza', related_name='detalles')
    cuentascobrar = models.ForeignKey(Cuentascobrar, models.DO_NOTHING, db_column='id_cuentascobrar')
    monto = models.FloatField()

    class Meta:
        managed = False
        db_table = 'detalle_cobranza'


# FUNCIÓN PARA OBTENER EN MES SEGÚN LO ELEGIDO EN EL FORMULARIO
def obtener_mes(mes):
    if mes == "Enero":
        num_mes = 1
    elif mes == "Febrero":
        num_mes = 2
    elif mes == "Marzo":
        num_mes = 3
    elif mes == "Abril":
        num_mes = 4
    elif mes == "Mayo":
        num_mes = 5
    elif mes == "Junio":
        num_mes = 6
    elif mes == "Julio":
        num_mes = 7
    elif mes == "Agosto":
        num_mes = 8
    elif mes == "Setiembre":
        num_mes = 9
    elif mes == "Octubre":
        num_mes = 10
    elif mes == "Noviembre":
        num_mes = 11
    elif mes == "Diciembre":
        num_mes = 12
    else:
        num_mes = date.today().month
    return num_mes


# FUNCIÓN PARA CÁLCULO DE INGRESOS DE UN AÑO
def calculo_ingresos_promotor(anio):
    if anio == str(date.today().year):
        mes_rango = date.today().month
    else:
        mes_rango = 12
    anio = int(anio)
    porcobrar = Cuentascobrar.objetos.get_queryset().filter(Q(fecha_ven__year=anio))

    deuda_total = []  # Lista de Deudas totales por mes
    cobro_total = []  # Lista de Cobros totales por mes
    por_cobrar_total =[]
    for mes in range(0, mes_rango):
        cuenta_mes = porcobrar.filter(Q(fecha_ven__month=mes + 1))
        deuda_total.append(0)  # Declara las Deudas totales iniciales de un mes como '0'
        cobro_total.append(0)  # Declara los Cobros totales iniciales de un mes como '0'
        por_cobrar_total.append(0)
        for cuenta in cuenta_mes:
            deuda_total[mes] = deuda_total[mes] + cuenta.deuda  # Cálculo de las deudas totales del mes
            cobro_total[mes] = cobro_total[mes] + cuenta.precio - cuenta.deuda  # Cálculo de los cobros totales del mes
            por_cobrar_total[mes] = por_cobrar_total[mes] + cuenta.precio
    return por_cobrar_total, cobro_total, deuda_total


# FUNCIÓN PARA CÁLCULO DE INGRESOS DE CADA NIVEL PARA UN DETERMINADO AÑO Y MES
def calculo_por_nivel_promotor(anio, mes):
    anio2 = int(anio)
    porcobrar_año = Cuentascobrar.objetos.get_queryset().filter(Q(fecha_ven__year=anio2))  # Filtrar por año
    num_mes = obtener_mes(mes)
    porcobrar_mes = porcobrar_año.filter(Q(fecha_ven__month=num_mes))  # Filtrar por mes
    deuda_total_nivel = []
    cobro_total_nivel = []
    por_cobrar_nivel = []
    numero_nivel = 3  # Cambiar por el número de niveles que tiene cada colegio
    for nivel in range(1, numero_nivel + 1):
        porcobrar_nivel = porcobrar_mes.filter(Q(servicio__tipo_servicio__nivel=nivel))
        deuda_total_nivel.append(0)  # Declara las Deudas totales iniciales de un nivel y mes como '0'
        cobro_total_nivel.append(0)  # Declara los Cobros totales iniciales de un nivel y mes como '0'
        por_cobrar_nivel.append(0)
        for cuenta in porcobrar_nivel:
            deuda_total_nivel[nivel - 1] = deuda_total_nivel[nivel - 1] + cuenta.deuda
            cobro_total_nivel[nivel - 1] = cobro_total_nivel[nivel - 1] + cuenta.precio - cuenta.deuda
            por_cobrar_nivel[nivel - 1] = por_cobrar_nivel[nivel - 1] + cuenta.precio
    return por_cobrar_nivel, cobro_total_nivel, deuda_total_nivel


# FUNCIÓN DE CÁLCULO DE INGRESOS FILTRANDO SEGÚN VALORES DE ENTRADA
def calculo_ingresos_alumno(alumno, anio, mes, estado):

    # Proceso de filtrado según el alumno
    por_cobrar1 = Cuentascobrar.objetos.get_queryset().filter(Q(matricula__alumno__id_alumno=alumno))

    # Proceso de filtrado según el año
    if anio == "Todos":
        por_cobrar2 = por_cobrar1
    else:
        anio = int(anio)
        por_cobrar2 = por_cobrar1.filter(fecha_ven__year=anio)

    # Proceso de filtrado según el estado o tipo
    if estado == "Todos":
        por_cobrar = por_cobrar2
    elif estado == "Pagado":
        por_cobrar = por_cobrar2.filter(estado=False)
    elif estado == "No_pagado":
        por_cobrar = por_cobrar2.filter(estado=True)

    # Proceso de filtrado según el mes
    if mes == "Todos":
        cuenta_padres = por_cobrar
    else:
        num_mes = obtener_mes(mes)
        cuenta_padres = por_cobrar.filter(Q(fecha_ven__month=num_mes))
    return cuenta_padres
