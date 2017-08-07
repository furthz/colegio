# Create your tests here.

from django.test import TestCase

from datetime import date, datetime

from utils.models import TipoSexo
from utils.models import TipoDocumento

from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model, SESSION_KEY
from .models import Apoderado
from .models import Telefono
from .models import Alumno
from .models import ApoderadoAlumno
from .models import Direccion
from .models import Personal
from .models import Promotor
from .models import Cajero
from .models import Director
from .models import Colegio
from .models import PersonalColegio
from profiles.models import Profile

from django.utils.timezone import now as timezone_now

User = get_user_model()


class PersonaModelTest(TestCase):
    def setUp(self):

        usuario = User.objects.create(password='sha1$6efc0$f93efe9fd7542f25a7be94871ea45aa95de57161',
                                      last_login=date.today(), is_superuser=False,
                                      name='testclient',
                                      is_staff=False, is_active=True,
                                      date_joined=date.today()
                                      )


        print("Usuario: "+ str(usuario.id))

        self.persona = Profile(nombre="Juan",
                               segundo_nombre="Carlos",
                               apellido_ma='Carrasco',
                               apellido_pa="Bermudez",
                               tipo_documento="1",
                               numerodocumento="3344955",
                               sexo="1",
                               correo="sasa",
                               fecha_nac=date.today(),
                               fecha_creacion_persona=date.today(),
                               fecha_modificacion_persona=date.today(),
                               usuario_modificacion_persona="raul",
                               usuario_creacion_persona="raul",
                                user=usuario
                               )
        self.persona.save()



        # self.persona.save()

        self.tipo = TipoDocumento(descripcion="DNI", activo=True)
        self.tipo.save()

        print("idpersonainicio: " + str(self.persona.id_profile))

    def test_PersonaAddApoderado(self):
        apo = Apoderado()
        apo = apo.saveApoderadoFromPersona(persona=self.persona, parentesco="Padre")

        self.assertEquals(apo.nombre, self.persona.nombre)

        print("nombrepersona: " + self.persona.nombre)
        print("nombreapoderado: " + apo.nombre)

    def test_addDireccion(self):
        dir1 = Direccion(calle="Los Pinos", dpto="501", distrito="San Isidro", numero="306")
        dir1.save()

        self.persona.direcciones.add(dir1)

        self.persona.save()

        self.assertEquals(self.persona.direcciones.all().count(), 1)

    def test_personal(self):
        self.personal = Personal()

        self.personal = self.personal.savePersonalFromPersona(persona=self.persona, activo_personal=True)
        self.assertEquals(self.personal.nombre, self.personal.persona.nombre)

        promotor = Promotor().savePromotorFromPersonal(personal=self.personal, activo_promotor=True)
        self.assertEquals(promotor.nombre, promotor.persona.nombre)

        cajero = Cajero().saveCajeroFromPersonal(personal=self.personal, activo_cajero=True)
        self.assertEquals(cajero.nombre, cajero.persona.nombre)

        director = Director().saveDirectorFromPersonal(personal=self.personal, activo_director=True)
        self.assertEquals(director.nombre, director.persona.nombre)




        # print("URL: " + self.personal.get_url_path())


class ApoderadoModelTest(TestCase):
    def setUp(self):
        self.apoderado = Apoderado(nombre="Juan",
                                   segundo_nombre="Carlos",
                                   apellido_ma='Carrasco',
                                   apellido_pa="Bermudez",
                                   tipo_documento="1",
                                   numerodocumento="3344955",
                                   sexo="1",
                                   correo="sas",
                                   fecha_nac=date.today(),
                                   fecha_creacion_apoderado=date.today(),
                                   fecha_modificacion_apoderado=date.today(),
                                   usuario_modificacion_apoderado="raul",
                                   usuario_creacion_apoderado="raul",
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

        print(str("Apoderado.Sexo: %s" % self.apoderado.getSexo))

        self.assertEquals(self.apoderado.getSexo, tipo.descripcion)

    def test_TipoDocumento(self):
        tipodoc = TipoDocumento.objects.create(descripcion="DNI", activo=True)

        self.apoderado.tipo_documento = tipodoc.id_tipo

        self.apoderado.save()

        print("TipoDocumento: " + tipodoc.descripcion + " Apoderado.TipoDoc: " + self.apoderado.getTipoDocumento)

        self.assertEquals(self.apoderado.getTipoDocumento, tipodoc.descripcion)

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
                             tipo_documento="1",
                             numerodocumento="3344955",
                             sexo="1",
                             correo="sas",
                             fecha_nac=date.today(),
                             fecha_creacion_alumno=date.today(),
                             fecha_modificacion_alumno=date.today(),
                             usuario_modificacion_alumno="raul",
                             usuario_creacion_alumno="raul",
                             codigoint="123"
                             )
        self.alumno.save()

    def test_alumnoApoderado(self):
        apoderado = Apoderado(nombre="Juan",
                              segundo_nombre="Carlos",
                              apellido_ma='Carrasco',
                              apellido_pa="Bermudez",
                              tipo_documento="1",
                              numerodocumento="3344955",
                              sexo="1",
                              correo="sas",
                              fecha_nac=date.today(),
                              fecha_creacion_apoderado=date.today(),
                              fecha_modificacion_apoderado=date.today(),
                              usuario_modificacion_apoderado="raul",
                              usuario_creacion_apoderado="raul",
                              parentesco="Padre"
                              )

        apoderado.save()

        apoalum = ApoderadoAlumno(apoderado=apoderado, alumno=self.alumno, activo=True, fecha_creacion=timezone_now())
        apoalum.save()

        apos = ApoderadoAlumno.objects.get(apoderado=apoderado)

        self.assertEquals(self.alumno.apoderados.all().count(), 1)

        self.assertEquals(self.alumno.apoderados.get(pk=apoderado.id_apoderado).nombre, apoderado.nombre)

        self.assertEquals(apoderado.alumnos.get(pk=self.alumno.id_alumno).nombre, self.alumno.nombre)



        # self.assertEquals(self.alumno.apoderadoalumno_set.get(alumno_id=apoalum.alumno_id).fecha_creacion, timezone_now())


class ColegioModelTest(TestCase):
    def setUp(self):
        self.colegio = Colegio(nombre="Juan Bautista", ruc="11223344", ugel="dos", activo=True)
        self.colegio.save()

    def test_colegio(self):
        self.assertEquals(self.colegio.nombre, "Juan Bautista")

    def test_colegioTelefono(self):
        tel = Telefono(numero="112233", tipo="celular")
        tel.save()

        self.colegio.telefonos.add(tel)
        self.colegio.save()

        self.assertEquals(self.colegio.telefonos.count(), 1)

    def test_colegioDireccion(self):
        dire = Direccion(distrito="San Isidro", numero="306", calle="Los Pinos")
        dire.save()

        self.colegio.direcciones.add(dire)
        self.colegio.save()

        self.assertEquals(self.colegio.direcciones.count(), 1)

    def test_colegioAddPersonal(self):
        pers = Personal(nombre="Juan",
                        segundo_nombre="Carlos",
                        apellido_ma='Carrasco',
                        apellido_pa="Bermudez",
                        tipo_documento="1",
                        numerodocumento="3344955",
                        sexo="1",
                        correo="sas",
                        fecha_nac=date.today(),
                        fecha_creacion_persona=date.today(),
                        fecha_modificacion_persona=date.today(),
                        usuario_modificacion_persona="raul",
                        usuario_creacion_persona="raul"
                        )
        pers.save()

        persocole = PersonalColegio(personal=pers, colegio=self.colegio, activo=True)
        persocole.save()

        self.assertEquals(self.colegio.personales.count(), 1)
