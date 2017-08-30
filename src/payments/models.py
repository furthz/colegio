from django.db import models

# Create your models here.
from register.models import Proveedor, Colegio, PersonalColegio
from utils.models import ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin

class Eliminar(models.Model):
    """
    Clase para cambiar de estado automaticamente segun guardado o update
    """
    eliminado = models.BooleanField()

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.eliminado = False

        else:  # modificacion
            self.eliminado = True

        super(Eliminar, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class TipoPago(ActivoMixin, Eliminar, models.Model):
    """
    Clase para definir y organizar los tipos de pagos que realiza el colegio
    """
    id_tipo_pago = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    padre = models.ForeignKey("self", models.DO_NOTHING, db_column="id_parent")

    def __str__(self):
        """
        Devuelve la descripción del TIPOPAGO. Ejemplo :
        :return Pago de agua
        """

        return "{0}".format(self.descripcion)

    class Meta:
        managed = True
        ordering = ["id_tipo_pago"]
        db_table = 'tipo_pago'


class CajaChica(CreacionModificacionFechaMixin, CreacionModificacionUserMixin):
    """
    Clase para definir el monto que dispondrá un colegio para destinar a los pagos varios
    """
    id_caja_chica = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio", related_name="caja_chica")
    presupuesto = models.DecimalField(decimal_places=10, max_digits=10)
    periodo = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'caja_chica'


class Pago(CreacionModificacionFechaMixin, CreacionModificacionUserMixin):
    """
    Clase para definir los pagos que el colegio realiza por los diferentes conceptos
    """
    id_pago = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column="id_proveedor")
    caja_chica = models.ForeignKey(CajaChica, models.DO_NOTHING, db_column="id_caja_chica", related_name="pagos")
    personal = models.ForeignKey(PersonalColegio, models.DO_NOTHING, db_column="id_personal_colegio", related_name="pagos")
    tipo_pago = models.ForeignKey(TipoPago, models.DO_NOTHING, db_column="id_tipo_pago", related_name="pagos")
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(decimal_places=10, max_digits=10)
    fecha = models.DateTimeField()
    numero_comprobante = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'pago'

