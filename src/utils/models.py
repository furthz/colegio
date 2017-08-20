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

    get_url_path.dont_recurse = True

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
    creator = models.BooleanField('Creator', max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Método para guardar el usuario logueado creador
        :param args:
        :param kwargs:
        :return:
        """
        from utils.middleware import get_current_user
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
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CreacionModificacionUserMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion = models.CharField('Usuario_Creacion', null=True, blank=True, max_length=10)
    usuario_modificacion = models.CharField('Usuario_Modificacion', null=True, blank=True, max_length=10)

    def save(self, *args, **kwargs):
        from utils.middleware import get_current_user

        usuario = get_current_user()
        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1

        # creacion
        if not self.pk:
            self.usuario_creacion = iduser

        self.usuario_modificacion = iduser

        super(CreacionModificacionUserMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionUserProfileMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion_persona = models.CharField('Usuario_Creacion', null=True, blank=True, max_length=10)
    usuario_modificacion_persona = models.CharField('Usuario_Modificacion', null=True, blank=True, max_length=10)

    def save(self, *args, **kwargs):
        from utils.middleware import get_current_user

        usuario = get_current_user()

        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1

        # creacion
        if not self.pk:
            self.usuario_creacion_persona = iduser

        self.usuario_modificacion_persona = iduser

        super(CreacionModificacionUserProfileMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionUserPersonalMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion_personal = models.CharField('Usuario_Creacion', null=True, blank=True, max_length=10,
                                                 db_column='usuario_creacion')
    usuario_modificacion_personal = models.CharField('Usuario_Modificacion', null=True, blank=True, max_length=10,
                                                     db_column='usuario_modificacion')

    def save(self, *args, **kwargs):
        from utils.middleware import get_current_user

        usuario = get_current_user()
        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1

        # creacion
        if not self.pk:
            self.usuario_creacion_personal = iduser

        self.usuario_modificacion_personal = iduser

        super(CreacionModificacionUserPersonalMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionUserApoderadoMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion_apoderado = models.CharField('Usuario_Creacion', null=True, blank=True, max_length=10,
                                                  db_column='usuario_creacion')
    usuario_modificacion_apoderado = models.CharField('Usuario_Modificacion', null=True, blank=True, max_length=10,
                                                      db_column='usuario_modificacion')

    def save(self, *args, **kwargs):
        from utils.middleware import get_current_user

        usuario = get_current_user()

        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1

        # creacion
        if not self.pk:
            self.usuario_creacion_apoderado = iduser

        self.usuario_modificacion_apoderado = iduser

        super(CreacionModificacionUserApoderadoMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionUserAlumnoMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion_alumno = models.CharField('Usuario_Creacion', null=True, blank=True, max_length=10,
                                               db_column='usuario_creacion')
    usuario_modificacion_alumno = models.CharField('Usuario_Modificacion', null=True, blank=True, max_length=10,
                                                   db_column='usuario_modificacion')

    def save(self, *args, **kwargs):
        from utils.middleware import get_current_user

        usuario = get_current_user()

        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1

        # creacion
        if not self.pk:
            self.usuario_creacion_alumno = iduser

        self.usuario_modificacion_alumno = iduser

        super(CreacionModificacionUserAlumnoMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True

class CreacionModificacionUserTesoreroMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion_tesorero = models.CharField('Usuario_Creacion', null=True, blank=True, max_length=10,
                                                 db_column='usuario_creacion')
    usuario_modificacion_tesorero = models.CharField('Usuario_Modificacion', null=True, blank=True, max_length=10,
                                                     db_column='usuario_modificacion')

    def save(self, *args, **kwargs):
        from utils.middleware import get_current_user

        usuario = get_current_user()

        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1

        # creacion
        if not self.pk:
            self.usuario_creacion_tesorero = iduser

        self.usuario_modificacion_tesorero = iduser

        super(CreacionModificacionUserTesoreroMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionUserPromotorMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion_promotor = models.CharField('Usuario_Creacion', null=True, blank=True, max_length=10,
                                                 db_column='usuario_creacion')
    usuario_modificacion_promotor = models.CharField('Usuario_Modificacion', null=True, blank=True, max_length=10,
                                                     db_column='usuario_modificacion')

    def save(self, *args, **kwargs):
        from utils.middleware import get_current_user

        usuario = get_current_user()

        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1

        # creacion
        if not self.pk:
            self.usuario_creacion_promotor = iduser

        self.usuario_modificacion_promotor = iduser

        super(CreacionModificacionUserPromotorMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionUserCajeroMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion_cajero = models.CharField('Usuario_Creacion', null=True, blank=True, max_length=10,
                                               db_column='usuario_creacion')
    usuario_modificacion_cajero = models.CharField('Usuario_Modificacion', null=True, blank=True, max_length=10,
                                                   db_column='usuario_modificacion')

    def save(self, *args, **kwargs):
        from utils.middleware import get_current_user

        usuario = get_current_user()

        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1

        # creacion
        if not self.pk:
            self.usuario_creacion_cajero = iduser

        self.usuario_modificacion_cajero = iduser

        super(CreacionModificacionUserCajeroMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionUserDirectorMixin(models.Model):
    """
    Clase abstracta para poder especificar los usuario:
        - Creacion
        - Modificacion
    """
    usuario_creacion_director = models.CharField('Usuario_Creacion', null=True, blank=True, max_length=10,
                                                 db_column='usuario_creacion')
    usuario_modificacion_director = models.CharField('Usuario_Modificacion', null=True, blank=True, max_length=10,
                                                     db_column='usuario_modificacion')

    def save(self, *args, **kwargs):
        from utils.middleware import get_current_user

        usuario = get_current_user()

        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1

        # creacion
        if not self.pk:
            self.usuario_creacion_director = iduser

        self.usuario_modificacion_director = iduser

        super(CreacionModificacionUserDirectorMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionFechaMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.fecha_creacion = timezone_now()
            self.fecha_modificacion = timezone_now()
        else:  # modificacion
            if not self.fecha_creacion:
                self.fecha_creacion = timezone_now()

        self.fecha_modificacion = timezone_now()

        super(CreacionModificacionFechaMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionFechaProfileMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion_persona = models.DateTimeField(blank=True, null=True)
    fecha_modificacion_persona = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.fecha_creacion_persona = timezone_now()
        else:  # modificacion
            if not self.fecha_creacion_persona:
                self.fecha_creacion_persona = timezone_now()

        self.fecha_modificacion_persona = timezone_now()

        super(CreacionModificacionFechaProfileMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionFechaPersonalMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion_personal = models.DateTimeField(blank=True, null=True, db_column="fecha_creacion")
    fecha_modificacion_personal = models.DateTimeField(blank=True, null=True, db_column="fecha_modificacion")

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.fecha_creacion_personal = timezone_now()
        else:  # modificacion
            if not self.fecha_creacion_personal:
                self.fecha_creacion_personal = timezone_now()

        self.fecha_modificacion_personal = timezone_now()

        super(CreacionModificacionFechaPersonalMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionFechaApoderadoMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion_apoderado = models.DateTimeField(blank=True, null=True, db_column="fecha_creacion")
    fecha_modificacion_apoderado = models.DateTimeField(blank=True, null=True, db_column="fecha_modificacion")

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.fecha_creacion_apoderado = timezone_now()
        else:  # modificacion
            if not self.fecha_creacion_apoderado:
                self.fecha_creacion_apoderado = timezone_now()

        self.fecha_modificacion_apoderado = timezone_now()

        super(CreacionModificacionFechaApoderadoMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionFechaAlumnoMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion_alumno = models.DateTimeField(blank=True, null=True, db_column="fecha_creacion")
    fecha_modificacion_alumno = models.DateTimeField(blank=True, null=True, db_column="fecha_modificacion")

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.fecha_creacion_alumno = timezone_now()
        else:  # modificacion
            if not self.fecha_creacion_alumno:
                self.fecha_creacion_alumno = timezone_now()

        self.fecha_modificacion_alumno = timezone_now()

        super(CreacionModificacionFechaAlumnoMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionFechaPromotorMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion_promotor = models.DateTimeField(blank=True, null=True, db_column="fecha_creacion")
    fecha_modificacion_promotor = models.DateTimeField(blank=True, null=True, db_column="fecha_modificacion")

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.fecha_creacion_promotor = timezone_now()
        else:  # modificacion
            if not self.fecha_creacion_promotor:
                self.fecha_creacion_promotor = timezone_now()

        self.fecha_modificacion_promotor = timezone_now()

        super(CreacionModificacionFechaPromotorMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionFechaTesoreroMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion_tesorero = models.DateTimeField(blank=True, null=True, db_column="fecha_creacion")
    fecha_modificacion_tesorero = models.DateTimeField(blank=True, null=True, db_column="fecha_modificacion")

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.fecha_creacion_tesorero = timezone_now()
        else:  # modificacion
            if not self.fecha_creacion_tesorero:
                self.fecha_creacion_tesorero = timezone_now()

        self.fecha_modificacion_tesorero = timezone_now()

        super(CreacionModificacionFechaTesoreroMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionFechaCajeroMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion_cajero = models.DateTimeField(blank=True, null=True, db_column="fecha_creacion")
    fecha_modificacion_cajero = models.DateTimeField(blank=True, null=True, db_column="fecha_modificacion")

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.fecha_creacion_cajero = timezone_now()
        else:  # modificacion
            if not self.fecha_creacion_cajero:
                self.fecha_creacion_cajero = timezone_now()

        self.fecha_modificacion_cajero = timezone_now()

        super(CreacionModificacionFechaCajeroMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreacionModificacionFechaDirectorMixin(models.Model):
    """
    Clase abstracta para definir las fechas de:
     - Fecha_creacion
     - Fecha_modificacion
    """
    fecha_creacion_director = models.DateTimeField(blank=True, null=True, db_column="fecha_creacion")
    fecha_modificacion_director = models.DateTimeField(blank=True, null=True, db_column="fecha_modificacion")

    def save(self, *args, **kwargs):
        # creación
        if not self.pk:
            self.fecha_creacion_director = timezone_now()
        else:  # modificacion
            if not self.fecha_creacion_director:
                self.fecha_creacion_director = timezone_now()

        self.fecha_modificacion_director = timezone_now()

        super(CreacionModificacionFechaDirectorMixin, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class TipoDocumento(ActivoMixin, models.Model):
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
        db_table = 'tipo_documento'

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
    id_sexo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=10)

    def __str__(self):
        return self.descripcion

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
