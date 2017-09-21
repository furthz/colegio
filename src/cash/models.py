from django.db import models
from django.utils import timezone
from django.db.models import Sum
from register.models import Colegio, PersonalColegio
from utils.models import CreacionModificacionFechaMixin, CreacionModificacionUserMixin
from utils.middleware import get_current_colegio, get_current_userID
import datetime



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


class Caja(CreacionModificacionFechaMixin, CreacionModificacionUserMixin, Eliminar, models.Model):
    """
    Clase para la Caja
    """
    id_caja = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio', default=get_current_colegio)
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        """
        Devuelve el Número de la Caja más la descripción de esta. Ejemplo :
        :return 1 - Caja 001
        """

        return "{0} {1} {2}".format(self.numero, ' - ', self.descripcion)

    class Meta:
        managed = False
        ordering = ["id_caja"]
        db_table = 'caja'


class EstadoCambio(models.Model):
    """
    Clase para cambiar de estado automaticamente segun guardado o update
    """
    estado = models.BooleanField()

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            #Antes era True
            self.estado = True

        else:  # modificacion
            self.estado = False

        super(EstadoCambio, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


"""
Falta obtener las Cobranzas del día en una función
Cobranza.monto
"""


def getRemesasTotal():
    today = datetime.datetime.today()
    TotalRemesa = Remesa.objects.filter(fechacreacion__year=today.year, fechacreacion__month=today.month, fechacreacion__day=today.day).aggregate(Sum('monto'))['monto__sum']

    return TotalRemesa

#Cajacajero.movimiento


class CajaCajero(CreacionModificacionFechaMixin, CreacionModificacionUserMixin, EstadoCambio, models.Model):
    """
    Clase para CajaCajero
    """
    id_movimiento = models.AutoField(primary_key=True)
    personal_colegio = models.ForeignKey(PersonalColegio, models.DO_NOTHING,
                                         db_column="id_personal_colegio",
                                         default=get_current_userID)  # Persona encargada de la Caja
    caja = models.ForeignKey(Caja, models.DO_NOTHING, db_column='id_caja')  # Caja en la que se apertura la sesión
    saldo = models.FloatField(default=0)  # Sobrante o Faltante al Final de la caja
    monto_apertura = models.FloatField(default=0.0)  # Caja Inicial
    monto_cierre = models.FloatField(default=0.0)  # Caja Final
    comentario_apertura = models.CharField(max_length=500, blank=True, null=True)
    comentario_cierre = models.CharField(max_length=500, blank=True, null=True)
    total_remesa = models.FloatField(default=getRemesasTotal, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            remesa = Remesa.objects.latest('id_remesa')

        except Remesa.DoesNotExist:
            self.saldo = self.monto_apertura - self.monto_cierre
            super().save(*args, **kwargs)

            pass
        except Remesa.MultipleObjectsReturned:
            self.total_remesa = getRemesasTotal()
            self.saldo = ((self.monto_apertura) - getRemesasTotal()) - self.monto_cierre
            super().save(*args, **kwargs)

            pass
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Devuelve la Caja(Número de caja + Descripción) + Cajero asignado(Nombre+Correo)
        :return: 1 - Caja 001 - Raquel <raquel.montalvo@mundopixel.pe>
        """

        return "{0} {1} {2} {3} {4}".format(self.caja, ' - ', self.personal_colegio, ' - ', self.id_movimiento)

    class Meta:
        managed = False
        db_table = 'caja_cajero'


def cajeroExist():
    """
    Verifica la existencia de un registro en CajaCajero
    :return: 
    """
    try:
        movimientoid = CajaCajero.objects.latest('id_movimiento')
    except CajaCajero.DoesNotExist:
        movimientoid = None
        pass
    return movimientoid


class Remesa(models.Model):
    """
    Clase para la Remesa
    """

    id_remesa = models.AutoField(primary_key=True)
    personal_colegio = models.ForeignKey(PersonalColegio, models.DO_NOTHING, db_column="id_personal_colegio")
    movimiento = models.ForeignKey(CajaCajero, models.DO_NOTHING, db_column='id_movimiento', default=cajeroExist)
    fechacreacion = models.DateTimeField(default=timezone.now)
    monto = models.FloatField()
    comentario = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        """
        Devuelve el Nombre de la persona encargada de la Remesa + Fecha Creación
        :return:
        """

        return "{0} {1} {2}".format(self.personal_colegio, ' - ', self.fechacreacion)

    class Meta:
        managed = False
        db_table = 'remesa'
