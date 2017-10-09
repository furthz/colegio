from django.db import models

from register.models import Colegio, Alumno, Apoderado, Personal
from utils.models import CreacionModificacionUserMixin
from utils.models import CreacionModificacionFechaMixin
"""

class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio") # MEJOR QUE ESTE LIGADO A UN SERVICIO NO?
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False


class Horario(models.Model):
    id_horario = models.AutoField(primary_key=True)
    grupo = models.ForeignKey(Grupo, models.DO_NOTHING, db_column="id_grupo")
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    fecha_inicio_vigencia = models.DateField()
    fecha_fin_vigencia = models.DateField()

    class Meta:
        managed = False


class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")
    horario = models.ForeignKey(Horario, models.DO_NOTHING, db_column="id_horario")
    grupo = models.ForeignKey(Grupo, models.DO_NOTHING, db_column="id_grupo")
    encargado = models.ForeignKey(Personal, models.DO_NOTHING, db_column="id_personal")
    #tipo_evento = models.
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    fecha_evento = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        managed = False


class EventoUsuario(models.Model):
    apoderado = models.ForeignKey(Apoderado, models.DO_NOTHING, db_column="id_apoderado")
    evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column="id_evento")

    class Meta:
        managed = False


class AsistenciaCursos(models.Model):
    id_asistencia_curso = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")
    horario = models.ForeignKey(Horario, models.DO_NOTHING, db_column="id_horario")
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')
    docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column='id_docente')
    #tipo_asistencia = models
    fecha_asistencia = models.DateField()
    estado_asistencia = models.BooleanField()

    class Meta:
        managed = False


class AsistenciaDia(models.Model):
    id_asistencia_dia = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')
    fecha = models.DateField()
    estado_asistencia = models.BooleanField()
    descripcion = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False


class Notas(models.Model):
    id_nota = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column="id_curso")
    periodo_academico = models.ForeignKey(PeriodoAcademico, models.DO_NOTHING, db_column="id_periodo_academico")
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')
    nota = models.IntegerField()

    class Meta:
        managed = False
"""