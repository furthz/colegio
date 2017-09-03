from django.db import models
from django.urls import reverse
from register.models import Colegio
from enrollment.models import Servicio
from enrollment.models import Matricula
from register.models import PersonalColegio
from utils.models import ActivoMixin
from utils.models import CreacionModificacionFechaMixin
from utils.models import CreacionModificacionUserMixin
# Create your models here.

class TipoDescuento(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    colegio:        colegio al que le pertenece el tipo de descuento
    servicio:       servicio sobre el cual el descuento tiene efecto
    descripcion:    mas informacion sobre el tipo de descuento
    porcentaje:     porjentaje de descuento
    """
    id_tipo_descuento = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    servicio = models.ForeignKey(Servicio, models.DO_NOTHING, db_column='id_servicio')
    descripcion = models.CharField(max_length = 50)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=10)

    def __str__(self):

        return self.descripcion

    def full_detail(self):
        """
        Da una descripcion detallada de la informacion del Tipo de Descuento
        :return: lista de todos los atributos de la clase
        """
        detalle_completo = []
        return detalle_completo

    class Meta:
        managed = False
        db_table = 'tipo_descuento'
        #unique_together = (('id_tipo_servicio', 'colegio'),)

class Descuento(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    personal_colegio:   personal del colegio que puede aprobar o denegar un descuento
    tipo_descuento:     tipo de descuento que se solicita
    numero_expediente:  nuemro del expediente fisico con los documentos del solicitante
    comentario:         comentario u observacion sobre la solicitud de descuento
    estado:             estado de la solicitud (proceso, aprobado, denegado)
    """
    id_descuento = models.AutoField(primary_key=True)
    personal_colegio = models.ForeignKey(PersonalColegio, models.DO_NOTHING, db_column='id_persona_colegio')
    matricula = models.ForeignKey(Matricula, models.DO_NOTHING, db_column='id_matricula')
    tipo_descuento = models.ForeignKey(TipoDescuento, models.DO_NOTHING, db_column='id_tipo_descuento')
    numero_expediente = models.IntegerField()
    comentario = models.CharField(max_length=200, null=True, blank=True)
    estado = models.IntegerField()
    fecha_solicitud = models.DateField()
    fecha_aprobacion = models.DateField(null=True, blank=True)


    class Meta:
        managed = False
        db_table = 'descuento'

