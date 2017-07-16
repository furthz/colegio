# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey('Persona', models.DO_NOTHING, db_column='id_persona')
    codigoint = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alumno'


class Apoderado(models.Model):
    id_apoderado = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey('Persona', models.DO_NOTHING, db_column='id_persona')
    parentesco = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'apoderado'


class ApoderadoAlumno(models.Model):
    id_apoderado = models.ForeignKey(Apoderado, models.DO_NOTHING, db_column='id_apoderado', primary_key=True)
    id_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')

    class Meta:
        managed = False
        db_table = 'apoderado_alumno'
        unique_together = (('id_apoderado', 'id_alumno'),)


class Caja(models.Model):
    id_caja = models.AutoField(primary_key=True)
    id_colegio = models.ForeignKey('Colegio', models.DO_NOTHING, db_column='id_colegio')
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'caja'


class CajaCajero(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    id_colegio = models.IntegerField()
    id_persona = models.IntegerField()
    id_personal = models.ForeignKey('PersonalColegio', models.DO_NOTHING, db_column='id_personal')
    id_caja = models.ForeignKey(Caja, models.DO_NOTHING, db_column='id_caja')
    fecha = models.DateField()
    saldo = models.FloatField()
    monto_apertura = models.FloatField()
    monto_cierre = models.FloatField()
    estado = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'caja_cajero'
        unique_together = (('id_movimiento', 'id_colegio'),)


class Cajero(models.Model):
    id_cajero = models.AutoField(primary_key=True)
    id_personal = models.IntegerField()
    id_persona = models.ForeignKey('Personal', models.DO_NOTHING, db_column='id_persona')

    class Meta:
        managed = False
        db_table = 'cajero'
        unique_together = (('id_cajero', 'id_personal'),)


class Cobranza(models.Model):
    id_cobranza = models.AutoField(primary_key=True)
    id_colegio = models.IntegerField()
    id_movimiento = models.ForeignKey(CajaCajero, models.DO_NOTHING, db_column='id_movimiento')
    fecha_pago = models.DateField()
    fecha_creacion = models.DateField()
    fecha_update = models.DateField()
    monto = models.FloatField()
    comentario = models.CharField(max_length=500, blank=True, null=True)
    medio_pago = models.CharField(max_length=15)
    num_operacion = models.CharField(max_length=10)
    estado = models.IntegerField()
    cod_usuario_creacion = models.CharField(max_length=10)
    cod_usuario_update = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'cobranza'
        unique_together = (('id_cobranza', 'id_colegio'),)


class Colegio(models.Model):
    id_colegio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11)
    ugel = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'colegio'


class Cuentascobrar(models.Model):
    id_cuentascobrar = models.AutoField(primary_key=True)
    id_matricula = models.ForeignKey('Matricula', models.DO_NOTHING, db_column='id_matricula')
    id_alumno = models.IntegerField()
    id_colegio = models.IntegerField()
    id_servicio = models.ForeignKey('Servicio', models.DO_NOTHING, db_column='id_servicio')
    fechaven = models.DateField()
    fechagen = models.DateField()
    comentario = models.CharField(max_length=500, blank=True, null=True)
    estado = models.BooleanField()
    precio = models.FloatField()
    deuda = models.FloatField()
    cod_usuario_creacion = models.CharField(max_length=10)
    cod_usuario_update = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'cuentascobrar'
        unique_together = (('id_cuentascobrar', 'id_matricula', 'id_alumno', 'id_colegio'),)


class DetalleCobranza(models.Model):
    id_cobranza = models.ForeignKey(Cobranza, models.DO_NOTHING, db_column='id_cobranza', primary_key=True)
    id_colegio = models.IntegerField()
    id_cuentascobrar = models.ForeignKey(Cuentascobrar, models.DO_NOTHING, db_column='id_cuentascobrar')
    id_matricula = models.IntegerField()
    id_alumno = models.IntegerField()
    monto = models.FloatField()

    class Meta:
        managed = False
        db_table = 'detalle_cobranza'
        unique_together = (('id_cobranza', 'id_colegio', 'id_cuentascobrar', 'id_matricula', 'id_alumno'),)


class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey('Persona', models.DO_NOTHING, db_column='id_persona')
    id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    calle = models.CharField(max_length=100)
    dpto = models.CharField(max_length=15)
    distrito = models.CharField(max_length=100)
    numero = models.CharField(max_length=6, blank=True, null=True)
    referencia = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direccion'


class Director(models.Model):
    id_director = models.AutoField(primary_key=True)
    id_personal = models.IntegerField()
    id_persona = models.ForeignKey('Personal', models.DO_NOTHING, db_column='id_persona')

    class Meta:
        managed = False
        db_table = 'director'
        unique_together = (('id_director', 'id_personal'),)


class Matricula(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')
    id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    id_tipo_servicio = models.ForeignKey('TipoServicio', models.DO_NOTHING, db_column='id_tipo_servicio')
    fecha = models.DateField()
    estado = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'matricula'
        unique_together = (('id_matricula', 'id_alumno', 'id_colegio'),)


class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=200, blank=True, null=True)
    apellido_pa = models.CharField(max_length=50)
    apellido_ma = models.CharField(max_length=50, blank=True, null=True)
    tipo_documento = models.CharField(max_length=25)
    numerodocumento = models.CharField(max_length=15)
    sexo = models.CharField(max_length=10)
    correo = models.CharField(max_length=100, blank=True, null=True)
    fechanac = models.DateField()

    class Meta:
        managed = False
        db_table = 'persona'


class Personal(models.Model):
    id_personal = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='id_persona')

    class Meta:
        managed = False
        db_table = 'personal'
        unique_together = (('id_personal', 'id_persona'),)


class PersonalColegio(models.Model):
    id_personal = models.IntegerField(primary_key=True)
    id_persona = models.ForeignKey(Personal, models.DO_NOTHING, db_column='id_persona')
    id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'personal_colegio'
        unique_together = (('id_personal', 'id_persona', 'id_colegio'),)


class Promotor(models.Model):
    id_promotor = models.AutoField(primary_key=True)
    id_personal = models.IntegerField()
    id_persona = models.ForeignKey(Personal, models.DO_NOTHING, db_column='id_persona')

    class Meta:
        managed = False
        db_table = 'promotor'
        unique_together = (('id_promotor', 'id_personal'),)


class Remesa(models.Model):
    id_remesa = models.AutoField(primary_key=True)
    id_colegio = models.IntegerField()
    id_persona = models.IntegerField()
    id_personal = models.ForeignKey(PersonalColegio, models.DO_NOTHING, db_column='id_personal')
    id_movimiento = models.ForeignKey(CajaCajero, models.DO_NOTHING, db_column='id_movimiento')
    fecha = models.DateField()
    monto = models.FloatField()
    comentario = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'remesa'
        unique_together = (('id_remesa', 'id_colegio'),)


class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    id_colegio = models.IntegerField()
    id_tipo_servicio = models.ForeignKey('TipoServicio', models.DO_NOTHING, db_column='id_tipo_servicio')
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    isperiodic = models.BooleanField()
    fechafacturar = models.DateField()
    cuotas = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'servicio'


class Telefono(models.Model):
    id_telefono = models.AutoField(primary_key=True)
    id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    id_persona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='id_persona')
    numero = models.IntegerField()
    tipo = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'telefono'


class TipoServicio(models.Model):
    id_tipo_servicio = models.AutoField(primary_key=True)
    id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    isordinario = models.BooleanField()
    nivel = models.IntegerField(blank=True, null=True)
    grado = models.IntegerField(blank=True, null=True)
    extra = models.CharField(max_length=50, blank=True, null=True)
    codigomodular = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'tipo_servicio'
        unique_together = (('id_tipo_servicio', 'id_colegio'),)


class TipoSexo(models.Model):
    id_sexo = models.CharField(primary_key=True, max_length=10)
    descripcion = models.CharField(max_length=10)
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tipo_sexo'


class TiposGrados(models.Model):
    id_tipo_grado = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=20)
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tipos_grados'


class TiposMedioPago(models.Model):
    id_tipo_medio = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=15)
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tipos_medio_pago'


class TiposNivel(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=15)
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tipos_nivel'


class Tiposdocumentos(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=25)
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tiposdocumentos'
