from django.db import models

from utils.models import CreacionModificacionUserMixin, ActivoMixin
from utils.models import CreacionModificacionFechaMixin
from profiles.models import Profile


class EstadoAlerta(models.Model):
    id_estado_alerta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False


class TipoAlerta(models.Model):
    id_tipo_alerta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False


class Alerta(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    id_alerta = models.AutoField(primary_key=True)
    persona_receptor = models.ForeignKey(Profile, models.DO_NOTHING, db_column="id_persona", null= True, blank= True)
    tipo_alerta = models.ForeignKey(TipoAlerta, models.DO_NOTHING, db_column="id_tipo_alerta")
    estado_alerta = models.IntegerField()
    estado_visto = models.BooleanField(default= False)
    descripcion = models.CharField(max_length=300)
    fecha_visto = models.DateTimeField(null= True, blank= True)
    fecha_programada = models.DateTimeField(null= True, blank= True)
    fecha_recibido = models.DateTimeField(null= True, blank= True)
    #colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")
    #tipo = models.IntegerField()

    class Meta:
        managed = False
