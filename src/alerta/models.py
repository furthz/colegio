# coding=utf-8
from django.db import models

# Create your models here.

from django.db import models
from utils.models import CreacionModificacionUserMixin, ActivoMixin
from utils.models import CreacionModificacionFechaMixin
from profiles.models import Profile
from enrollment.models import Matricula


class TipoAlerta(CreacionModificacionFechaMixin, models.Model):
    id_tipo_alerta = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.descripcion)

    class Meta:
        managed = False
        ordering = ["id_tipo_alerta"]


class EstadoAlerta(CreacionModificacionFechaMixin, models.Model):
    id_estado_alerta = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.descripcion)

    class Meta:
        managed = False
        ordering = ["id_estado_alerta"]


class ContenidoAlerta(models.Model):
    id_contenido_alerta = models.AutoField(primary_key=True)
    contenido = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.contenido)

    class Meta:
        managed = False
        ordering = ["id_contenido_alerta"]


class PersonaEmisor(models.Model):
    id_persona_emisor = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, models.DO_NOTHING, db_column="id_persona")

    class Meta:
        managed = False
        ordering = ["id_persona_emisor"]


class PersonaReceptor(models.Model):
    id_persona_receptor = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, models.DO_NOTHING, db_column="id_persona")

    class Meta:
        managed = False
        ordering = ["id_persona_receptor"]


class Alerta(CreacionModificacionFechaMixin, models.Model):
    id_alerta = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(Matricula, models.DO_NOTHING, db_column="id_matricula")
    persona_emisor = models.ForeignKey(PersonaEmisor, models.DO_NOTHING, db_column="id_persona_emisor")
    persona_receptor = models.ForeignKey(PersonaReceptor, models.DO_NOTHING, db_column="id_persona_receptor")
    tipo_alerta = models.ForeignKey(TipoAlerta, models.DO_NOTHING, db_column="id_tipo_alerta")
    estado_alerta = models.ForeignKey(EstadoAlerta, models.DO_NOTHING, db_column="id_estado_alerta")
    contenido_alerta = models.ForeignKey(ContenidoAlerta, models.DO_NOTHING, db_column='id_contenido_alerta')
    fecha_visto = models.DateTimeField(blank=True, null=True)
    visto = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ["id_alerta"]