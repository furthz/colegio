"""
Modelos relacionados a los registros de las diferentes entidades

Autor: Raul Talledo <raul.talledo@technancial.com.pe>

Fecha: 23/07/2017

"""
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime
from utils.models import CreacionModificacionUserMixin, CreacionModificacionFechaMixin, ActivoMixin
from django.utils.functional import cached_property


class Persona(models.Model):
    """
    Clase para albergar todos los datos comunes a las personas
    que pueden ser:
        - Apoderados
        - Alumnos
        - Promotor
        - Director
        - Cajero
    """
    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=200, blank=True, null=True)
    apellido_pa = models.CharField(max_length=50)
    apellido_ma = models.CharField(max_length=50, blank=True, null=True)
    tipo_documento = models.IntegerField()
    numerodocumento = models.CharField(max_length=15)
    sexo = models.IntegerField()
    correo = models.CharField(max_length=100, blank=True, null=True)
    fecha_nac = models.DateField()
    fecha_creacion_persona = models.DateField()
    fecha_modificacion_persona = models.DateField()
    usuario_creacion_persona = models.CharField(max_length=10)
    usuario_modificacion_persona = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'persona'

    @cached_property
    def getNombreCompleto(self):
        """
        Método que concatena los nombres y apellidos

        :return: Nombre completo de la persona
        """

        return "{0} {1} {2} {3}".format(self.nombre, self.segundo_nombre, self.apellido_pa, self.apellido_ma)

    @property
    def getEdad(self):
        """
        Método que calcula los años de una persona
        :return: La cantidad de años de la persona
        """

        edad = datetime.now().date() - self.fecha_nac

        diasedad = edad.days

        años = diasedad / 365

        return años

    @property
    def getSexo(self):
        """
        Método que retorna la descripción del tipo de sexo, cruzandolo con el catalogo TipoSexo

        :return: Descripción del catalogo TipoSexo
        """
        from utils.models import TipoSexo

        idsexo = self.sexo

        sexo = TipoSexo.objects.get(pk=idsexo)

        return sexo.descripcion

    @property
    def getTipoDocumento(self):
        """
        Método que retorna la descripción del tipo de documento, cruzándolo con el cataloto TipoDocumento
        :return: Descripción del catalogo TipoDocumento
        """

        from utils.models import TipoDocumento

        idtipo = self.tipo_documento

        tipodoc = TipoDocumento.objects.get(pk=idtipo)

        return tipodoc.descripcion

class Personal(Persona, models.Model):
    """
    Clase para el Personal
    """
    id_personal = models.AutoField(primary_key=True)
    persona = models.OneToOneField(Persona, models.DO_NOTHING, parent_link=True)
    activo_personal = models.BooleanField(db_column="activo", default=True)
    fecha_creacion_personal = models.DateField(db_column="fecha_creacion")
    fecha_modificacion_personal = models.DateField(db_column="fecha_modificacion")
    usuario_creacion_personal = models.CharField(max_length=10, db_column="usuario_creacion")
    usuario_modificacion_personal = models.CharField(max_length=10, db_column="usuario_modificacion")

    def savePersonalFromPersona(self, persona: Persona, **atributos):
        """
        Método que permite guardar un Personal a partir de una persona existente
        :param persona: Persona existente
        :param atributos: Nuevos atributos propios de Apoderado
        :return: Objeto Personal creado
        """

        personalink = Personal._meta.parents.get(persona.__class__, None)

        if personalink is None:
            raise ValidationError(str("A %s no puede ser padre de %s" % (
                persona.__class__.__name__, self.__name__)))

        atributos[personalink.name] = persona

        for field in persona._meta.fields:
            atributos[field.name] = getattr(persona, field.name)

        personal = Personal(**atributos)
        personal.save()

        return personal

    class Meta:
        managed = False
        db_table = 'personal'
        unique_together = (('id_personal', 'persona'),)


class Colegio(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    Clase para el Colegio
    """
    id_colegio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11)
    ugel = models.CharField(max_length=100)
    personales = models.ManyToManyField(Personal, through='PersonalColegio', related_name='Colegios', null=True)

    class Meta:
        managed = False
        db_table = 'colegio'


class Telefono(ActivoMixin, CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    """
    Clase que guarda toda la información relacionada a los teléfonos que pueden estar vinculado a model: #Personas
    o #Colegio
    """
    id_telefono = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio', related_name="telefonos")
    persona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='id_persona', related_name="telefonos")
    numero = models.IntegerField()
    tipo = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'telefono'


class Direccion(CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    """
    Clase para hacer referencia a las direcciones
    """

    id_direccion = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='id_persona', related_name="direcciones")
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio', related_name="direcciones")
    calle = models.CharField(max_length=100)
    dpto = models.CharField(max_length=15)
    distrito = models.CharField(max_length=100)
    numero = models.CharField(max_length=6, blank=True, null=True)
    referencia = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direccion'


class Apoderado(Persona, models.Model):
    """
    Clase para identificar a los apoderados de los alumnos
    """
    id_apoderado = models.AutoField(primary_key=True)
    parentesco = models.CharField(max_length=30)
    persona = models.OneToOneField(Persona, models.DO_NOTHING, parent_link=True, )
    fecha_creacion_apoderado = models.DateField(db_column="fecha_creacion")
    fecha_modificacion_apoderado = models.DateField(db_column="fecha_modificacion")
    usuario_creacion_apoderado = models.CharField(max_length=10, db_column="usuario_creacion")
    usuario_modificacion_apoderado = models.CharField(max_length=10, db_column="usuario_modificacion")

    def saveApoderadoFromPersona(self, persona: Persona, **atributos):
        """
        Método que permite guardar un Apoderado a partir de una persona existente
        :param persona: Persona existente
        :param atributos: Nuevos atributos propios de Apoderado
        :return: Objeto Apoderado creado
        """

        personalink = Apoderado._meta.parents.get(persona.__class__, None)

        if personalink is None:
            raise ValidationError(str("A %s no puede ser padre de %s" % (
                persona.__class__.__name__, self.__name__)))

        atributos[personalink.name] = persona

        for field in persona._meta.fields:
            atributos[field.name] = getattr(persona, field.name)

        apo = Apoderado(**atributos)
        apo.save()

        return apo

    class Meta:
        managed = False
        db_table = 'apoderado'


class Alumno(Persona, models.Model):
    """
    Clase para identificar a los Alumnos
    """
    id_alumno = models.AutoField(primary_key=True)
    codigoint = models.CharField(max_length=15, blank=True, null=True)
    persona = models.OneToOneField(Persona, models.DO_NOTHING, parent_link=True)
    apoderados = models.ManyToManyField(Apoderado, through='ApoderadoAlumno', related_name='alumnos', null=True)
    fecha_creacion_alumno = models.DateField(db_column="fecha_creacion")
    fecha_modificacion_alumno = models.DateField(db_column="fecha_modificacion")
    usuario_creacion_alumno = models.CharField(max_length=10, db_column="usuario_creacion")
    usuario_modificacion_alumno = models.CharField(max_length=10, db_column="usuario_modificacion")

    def saveAlumnoFromPersona(self, persona: Persona, **atributos):
        """
        Método que permite guardar un Apoderado a partir de una persona existente
        :param persona: Persona existente
        :param atributos: Nuevos atributos propios de Apoderado
        :return: Objeto Alumno creado
        """

        personalink = Alumno._meta.parents.get(persona.__class__, None)

        if personalink is None:
            raise ValidationError(str("A %s no puede ser padre de %s" % (
                persona.__class__.__name__, self.__name__)))

        atributos[personalink.name] = persona

        for field in persona._meta.fields:
            atributos[field.name] = getattr(persona, field.name)

        alu = Alumno(**atributos)
        alu.save()

        return alu

    class Meta:
        managed = False
        db_table = 'alumno'


class ApoderadoAlumno(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    Clase para relacionar los Apoderado de los Alumnos
    """
    id_apoderadoalumno = models.AutoField(primary_key=True)
    apoderado = models.ForeignKey(Apoderado, models.DO_NOTHING, db_column='id_apoderado')
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')

    class Meta:
        managed = False
        db_table = 'apoderado_alumno'
        unique_together = (("apoderado", "alumno"),)



class Promotor(Personal, models.Model):
    """
    Clase para el Promotor
    """
    id_promotor = models.AutoField(primary_key=True)
    personalprom = models.OneToOneField(Personal, models.DO_NOTHING, parent_link=True, )
    activo_promotor = models.BooleanField(default=True, db_column="activo")
    fecha_creacion_promotor = models.DateField(db_column="fecha_creacion")
    fecha_modificacion_promotor = models.DateField(db_column="fecha_modificacion")
    usuario_creacion_promotor = models.CharField(max_length=10, db_column="usuario_creacion")
    usuario_modificacion_promotor = models.CharField(max_length=10, db_column="usuario_modificacion")

    def savePromotorFromPersonal(self, personal: Personal, **atributos):
        """
        # Método que permite guardar un Promotor a partir de un personal existente
        # :param personal: Personal existente
        # :param atributos: Nuevos atributos propios de Apoderado
        # :return: Objeto Promotor creado
        """

        personalink = Promotor._meta.parents.get(personal.__class__, None)

        if personalink is None:
            raise ValidationError(str("A %s no puede ser padre de %s" % (
                personal.__class__.__name__, self.__name__)))

        atributos[personalink.name] = personal

        for field in personal._meta.fields:
            atributos[field.name] = getattr(personal, field.name)

        promotor = Promotor(**atributos)
        promotor.save()

        return promotor

    class Meta:
        managed = False
        db_table = 'promotor'


class Cajero(Personal, models.Model):
    """
    Clase para el Cajero
    """
    id_cajero = models.AutoField(primary_key=True)
    personalcajero = models.OneToOneField(Personal, models.DO_NOTHING, parent_link=True, )
    activo_cajero = models.BooleanField(default=True, db_column="activo")
    fecha_creacion_cajero = models.DateField(db_column="fecha_creacion")
    fecha_modificacion_cajero = models.DateField(db_column="fecha_modificacion")
    usuario_creacion_cajero = models.CharField(max_length=10, db_column="usuario_creacion")
    usuario_modificacion_cajero = models.CharField(max_length=10, db_column="usuario_modificacion")

    def saveCajeroFromPersonal(self, personal: Personal, **atributos):
        """
        # Método que permite guardar un Promotor a partir de un personal existente
        # :param personal: Personal existente
        # :param atributos: Nuevos atributos propios de Apoderado
        # :return: Objeto Promotor creado
        """

        personalink = Cajero._meta.parents.get(personal.__class__, None)

        if personalink is None:
            raise ValidationError(str("A %s no puede ser padre de %s" % (
                personal.__class__.__name__, self.__name__)))

        atributos[personalink.name] = personal

        for field in personal._meta.fields:
            atributos[field.name] = getattr(personal, field.name)

        cajero = Cajero(**atributos)
        cajero.save()

        return cajero

    class Meta:
        managed = False
        db_table = 'cajero'


class Director(Personal, models.Model):
    """
    Clase para el Director
    """
    id_director = models.AutoField(primary_key=True)
    personaldirector = models.OneToOneField(Personal, models.DO_NOTHING, parent_link=True, )
    activo_director = models.BooleanField(default=True, db_column="activo")
    fecha_creacion_director = models.DateField(db_column="fecha_creacion")
    fecha_modificacion_director = models.DateField(db_column="fecha_modificacion")
    usuario_creacion_director = models.CharField(max_length=10, db_column="usuario_creacion")
    usuario_modificacion_director = models.CharField(max_length=10, db_column="usuario_modificacion")

    def saveDirectorFromPersonal(self, personal: Personal, **atributos):
        """
        # Método que permite guardar un Promotor a partir de un personal existente
        # :param personal: Personal existente
        # :param atributos: Nuevos atributos propios de Apoderado
        # :return: Objeto Promotor creado
        """

        personalink = Director._meta.parents.get(personal.__class__, None)

        if personalink is None:
            raise ValidationError(str("A %s no puede ser padre de %s" % (
                personal.__class__.__name__, self.__name__)))

        atributos[personalink.name] = personal

        for field in personal._meta.fields:
            atributos[field.name] = getattr(personal, field.name)

        director = Director(**atributos)
        director.save()

        return director

    class Meta:
        managed = False
        db_table = 'director'


class PersonalColegio(ActivoMixin, CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    """
    Clase que relacion el Personal con un Colegio
    """
    id_personal_colegio = models.AutoField(primary_key=True)
    personal = models.ForeignKey(Personal, models.DO_NOTHING, db_column="id_personal")
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")


    class Meta:
        managed = False
        db_table = 'personal_colegio'
        #unique_together = (("apoderado", "alumno"),)