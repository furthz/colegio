"""
Modelos relacionados a los registros de las diferentes entidades

Autor: Raul Talledo <raul.talledo@technancial.com.pe>

Fecha: 23/07/2017

"""
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime
from utils.models import CreacionModificacionUserMixin, CreacionModificacionFechaMixin


class Persona(CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
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
    tipo_documento = models.CharField(max_length=25)
    numerodocumento = models.CharField(max_length=15)
    sexo = models.CharField(max_length=10)
    correo = models.CharField(max_length=100, blank=True, null=True)
    fecha_nac = models.DateField()

    class Meta:
        managed = False
        db_table = 'persona'

    def getNombreCompleto(self):
        """
        Método que concatena los nombres y apellidos

        :return: Nombre completo de la persona
        """
        nombrecompleto = self.nombre + " " + self.segundo_nombre + " " + self.apellido_pa + " " + self.apellido_ma

        return nombrecompleto

    def getEdad(self):
        """
        Método que calcula los años de una persona
        :return: La cantidad de años de la persona
        """

        edad = datetime.now().date() - self.fecha_nac

        diasedad = edad.days

        años = diasedad / 365

        return años

    def getSexo(self):
        """
        Método que retorna la descripción del tipo de sexo, cruzandolo con el catalogo TipoSexo

        :return: Descripción del catalogo TipoSexo
        """
        from utils.models import TipoSexo

        idsexo = self.sexo

        sexo = TipoSexo.objects.get(pk=idsexo)

        return sexo.descripcion

    def getTipoDocumento(self):
        """
        Método que retorna la descripción del tipo de documento, cruzándolo con el cataloto TipoDocumento
        :return: Descripción del catalogo TipoDocumento
        """

        from utils.models import TipoDocumento

        idtipo = self.tipo_documento

        tipodoc = TipoDocumento.objects.get(pk=idtipo)

        return tipodoc.descripcion


class Telefono(CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    """
    Clase que guarda toda la información relacionada a los teléfonos que pueden estar vinculado a model: #Personas
    o #Colegio
    """
    id_telefono = models.AutoField(primary_key=True)
    # id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    persona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='id_persona', related_name="telefonos")
    numero = models.IntegerField()
    tipo = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'telefono'


class Apoderado(Persona, models.Model):
    """
    Clase para identificar a los apoderados de los alumnos
    """
    id_apoderado = models.AutoField(primary_key=True)
    parentesco = models.CharField(max_length=30)
    persona = models.OneToOneField(Persona, models.DO_NOTHING, parent_link=True, )

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
    apoderados = models.ManyToManyField(Apoderado, db_table="apoderado_alumno", related_name="alumnos")

    class Meta:
        managed = False
        db_table = 'alumno'
