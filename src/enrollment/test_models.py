from django.test import TestCase
from datetime import date
# Create your tests here.
from enrollment.models import TipoServicio
from enrollment.models import Sucursal
from enrollment.models import Servicio

class TipoServicioModelTest(TestCase):


    def setUp(self):
        self.colegio_test1 = Sucursal(nombre ='Trilce',
                                      ruc = '123456789',
                                      ugel = '6',
                                      fecha_creacion = date.today(),
                                      fecha_modificacion = date.today(),
                                      usuario_creacion = 'Paul',
                                      usuario_modificacion = 'Paul'
                                      )
        self.colegio_test2 = Sucursal(nombre='Pamer',
                                      ruc='987654321',
                                      ugel='6',
                                      fecha_creacion=date.today(),
                                      fecha_modificacion=date.today(),
                                      usuario_creacion='Paul',
                                      usuario_modificacion='Paul'
                                      )
        self.colegio_test1.save()
        self.colegio_test2.save()
        print(self.colegio_test1)
        print(self.colegio_test1)
        self.tiposervicio_test1 = TipoServicio(is_ordinario = True,
                                               nivel = 1,
                                               grado = 2,
                                               fecha_creacion=date.today(),
                                               fecha_modificacion=date.today(),
                                               usuario_creacion='Paul',
                                               usuario_modificacion='Paul',
                                               extra = None,
                                               codigo_modular = '1234',
                                               colegio=self.colegio_test1
                                               )
        self.tiposervicio_test2 = TipoServicio(is_ordinario=True,
                                               nivel=1,
                                               grado=3,
                                               fecha_creacion=date.today(),
                                               fecha_modificacion=date.today(),
                                               usuario_creacion='Paul',
                                               usuario_modificacion='Paul',
                                               extra=None,
                                               codigo_modular='9876',
                                               colegio=self.colegio_test2
                                               )
        self.tiposervicio_test1.save()
        self.tiposervicio_test2.save()
        print(self.tiposervicio_test1.full_detail)
        print(self.tiposervicio_test2.full_detail)
        self.servicio_test1 = Servicio(tipo_servicio= self.tiposervicio_test1,
                                       nombre="Matricula",
                                       precio=150,
                                       is_periodic=False,
                                       fecha_facturar=date.today(),
                                       cuotas=1,
                                       fecha_creacion=date.today(),
                                       fecha_modificacion=date.today()
                                       )
        self.servicio_test2 = Servicio(tipo_servicio=self.tiposervicio_test1,
                                       nombre="Pension",
                                       precio=200,
                                       is_periodic=True,
                                       fecha_facturar=date.today(),
                                       cuotas=10,
                                       fecha_creacion=date.today(),
                                       fecha_modificacion=date.today()
                                       )
        self.servicio_test3 = Servicio(tipo_servicio=self.tiposervicio_test2,
                                       nombre="Matricula",
                                       precio=550,
                                       is_periodic=False,
                                       fecha_facturar=date.today(),
                                       cuotas=1,
                                       fecha_creacion=date.today(),
                                       fecha_modificacion=date.today()
                                       )
        self.servicio_test4 = Servicio(tipo_servicio=self.tiposervicio_test2,
                                       nombre="Pension",
                                       precio=1000,
                                       is_periodic=True,
                                       fecha_facturar=date.today(),
                                       cuotas=10,
                                       fecha_creacion=date.today(),
                                       fecha_modificacion=date.today()
                                       )
        self.servicio_test1.save()
        self.servicio_test2.save()
        self.servicio_test3.save()
        self.servicio_test4.save()
        print(self.servicio_test1.full_detail)
        print(self.servicio_test2.full_detail)
        print(self.servicio_test3.full_detail)
        print(self.servicio_test4.full_detail)



    def test_relacion_padrehijo(self):
        self.assertEquals(self.colegio_test1.id_colegio,self.tiposervicio_test1.colegio.id_colegio)
        self.assertEquals(self.colegio_test2.id_colegio,self.tiposervicio_test2.colegio.id_colegio)
        self.assertNotEquals(self.colegio_test1.id_colegio,self.tiposervicio_test2.colegio.id_colegio)
        self.assertNotEquals(self.colegio_test2.id_colegio, self.tiposervicio_test1.colegio.id_colegio)

