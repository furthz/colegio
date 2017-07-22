import pytest
from django.test import TestCase

# Create your tests here.
from .models import Tiposdocumentos

class TiposdocumentosModelTest(TestCase):


    def setUp(self):
        #Tiposdocumentos.objects.create(descripcion = 'Carnet', activo= 'True')
        self.carnet = Tiposdocumentos.objects.create(descripcion='Carnet', activo='True')

    def test_description_label(self):
        print ("DESCRIPCION: " + self.carnet.descripcion)
        self.assertEquals(self.carnet.descripcion, 'Carnet')

    def test_activo_label(self):
        print("ACTIVO: " + self.carnet.activo)
        self.assertEquals(self.carnet.activo, "True")


