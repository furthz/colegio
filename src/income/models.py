from django.db import models

# Create your models here.

from utils.models import CreacionModificacionUserMixin, CreacionModificacionFechaMixin


class Cobranza(CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    id_cobranza = models.AutoField(primary_key=True)
    # id_movimiento = models.ForeignKey(CajaCajero, models.DO_NOTHING, db_column='id_movimiento')
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
    # id_cuentascobrar = models.ForeignKey(Cuentascobrar, models.DO_NOTHING, db_column='id_cuentascobrar')
    monto = models.FloatField()

    class Meta:
        managed = False
        db_table = 'detalle_cobranza'