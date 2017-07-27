# Create your tests here.

from django.test import TestCase

from .models import Apoderado
from datetime import date
from utils.models import TipoSexo
from utils.models import TipoDocumento
from .models import Telefono
from .models import Alumno
from .models import Persona


class PersonaModelTest(TestCase):
    def setUp(self):
        self.persona = Persona(nombre="Juan",
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
                               usuario_creacion="raul"
                               )
        self.persona.save()

        print("idpersonainicio: " + str(self.persona.id_persona))

    def test_PersonaAddApoderado(self):
        apo = Apoderado()
        apo = apo.saveApoderadoFromPersona(persona=self.persona, parentesco="Padre")

        self.assertEquals(apo.nombre, self.persona.nombre)

        print("nombrepersona: " + self.persona.nombre)
        print("nombreapoderado: " + apo.nombre)


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

        print("Sexo: " + tipo.descripcion + " Apoderado.Sexo: " + self.apoderado.getSexo)

        self.assertEquals(self.apoderado.getSexo, tipo.descripcion)

    def test_TipoDocumento(self):
        tipodoc = TipoDocumento.objects.create(descripcion="DNI", activo=True)

        self.apoderado.tipo_documento = tipodoc.id_tipo

        self.apoderado.save()

        print("TipoDocumento: " + tipodoc.descripcion + " Apoderado.TipoDoc: " + self.apoderado.getTipoDocumento())

        self.assertEquals(self.apoderado.getTipoDocumento(), tipodoc.descripcion)

    def test_TelefonosPersona(self):
        telef = Telefono(numero="940294196", tipo="Movil")

        telef.save()

        self.apoderado.telefonos.add(telef)

        self.apoderado.save()

        self.assertEquals(str(self.apoderado.telefonos.get(pk=1).numero), telef.numero)


class AlumnoModelTest(TestCase):
    def setUp(self):
        self.alumno = Alumno(nombre="Juan",
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
                             codigoint="123"
                             )
        self.alumno.save()

    def test_alumnoApoderado(self):
        apoderado = Apoderado(nombre="Juan",
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
        apoderado.save()

        self.alumno.apoderados.add(apoderado)
        self.alumno.save()

        self.assertEquals(self.alumno.apoderados.all().count(), 1)

        self.assertEquals(self.alumno.apoderados.get(pk=apoderado.id_apoderado).nombre, apoderado.nombre)

        self.assertEquals(apoderado.alumnos.get(pk=self.alumno.id_alumno).nombre, self.alumno.nombre)
