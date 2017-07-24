"""
Modelos relacionados a los registros de las diferentes entidades

Autor: Raul Talledo <raul.talledo@technancial.com.pe>

Fecha: 23/07/2017

"""
from django.db import models
from datetime import datetime


# Create your models here.

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
    tipo_documento = models.CharField(max_length=25)
    numerodocumento = models.CharField(max_length=15)
    sexo = models.CharField(max_length=10)
    correo = models.CharField(max_length=100, blank=True, null=True)
    fecha_nac = models.DateField()
    fecha_creacion = models.DateField()
    fecha_modificacion = models.DateField()
    usuario_modificacion = models.CharField(max_length=10, null=True)
    usuario_creacion = models.CharField(max_length=10, null=True)

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
        Método que retorna la descripción del tipo de sexo,
        cruzandolo con el catalogo TipoSexo

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




class Apoderado(Persona, models.Model):
    """

    """
    id_apoderado = models.AutoField(primary_key=True)
    parentesco = models.CharField(max_length=30)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, parent_link=True)

    class Meta:
        managed = False
        db_table = 'apoderado'
