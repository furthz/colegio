"""

Modelo de las clases soporte para la aplicación

:author: Raul Talledo <raul.talledo@technancial.com.pe>

Creado 15/07/2017

"""
from __future__ import unicode_literals
from django.db import models
from urllib.parse import urlparse
from django.conf import settings
from django.utils.timezone import now as timezone_now


class UrlMixin(models.Model):
    """
    Un reemplazo para get_absolute_url()
    Los modelos que extienden de este mixin deberían tener implementado ambos:
        - get_url
        - get_url_path
    """

    class Meta:
        abstract = True

    def get_url(self):
        """
        Método que obtiene la url del objeto
        :return: ruta
        """
        if hasattr(self.get_url, "dont_recurse"):
            raise NotImplementedError

        try:
            path = self.get_url
        except NotImplementedError:
            raise

        website_url = getattr(settings, "DEFAULT_WEBSITE_URL", "http://127.0.0.1:8000")

        return website_url + path

    def get_url_path(self):
        """
        Metodo que obtiene la url del objetos
        :return: ruta
        """
        if hasattr(self.get_url, "dont_recurse"):
            raise NotImplementedError

        try:
            url = self.get_url
        except NotImplementedError:
            raise
        bits = urlparse(url)

        return urlparse(("", "") + bits[2:])

    def get_absolute_url(self):
        """
        Método que devuelve la url absoluta del objeto
        :return: ruta
        """
        return self.get_url_path()


class MetaTagsMixin(models.Model):
    """
    Clase abstracta para los tags en la sección <HEAD>
    """
    meta_keywords = models.CharField('Keywords', max_length=255, blank=True,
                                     help_text='Separa los Keywords por comas', )

    meta_description = models.CharField('Description', max_length=255, blank=True, )

    meta_author = models.CharField('Author', max_length=255, blank=True, )

    meta_copyright = models.CharField('Copyright', max_length=255, blank=True, )

    class Meta:
        abstract = True


class CreatorMixin(models.Model):
    """
    clase abstracta para obtener el creador
    """
    creator = models.BooleanField('Creator', max_length=255, blank=True)

    def save(self, *args, **kwargs):
        """
        Método para guardar el usuario logueado creador
        :param args:
        :param kwargs:
        :return:
        """
        from src.utils.middleware import get_current_user
        if not self:
            self.creator = get_current_user()
        super(CreatorMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class ActivoMixin(models.Model):
    """
    Clase abstracta para definir aquellas que tendrán el campo Activo
    """
    activo = models.BooleanField()

    class Meta:
        abstract = True


class CreacionModificacionUserMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion = models.CharField('Usuario_Creacion', max_length=10)
    usuario_modificacion = models.CharField('Usuario_Modificacion', max_length=10)

    class Meta:
        abstract = True


class CreacionModificacionFechaMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion = models.DateTimeField()
    fecha_modificacion = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.fecha_creacion = timezone_now()
        else:
            if not self.fecha_creacion:
                self.fecha_creacion = timezone_now()

            self.fecha_modificacion = timezone_now()

        super(CreacionModificacionFechaMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class Tiposdocumentos(ActivoMixin, models.Model):
    """
    clase para definir el catalogo de tipos de documentos
    Campos:
        - id_tipo: clave incremental
        - descripción: nombre del tipo de documento
        - activo: para identificar si el registro está habilitado

    """
    id_tipo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'tiposdocumentos'

    def __str__(self):
        return self.descripcion


class TipoSexo(ActivoMixin, models.Model):
    """
    Clase para definir el catalogo de tipos de sexo
    Campos:
        - id_sexo: identificador
        - descripción: nombre a utilzar para definir el sexo
        - activo: identificar si el registro está habilitado
    """
    id_sexo = models.CharField(primary_key=True, max_length=10)
    descripcion = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'tipo_sexo'


class TiposGrados(ActivoMixin, models.Model):
    """
    Clase para definir los tipos de grados
    Campos:
        - id_tipo_grado: identificador
        - descripición: nombre del tipo de grado
        - activo: identificador para ver si el registro está habilitado
    """
    id_tipo_grado = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tipos_grados'


class TiposMedioPago(ActivoMixin, models.Model):
    """
    Clase para definir el catalogo de los medios de pago
    Campos:
        - id_tipo_medio: identificador
        - descripción: nombre del tipo de medio de pago
        - activo: identificador para ver si el registro está activo
    """
    id_tipo_medio = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'tipos_medio_pago'


class TiposNivel(ActivoMixin, models.Model):
    """
    Clase para definir los tipos de nivel disponibles
    Campos:
        - id_tipo: identificador
        - descripción: nombre de los tipos de nivel
        - activo: identificador para ver si el registro está activo
    """
    id_tipo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'tipos_nivel'
