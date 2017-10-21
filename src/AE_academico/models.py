from django.db import models

from enrollment.models import TipoServicio
from register.models import Colegio, Alumno, Apoderado, Personal, Docente
from profiles.models import Profile
from utils.models import CreacionModificacionUserMixin, ActivoMixin
from utils.models import CreacionModificacionFechaMixin


class Aula(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    id_aula = models.AutoField(primary_key=True)
    tipo_servicio = models.ForeignKey(TipoServicio, models.DO_NOTHING, db_column="id_tipo_servicio")
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False

    def __str__(self):
        """
        Solo retorna informacion de la clase como string
        :return: nombre del servicio
        """
        return "{0}".format(self.nombre)


class Curso(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin,models.Model):
    id_curso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")

    class Meta:
        managed = False


class AulaCurso(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin,models.Model):
    id_aula_curso = models.AutoField(primary_key=True)
    aula = models.ForeignKey(Aula, models.DO_NOTHING, db_column="id_aula")
    curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column="id_curso")

    class Meta:
        managed = False


class CursoDocente(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin,models.Model):
    id_curso_docente = models.AutoField(primary_key=True)
    docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column="id_docente")
    curso = models.ForeignKey(AulaCurso, models.DO_NOTHING, db_column="id_aula_curso")

    class Meta:
        managed = False


class HorarioAula(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin,models.Model):
    id_horario_aula = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column="id_curso")
    docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column="id_docente")
    lugar = models.CharField(max_length=50)
    dia = models.CharField(max_length=10)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        managed = False


class Evento(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin,models.Model):
    id_evento = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")
    encargado = models.ForeignKey(Personal, models.DO_NOTHING, db_column="id_personal")
    #tipo_evento = models.
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    fecha_evento = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    # para seleccionar los participantes se hará mediante un filtrado

    class Meta:
        managed = False


class Asistencia(CreacionModificacionFechaMixin, CreacionModificacionUserMixin,models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')
    curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='id_curso')
    fecha = models.DateField()
    estado_asistencia = models.BooleanField()
    comentario = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False


class PeriodoAcademico(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin,models.Model):  # Primer Trimestre, Segundo Bimestre, etc.
    id_periodo_academico = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False

class Notas(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin,models.Model):
    id_nota = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column="id_curso")
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")
    periodo_academico = models.ForeignKey(PeriodoAcademico, models.DO_NOTHING, db_column="id_periodo_academico")
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')
    nota = models.IntegerField()

    class Meta:
        managed = False



