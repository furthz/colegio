from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

from income.views import ControlIngresosPadresView, ControlIngresosPromotorView, ControlIngresosPromotorDetallesView2
from income.views import ControlIngresosPromotorDetallesView
from income.views import RegistrarPagoListView
from income.views import recibo_A6, boleta_A6, recibo_A5, boleta_A5, FiltrarCuentas


urlpatterns = [
    url(r'^register/filter$', RegistrarPagoListView.as_view(), name="register"),
    url(r'^register/$', FiltrarCuentas.as_view(), name="filtrar_cuentas"),

    url(r'^cuentas_cobrar_padres/filter', ControlIngresosPadresView.as_view(), name="cuentas_cobrar_padres"),

    url(r'^cuentas_cobrar_promotor/filter', ControlIngresosPromotorView.as_view(), name="cuentas_cobrar_promotor"),

    url(r'^cuentas_cobrar_promotor_detalle/filter', ControlIngresosPromotorDetallesView.as_view(), name="cuentas_cobrar_promotor_detalle"),

    url(r'^register/reciboA6/$', recibo_A6, name="recibo_A6"),
    url(r'^register/boletaA6/$', boleta_A6, name="boleta_A6"),
    url(r'^register/reciboA5/$', recibo_A5, name="recibo_A5"),
    url(r'^register/boletaA5/$', boleta_A5, name="boleta_A5"),

    url(r'^cuentas_cobrar_promotor_detalle2/filter', ControlIngresosPromotorDetallesView2.as_view(), name="cuentas_cobrar_promotor_detalle2"),

]
