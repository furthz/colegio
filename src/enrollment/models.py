from django.db import models
from django.urls import reverse
from utils.models import TiposNivel
from utils.models import TiposGrados
# Create your models here.

class Colegio(models.Model):
    """
    Nombre:     nombre del colegio
    RUC:        ruc perteneciente al colegio
    UGEL:       ugel a la cual pertenece el colegio
    """
    id_colegio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11)
    ugel = models.CharField(max_length=100)
    fecha_creacion = models.DateField()
    fecha_modificacion = models.DateField()
    usuario_creacion = models.CharField(max_length=10)
    usuario_modificacion = models.CharField(max_length=10)

    def __str__(self):
        """
        Solo retorna informacion de la clase como string
        :return: nombre del servicio
        """
        return self.nombre

    class Meta:
        managed = False
        db_table = 'colegio'


class TipoServicio(models.Model):
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
    nivel = models.ForeignKey(TiposNivel, models.DO_NOTHING, db_column='nivel')
    #nivel = models.IntegerField(blank=True, null=True)
    grado = models.ForeignKey(TiposGrados, models.DO_NOTHING, db_column='grado')
    #grado = models.IntegerField(blank=True, null=True)
    extra = models.CharField(max_length=50, blank=True, null=True)
    codigo_modular = models.CharField(max_length=10)
    fecha_creacion = models.DateField()
    fecha_modificacion = models.DateField()
    usuario_creacion = models.CharField(max_length=10, blank=True, null=True)
    usuario_modificacion = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        """
        Solo retorna informacion de la clase como string
        :return: nombre del servicio
        """
        return "nivel: {0}   grado: {1}   extra: {2}".format(self.nivel,self.grado,self.extra)

    def full_detail(self):
        """
        Da una descripcion detallada de la informacion del Tipo de Servicio
        :return: lista de todos los atributos de la clase
        """
        detalle_completo = ["Nivel: {0}".format(self.nivel),
                            "Grado: {0}".format(self.grado),
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
        :return:
        """
        return reverse('enrollments:tiposervicio_detail', kwargs={'pk': self.pk})
        #return "/servicios/impdates/list/{0}/".format(str(self.pk))

    class Meta:
        managed = False
        db_table = 'tipo_servicio'
        #unique_together = (('id_tipo_servicio', 'colegio'),)

class Servicio(models.Model):
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
    fecha_creacion = models.DateField()
    fecha_modificacion = models.DateField()
    usuario_creacion = models.CharField(max_length=10, blank=True, null=True)
    usuario_modificacion = models.CharField(max_length=10, blank=True, null=True)

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
        :return:
        """
        return reverse('enrollments:servicio_list', kwargs={'pkts': self.tipo_servicio.pk})
        #return "/servicios/impdates/list/{0}/listservicios".format(str(self.tipo_servicio.id_tipo_servicio))

    class Meta:
        managed = False
        db_table = 'servicio'


