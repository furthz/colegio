"""
Modelos relacionados a los registros de las diferentes entidades

Autor: Raul Talledo <raul.talledo@technancial.com.pe>

Fecha: 23/07/2017

"""

from django.db import models
from django.urls import reverse

from utils.middleware import get_current_colegio
from utils.misc import insert_child
from utils.models import CreacionModificacionUserMixin, CreacionModificacionFechaPersonalMixin, \
    CreacionModificacionFechaApoderadoMixin, CreacionModificacionFechaAlumnoMixin, \
    CreacionModificacionFechaPromotorMixin, CreacionModificacionFechaCajeroMixin, \
    CreacionModificacionFechaDirectorMixin, \
    CreacionModificacionUserPersonalMixin, CreacionModificacionUserApoderadoMixin, \
    CreacionModificacionUserAlumnoMixin, \
    CreacionModificacionUserPromotorMixin, CreacionModificacionUserCajeroMixin, CreacionModificacionUserDirectorMixin, \
    CreacionModificacionUserTesoreroMixin, CreacionModificacionFechaTesoreroMixin, \
    CreacionModificacionUserAdministrativoMixin, CreacionModificacionFechaAdministrativoMixin, \
    CreacionModificacionUserProveedorMixin, CreacionModificacionFechaProveedorMixin
from utils.models import CreacionModificacionFechaMixin
from utils.models import ActivoMixin
from profiles.models import Profile


class Personal(CreacionModificacionUserPersonalMixin, CreacionModificacionFechaPersonalMixin, Profile, models.Model):
    """
    Clase para el Personal
    """
    id_personal = models.AutoField(primary_key=True)
    persona = models.OneToOneField(Profile, models.DO_NOTHING, parent_link=True)
    activo_personal = models.BooleanField(db_column="activo", default=True)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:personal_detail', kwargs={'pk': self.pk})

    @staticmethod
    def saveFromPersona(per: Profile, **atributos):

        try:
            personal = Personal.objects.get(persona=per)
            return personal
        except Personal.DoesNotExist:
            return insert_child(obj=per, child_model=Personal, **atributos)

    def __str__(self):
        return "Personal ID: {0}".format(self.id_personal)

    class Meta:
        managed = True
        db_table = 'personal'


class Colegio(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    Clase para el Colegio
    """
    id_colegio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11)
    ugel = models.CharField(max_length=100)
    personales = models.ManyToManyField(Personal, through='PersonalColegio', related_name='Colegios', null=True)


    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'colegio'


class Telefono(ActivoMixin, CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    """
    Clase que guarda toda la información relacionada a los teléfonos que pueden estar vinculado a model: #Personas
    o #Colegio
    """
    id_telefono = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio', related_name="telefonos")
    persona = models.ForeignKey(Profile, models.DO_NOTHING, db_column='id_persona', related_name="telefonos")
    numero = models.IntegerField()
    tipo = models.CharField(max_length=10)

    def __str__(self):
        return str(self.numero)

    class Meta:
        managed = True
        db_table = 'telefono'


class Direccion(CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    """
    Clase para hacer referencia a las direcciones
    """

    id_direccion = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Profile, models.DO_NOTHING, db_column='id_persona', related_name="direcciones")
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio', related_name="direcciones")
    calle = models.CharField(max_length=100)
    dpto = models.CharField(max_length=15)
    provincia = models.CharField(max_length=15)
    distrito = models.CharField(max_length=100)
    numero = models.CharField(max_length=6, blank=True, null=True)
    referencia = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'direccion'


class Apoderado(CreacionModificacionUserApoderadoMixin, CreacionModificacionFechaApoderadoMixin, Profile, models.Model):
    """
    Clase para identificar a los apoderados de los alumnos
    """
    id_apoderado = models.AutoField(primary_key=True)
    parentesco = models.CharField(max_length=30)
    persona = models.OneToOneField(Profile, models.DO_NOTHING, parent_link=True, )

    def full_detail(self):
        lista = Profile.full_detail(self)
        lista.append("parentesco: {0}".format(self.parentesco))
        return lista

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:apoderado_detail', kwargs={'pk': self.pk})

    @staticmethod
    def saveFromPersona(per: Profile, **atributos):
        """
        Método que permite guardar un Apoderado a partir de una persona existente
        :param per: Persona base
        :param atributos: Nuevos atributos propios de Apoderado
        :return: Objeto Apoderado creado
        """
        try:
            apoderado = Apoderado.objects.get(persona=per)
            return apoderado
        except Apoderado.DoesNotExist:
            return insert_child(obj=per, child_model=Apoderado, **atributos)

    class Meta:
        managed = True
        db_table = 'apoderado'


class Alumno(CreacionModificacionUserAlumnoMixin, CreacionModificacionFechaAlumnoMixin, Profile, models.Model):
    """
    Clase para identificar a los Alumnos
    """
    id_alumno = models.AutoField(primary_key=True)
    codigoint = models.CharField(max_length=15, blank=True, null=True)
    persona = models.OneToOneField(Profile, models.DO_NOTHING, parent_link=True, unique=True)
    apoderados = models.ManyToManyField(Apoderado, through='ApoderadoAlumno', related_name='alumnos', null=True)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:alumno_detail', kwargs={'pk': self.pk})

    @staticmethod
    def saveFromPersona(per: Profile, **atributos):
        """
        Método que permite guardar un Apoderado a partir de una persona existente
        :param per: Persona existente
        :param atributos: Nuevos atributos propios de Apoderado
        :return: Objeto Alumno creado
        """
        try:
            alu = Alumno.objects.get(persona=per)
            return alu
        except Alumno.DoesNotExist:
            return insert_child(obj=per, child_model=Alumno, **atributos)

    def __str__(self):
        return self.getNombreCompleto

    class Meta:
        managed = True
        db_table = 'alumno'


class ApoderadoAlumno(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    Clase para relacionar los Apoderado de los Alumnos
    """
    id_apoderadoalumno = models.AutoField(primary_key=True)
    apoderado = models.ForeignKey(Apoderado, models.DO_NOTHING, db_column='id_apoderado')
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')

    class Meta:
        managed = True
        db_table = 'apoderado_alumno'
        unique_together = (("apoderado", "alumno"),)


# POR ARREGLAR
class Tesorero(CreacionModificacionUserTesoreroMixin, CreacionModificacionFechaTesoreroMixin, Personal, models.Model):
    id_tesorero = models.AutoField(primary_key=True)
    empleado = models.OneToOneField(Personal, models.DO_NOTHING, parent_link=True)
    activo_tesorero = models.BooleanField(default=True, db_column="activo")

    def __str__(self):
        return "Id Tesorero: {0}".format(self.id_tesorero)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:tesorero_detail', kwargs={'pk': self.pk})

    @staticmethod
    def saveFromPersonal(per: Personal, **atributos):
        """
        # Método que permite guardar un Promotor a partir de un personal existente
        # :param personal: Personal existente
        # :param atributos: Nuevos atributos propios de Apoderado
        # :return: Objeto Promotor creado
        """
        try:
            tesorero = Tesorero.objects.get(persona=per)
            return tesorero
        except Tesorero.DoesNotExist:
            return insert_child(obj=per, child_model=Tesorero, **atributos)

    class Meta:
        managed = True
        db_table = 'tesorero'


class Promotor(CreacionModificacionUserPromotorMixin, CreacionModificacionFechaPromotorMixin, Personal, models.Model):
    """
    Clase para el Promotor
    """
    id_promotor = models.AutoField(primary_key=True)
    empleado = models.OneToOneField(Personal, models.DO_NOTHING, parent_link=True)
    activo_promotor = models.BooleanField(default=True, db_column="activo")

    def __str__(self):
        return "Id Promotor: {0}".format(self.id_promotor)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:promotor_detail', kwargs={'pk': self.pk})

    @staticmethod
    def saveFromPersonal(per: Personal, **atributos):
        """
        # Método que permite guardar un Promotor a partir de un personal existente
        # :param personal: Personal existente
        # :param atributos: Nuevos atributos propios de Apoderado
        # :return: Objeto Promotor creado
        """
        try:
            promotor = Promotor.objects.get(persona=per)
            return promotor
        except Promotor.DoesNotExist:
            return insert_child(obj=per, child_model=Promotor, **atributos)

    class Meta:
        managed = True
        db_table = 'promotor'


class Cajero(CreacionModificacionUserCajeroMixin, CreacionModificacionFechaCajeroMixin, Personal, models.Model):
    """
    Clase para el Cajero
    """
    id_cajero = models.AutoField(primary_key=True)
    empleado = models.OneToOneField(Personal, models.DO_NOTHING, parent_link=True)
    activo_cajero = models.BooleanField(default=True, db_column="activo")

    def __str__(self):
        return "Id Cajero: {0}".format(self.id_cajero)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:cajero_detail', kwargs={'pk': self.pk})

    @staticmethod
    def saveFromPersonal(per: Personal, **atributos):
        """
        # Método que permite guardar un Promotor a partir de un personal existente
        # :param personal: Personal existente
        # :param atributos: Nuevos atributos propios de Apoderado
        # :return: Objeto Promotor creado
        """
        try:
            cajero = Cajero.objects.get(persona=per)
            return cajero
        except Cajero.DoesNotExist:
            return insert_child(obj=per, child_model=Cajero, **atributos)

    class Meta:
        managed = True
        db_table = 'cajero'


class Director(CreacionModificacionUserDirectorMixin, CreacionModificacionFechaDirectorMixin, Personal, models.Model):
    """
    Clase para el Director
    """
    id_director = models.AutoField(primary_key=True)
    empleado = models.OneToOneField(Personal, models.DO_NOTHING, parent_link=True, )
    activo_director = models.BooleanField(default=True, db_column="activo")

    def __str__(self):
        return "Id Director: {0}".format(self.id_director)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:director_detail', kwargs={'pk': self.pk})

    @staticmethod
    def saveFromPersonal(per: Personal, **atributos):
        """
        # Método que permite guardar un Promotor a partir de un personal existente
        # :param personal: Personal existente
        # :param atributos: Nuevos atributos propios de Apoderado
        # :return: Objeto Promotor creado        """
        try:
            alu = Director.objects.get(persona=per)
            return alu
        except Director.DoesNotExist:
            return insert_child(obj=per, child_model=Director, **atributos)

    class Meta:
        managed = True
        db_table = 'director'


class PersonalColegio(ActivoMixin, CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    """
    Clase que relacion el Personal con un Colegio
    """
    id_personal_colegio = models.AutoField(primary_key=True)
    personal = models.ForeignKey(Personal, models.DO_NOTHING, db_column="id_personal")
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")

    class Meta:
        managed = True
        db_table = 'personal_colegio'


class Administrativo(CreacionModificacionUserAdministrativoMixin, CreacionModificacionFechaAdministrativoMixin,
                     Personal, models.Model):
    """
    Clase que parmite crear el rol de administrativos
    """
    id_administrativo = models.AutoField(primary_key=True)
    empleado = models.OneToOneField(Personal, models.DO_NOTHING, parent_link=True)
    activo_administrativo = models.BooleanField(default=True, db_column="activo")

    def __str__(self):
        return "Id Administrativo: {0}".format(self.id_tesorero)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:administrativo_detail', kwargs={'pk': self.pk})

    @staticmethod
    def saveFromPersonal(per: Personal, **atributos):
        """
        # Método que permite guardar un Promotor a partir de un personal existente
        # :param personal: Personal existente
        # :param atributos: Nuevos atributos propios de Apoderado
        # :return: Objeto Promotor creado
        """
        try:
            admin = Administrativo.objects.get(persona=per)
            return admin
        except Administrativo.DoesNotExist:
            return insert_child(obj=per, child_model=Administrativo, **atributos)

    class Meta:
        managed = True
        db_table = 'administrativo'


class Proveedor(CreacionModificacionUserProveedorMixin, CreacionModificacionFechaProveedorMixin,models.Model):
    """
    Clase para identificar a los proveedores
    """
    id_proveedor = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=100)
    ruc = models.CharField(max_length=15)

    def __str__(self):
        return self.razon_social

    def full_detail(self):
        lista = Profile.full_detail(self)
        lista.append("razon social: {0}".format(self.razon_social))
        return lista

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles de la persona
        """
        return reverse('registers:proveedor_detail', kwargs={'pk': self.pk})


    class Meta:
        managed = True
        db_table = 'proveedor'

class ProvedorColegio(ActivoMixin,CreacionModificacionUserProveedorMixin, CreacionModificacionFechaProveedorMixin,models.Model):
    """
    Proveedor Colegio
    """
    id_proveedor_colegio = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column="id_proveedor")
    colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column="id_colegio")

    class Meta:
        managed = True
        db_table = 'proveedor_colegio'

    def __str__(self):
        return self.proveedor.razon_social