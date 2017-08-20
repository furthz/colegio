from __future__ import unicode_literals

from django.urls import reverse
from django.utils.functional import cached_property
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.db import models

from django.conf import settings

from utils.models import CreacionModificacionFechaProfileMixin, CreacionModificacionUserProfileMixin


class BaseProfile(CreacionModificacionFechaProfileMixin, CreacionModificacionUserProfileMixin, models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False, null=True)
    # Add more user profile fields here. Make sure they are nullable
    # or with default values
    picture = models.ImageField('Profile picture',
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    bio = models.CharField("Short Bio", max_length=200, blank=True, null=True)
    email_verified = models.BooleanField("Email verified", default=False)

    nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=200, blank=True, null=True)
    apellido_pa = models.CharField(max_length=50, null=True, blank=True)
    apellido_ma = models.CharField(max_length=50, blank=True, null=True)
    tipo_documento = models.IntegerField(null=True)
    numero_documento = models.CharField(db_index=True, max_length=15, null=True, db_column='numerodocumento')
    sexo = models.IntegerField(null=True)
    correo = models.EmailField(db_index= True, max_length=100, blank=True, null=True)
    fecha_nac = models.DateField(null=True)
    # fecha_creacion_persona = models.DateField()
    # fecha_modificacion_persona = models.DateField()
    # usuario_creacion_persona = models.CharField(max_length=10)
    # usuario_modificacion_persona = models.CharField(max_length=10)

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

        edad = datetime.now().date().year - self.fecha_nac.year

        años = edad

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

    class Meta:
        abstract = True
        #unique_together = (("tipo_documento", "numero_documento"),)

@python_2_unicode_compatible
class Profile(BaseProfile):
    id_persona = models.AutoField(primary_key=True)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:persona_detail', kwargs={'pk': self.pk})

    def full_detail(self):
        """
        Da una descripcion detallada de la informacion del Tipo de Servicio
        :return: lista de todos los atributos de la clase
        """
        detalle_completo = ["Nombres y Apellidos: {0}".format(self.getNombreCompleto),
                            "Tipo Documento: {0}".format(self.getTipoDocumento),
                            "Número Documento: {0}".format(self.numero_documento),
                            "Sexo: {0}".format(self.getSexo),
                            "Correo: {0}".format(self.correo),
                            "Edad: {0}".format(self.getEdad),
                            "Usuario creacion: {0}".format(self.usuario_creacion_persona),
                            "Fecha creacion: {0}".format(self.fecha_creacion_persona),
                            "Usuario modificacion: {0}".format(self.usuario_modificacion_persona),
                            "Fecha modificacion: {0}".format(self.fecha_modificacion_persona)
                            ]
        return detalle_completo

    def __str__(self):
        return "{}'s profile". format(self.user)

