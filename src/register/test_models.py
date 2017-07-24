# Create your tests here.

from django.test import TestCase

from .models import Persona
from .models import Apoderado
from datetime import date
from utils.models import TipoSexo
from utils.models import TipoDocumento


class ApoderadoModelTest(TestCase):
    def setUp(self):

        self.apoderado = Apoderado(nombre="Juan",
                                   segundo_nombre="Carlos",
                                   apellido_ma='Carrasco',
                                   apellido_pa="Bermudez",
                                   tipo_documento="DNI",
                                   numerodocumento="3344955",
                                   sexo="1",
                                   correo="sas",
                                   fecha_nac=date.today(),
                                   fecha_creacion=date.today(),
                                   fecha_modificacion=date.today(),
                                   usuario_modificacion="raul",
                                   usuario_creacion="raul",
                                   parentesco="Padre"
                                   )
        self.apoderado.save()

    def test_herenciaApoderadoPersonaTest(self):

        print("Nombre Persona: " + self.apoderado.persona.nombre)

        self.assertEquals(self.apoderado.nombre, "Juan")

    def test_Personasexo(self):

        tipo = TipoSexo.objects.create(descripcion="Masculino", activo=True)

        self.apoderado.sexo = tipo.id_sexo

        self.apoderado.save()

        print("Sexo: " + tipo.descripcion + " Apoderado.Sexo: " + self.apoderado.getSexo())

        self.assertEquals(self.apoderado.getSexo(), tipo.descripcion)

    def test_TipoDocumento(self):

        tipodoc = TipoDocumento.objects.create(descripcion="DNI", activo=True)

        self.apoderado.tipo_documento = tipodoc.id_tipo

        self.apoderado.save()

        print("TipoDocumento: " + tipodoc.descripcion + " Apoderado.TipoDoc: " + self.apoderado.getTipoDocumento())

        self.assertEquals(self.apoderado.getTipoDocumento(), tipodoc.descripcion)
