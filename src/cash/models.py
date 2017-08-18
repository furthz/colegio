from django.db import models
from django.utils import timezone
from register.models import Colegio, PersonalColegio


class Caja(models.Model):
    """
    Clase para la Caja
    """
    id_caja = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    fecha_modificacion = models.DateField(blank=True, null=True)
    usuario_creacion = models.CharField(max_length=10, blank=True, null=True)
    usuario_modificacion = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        """
        Devuelve el Número de la Caja más la descripción de esta. Ejemplo :
        :return 1 - Caja 001
        """

        return "{0} {1} {2}".format(self.numero, ' - ', self.descripcion)

    class Meta:
        managed = False
        db_table = 'caja'


class CajaCajero(models.Model):
    """
    Clase para CajaCajero
    """
    id_movimiento = models.AutoField(primary_key=True)
    personal_colegio = models.ForeignKey(PersonalColegio, models.DO_NOTHING, db_column="id_personal_colegio")
    caja = models.ForeignKey(Caja, models.DO_NOTHING, db_column='id_caja')
    saldo = models.FloatField()
    monto_apertura = models.FloatField()
    monto_cierre = models.FloatField()
    estado = models.IntegerField()
    fecha_creacion = models.DateField(blank=True, null=True)
    fecha_modificacion = models.DateField(blank=True, null=True)
    usuario_creacion = models.CharField(max_length=10, blank=True, null=True)
    usuario_modificacion = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        """
        Devuelve la Caja(Número de caja + Descripción) + Cajero asignado(Nombre+Correo)
        :return: 1 - Caja 001 - Raquel <raquel.montalvo@mundopixel.pe>
        """

        return "{0} {1} {2}".format(self.caja, ' - ', self.personal_colegio)

    class Meta:
        managed = False
        db_table = 'caja_cajero'


class Remesa(models.Model):
    """
    Clase para la Remesa
    """
    id_remesa = models.AutoField(primary_key=True)
    personal_colegio = models.ForeignKey(PersonalColegio, models.DO_NOTHING, db_column="id_personal_colegio")
    movimiento = models.ForeignKey(CajaCajero, models.DO_NOTHING, db_column='id_movimiento')
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
