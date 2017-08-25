from django.db import models
from django.utils import timezone
from register.models import Colegio, PersonalColegio
from utils.models import CreacionModificacionFechaMixin, CreacionModificacionUserMixin
from utils.middleware import get_current_colegio, get_current_userID

class Caja(CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
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
        db_table = 'caja'

class EstadoCambio(models.Model):
    """
    Clase para cambiar de estado automaticamente segun guardado o update
    """
    estado = models.BooleanField()

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.estado = True

        else:  # modificacion
            self.estado = False

        super(EstadoCambio, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True

class CajaCajero(CreacionModificacionFechaMixin, CreacionModificacionUserMixin, EstadoCambio,models.Model):
    """
    Clase para CajaCajero
    """
    id_movimiento = models.AutoField(primary_key=True)
    personal_colegio = models.ForeignKey(PersonalColegio, models.DO_NOTHING,
                                         db_column="id_personal_colegio", default=get_current_userID)  # Persona encargada de la Caja
    caja = models.ForeignKey(Caja, models.DO_NOTHING, db_column='id_caja')  # Caja en la que se apertura la sesión
    saldo = models.FloatField(default=0.0)  # Sobrante o Faltante al Final de la caja
    monto_apertura = models.FloatField(default=0.0)  # Caja Inicial
    monto_cierre = models.FloatField(default=0.0)  # Caja Final
    comentario = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        """
        Devuelve la Caja(Número de caja + Descripción) + Cajero asignado(Nombre+Correo)
        :return: 1 - Caja 001 - Raquel <raquel.montalvo@mundopixel.pe>
        """

        return "{0} {1} {2} {3} {4}".format(self.caja, ' - ', self.personal_colegio, ' - ', self.id_movimiento)

    class Meta:
        managed = False
        db_table = 'caja_cajero'




class Remesa(models.Model):
    """
    Clase para la Remesa
    """
    movimientoid = CajaCajero.objects.latest('id_movimiento')

    id_remesa = models.AutoField(primary_key=True)
    personal_colegio = models.ForeignKey(PersonalColegio, models.DO_NOTHING, db_column="id_personal_colegio")
    movimiento = models.ForeignKey(CajaCajero, models.DO_NOTHING, db_column='id_movimiento', default=movimientoid)
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
