from django.db import models
from django.urls import reverse
from register.models import Colegio
from register.models import Alumno
from utils.models import ActivoMixin
from utils.models import CreacionModificacionFechaMixin
from utils.models import CreacionModificacionUserMixin
# Create your models here.

class TipoServicio(CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    isordinario:        indica si el servicio es ordinario (1er grado, 2do grado, etc.)
                        o extra (curso de verano, danza, etc.)
    nivel:              indica el nivel que el colegio puede dictar (inicial, primaria, secundaria)
    grado:              indica los grados que el colegio puede dictar
    extra:              curso extraordinarios que el colegio dicta
    codigomodular:      numero que identifica al colegio
    """
    id_tipo_servicio = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    is_ordinario = models.BooleanField()
    nivel = models.IntegerField(blank=True, null=True)
    grado = models.IntegerField(blank=True, null=True)
    extra = models.CharField(max_length=50, blank=True, null=True)
    codigo_modular = models.CharField(max_length=10)

    def __str__(self):
        """
        Solo retorna informacion de la clase como string
        :return: nombre del servicio
        """
        return "nivel: {0}   grado: {1}   extra: {2}".format(self.getTipoNivel,self.getTipoGrado,self.extra)

    def full_detail(self):
        """
        Da una descripcion detallada de la informacion del Tipo de Servicio
        :return: lista de todos los atributos de la clase
        """
        detalle_completo = ["Nivel: {0}".format(self.getTipoNivel),
                            "Grado: {0}".format(self.getTipoGrado),
                            "Extra: {0}".format(self.extra),
                            "Codigo modular: {0}".format(self.codigo_modular),
                            "Fecha creacion: {0}".format(self.fecha_creacion),
                            "Fecha modificacion: {0}".format(self.fecha_modificacion),
                            "Usuario creacion: {0}".format(self.usuario_creacion),
                            "Usuario modificacion: {0}".format(self.usuario_modificacion)
                            ]
        return detalle_completo

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles del tipo de servicio
        """
        return reverse('enrollments:tiposervicio_detail', kwargs={'pk': self.pk})
        #return "/servicios/impdates/list/{0}/".format(str(self.pk))

    @property
    def getTipoNivel(self):
        """
        Método que retorna la descripción del tipo de nivel, cruzándolo con el cataloto TipoNivel
        :return: Descripción del catalogo TipoNivel
        """

        from utils.models import TiposNivel

        idtipo = self.nivel

        tipodoc = TiposNivel.objects.get(pk=idtipo)

        return tipodoc.descripcion

    @property
    def getTipoGrado(self):
        """
        Método que retorna la descripción del tipo de grado, cruzándolo con el cataloto TiposGrados
        :return: Descripción del catalogo TiposGrados
        """

        from utils.models import TiposGrados

        idtipo = self.grado

        tipodoc = TiposGrados.objects.get(pk=idtipo)

        return tipodoc.descripcion

    class Meta:
        managed = False
        db_table = 'tipo_servicio'
        #unique_together = (('id_tipo_servicio', 'colegio'),)

class Servicio(CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    nombre:         nombre del servicio
    precio:         precio del servicio
    isperiodic:     indica si el servicio tiene un costo periodico o no
    fechafacturar:  indica la fecha de facturacion
    cuotas:         indica el numero de cuotas en caso de ser periodico
    """
    id_servicio = models.AutoField(primary_key=True)
    tipo_servicio = models.ForeignKey('TipoServicio', models.DO_NOTHING, db_column='id_tipo_servicio')
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    is_periodic = models.BooleanField()
    fecha_facturar = models.DateField()
    cuotas = models.IntegerField()

    def __str__(self):
        """
        Solo retorna informacion de la clase como string
        :return: nombre del servicio
        """
        return  "Servicio:  {0}    ------------------- precio: {1}".format(self.nombre,self.precio)

    def full_detail(self):
        """
        Da una descripcion detallada de la informacion del servicio
        :return: lista de todos los atributos de la clase
        """
        detalle_completo = ["Descripcion: {0}".format(self.nombre),
                            "Precio: {0}".format(self.precio),
                            "Fecha Facturacion: {0}".format(self.fecha_facturar),
                            "Cuotas: {0}".format(self.cuotas),
                            "Fecha creacion: {0}".format(self.fecha_creacion),
                            "Fecha modificacion: {0}".format(self.fecha_modificacion),
                            "Usuario creacion: {0}".format(self.usuario_creacion),
                            "Usuario modificacion: {0}".format(self.usuario_modificacion)
                            ]
        return detalle_completo

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de la lista de servicios
        """
        return reverse('enrollments:servicio_list', kwargs={'pkts': self.tipo_servicio.pk})
        #return "/servicios/impdates/list/{0}/listservicios".format(str(self.tipo_servicio.id_tipo_servicio))

    class Meta:
        managed = False
        db_table = 'servicio'


class Matricula( CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    """

    """
    id_matricula = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    tipo_servicio = models.ForeignKey(TipoServicio, models.DO_NOTHING, db_column='id_tipo_servicio')

    def __str__(self):
        """

        :return:
        """
        return "El alumno: {0} esta registrado en {1}".format(self.alumno.persona.getNombreCompleto, self.tipo_servicio)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de la lista de servicios
        """
        return reverse('enrollments:matricula_list')

    class Meta:
        managed = False
        db_table = 'matricula'

class Cuentascobrar(CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """

    """
    id_cuentascobrar = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(Matricula, models.DO_NOTHING, db_column='id_matricula')
    servicio = models.ForeignKey(Servicio, models.DO_NOTHING, db_column='id_servicio')
    fecha_ven = models.DateField()
    comentario = models.CharField(max_length=500, blank=True, null=True)
    estado = models.BooleanField()
    precio = models.FloatField()
    deuda = models.FloatField()

    class Meta:
        managed = False
        db_table = 'cuentascobrar'


