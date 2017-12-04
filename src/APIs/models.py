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


class Comunicado(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    id_comunicado = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200)
    # colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")
    # tipo = models.IntegerField()

    class Meta:
        managed = False

class Alerta(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    id_alerta = models.AutoField(primary_key=True)
    persona_receptor = models.ForeignKey(Profile, models.DO_NOTHING, db_column="id_persona", null= True, blank= True)
    tipo_alerta = models.ForeignKey(TipoAlerta, models.DO_NOTHING, db_column="id_tipo_alerta")
    comunicado = models.ForeignKey(Comunicado, models.DO_NOTHING, db_column="id_comunicado")
    estado_alerta = models.IntegerField()
    estado_visto = models.BooleanField(default= False)
    fecha_visto = models.DateTimeField(null= True, blank= True)
    fecha_programada = models.DateTimeField(null= True, blank= True)
    fecha_recibido = models.DateTimeField(null= True, blank= True)
    #colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")
    #tipo = models.IntegerField()

    class Meta:
        managed = False

#######################################################################
#           Modelos de clases para los webservices PRUEBA
#######################################################################


class RelacionUsuarioPerfil(models.Model):
    id_persona = models.IntegerField()
    numero_documento = models.IntegerField()
    id_personal = models.IntegerField()
    apellido_pa = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)

    class Meta:
        managed = False

class RelacionPerfilAlumno(models.Model):
    id_colegio = models.IntegerField()
    id_matricula = models.IntegerField()
    id_alumno = models.IntegerField()
    id_persona = models.IntegerField()
    apellido_pa = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)

    class Meta:
        managed = False