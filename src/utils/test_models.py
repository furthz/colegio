from django.test import TestCase

# Create your tests here.
from .models import TipoDocumento
from .models import TiposMedioPago
from .models import TipoSexo
from .models import TiposGrados
from .models import TiposNivel


class TiposdocumentosModelTest(TestCase):
    def setUp(self):
        # Tiposdocumentos.objects.create(descripcion = 'Carnet', activo= 'True')
        self.carnet = TipoDocumento.objects.create(descripcion='Carnet', activo='True')

    def test_description_label(self):
        print("DESCRIPCION: " + self.carnet.descripcion)
        self.assertEquals(self.carnet.descripcion, 'Carnet')

    def test_activo_label(self):
        print("ACTIVO: " + self.carnet.activo)
        self.assertEquals(self.carnet.activo, 'True')


class TiposMedioPagoModelTest(TestCase):
    def setUp(self):
        self.visa = TiposMedioPago.objects.create(descripcion='Visa', activo='True')
        self.mastercard = TipoDocumento.objects.create(descripcion='MasterCard', activo='True')

    def test_descripcion_label(self):
        self.assertEquals(self.visa.descripcion, 'Visa')
        self.assertEquals(self.mastercard.descripcion, 'MasterCard')


class TipoSexoModelTest(TestCase):
    def setUp(self):
        self.Hombre = TipoSexo.objects.create(descripcion='Hombre', activo='True')

    def test_descpricion(self):
        print("Cantidad de Sexos: " + str(TipoSexo.objects.count()))
        self.assertGreaterEqual(TipoSexo.objects.count(), 1, "")


class TiposGradosModelTest(TestCase):
    def setUp(self):
        #self.g = TiposGrados()
        #self.g.save()

        self.Grado = TiposGrados.objects.create(descripcion='primero', activo='True')
        self.Grado2 = TiposGrados.objects.create(descripcion='segundo', activo='True')

    def test_cantidad(self):
        print("Cantidad de grados: " + str(TiposGrados.objects.count()))
        self.assertGreaterEqual(TiposGrados.objects.count(), 2, "")


class TiposNivelModelTest(TestCase):
    def setUp(self):
        self.primaria = TiposNivel.objects.create(descripcion='Primaria', activo='True')
        self.secundaria = TiposNivel.objects.create(descripcion='Secundaria', activo='True')
        self.inicial = TiposNivel.objects.create(descripcion='Inicial', activo='True')
