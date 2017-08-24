from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

from income.views import ControlIngresosPadresView, ControlIngresosPromotorView
from income.views import ControlIngresosPromotorDetallesView


urlpatterns = [

    url(r'^cuentas_cobrar_padres/filter', ControlIngresosPadresView.as_view(), name="cuentas_cobrar_padres/filter"),

    url(r'^cuentas_cobrar_promotor/filter', ControlIngresosPromotorView.as_view(), name="cuentas_cobrar_promotor/filter"),

    url(r'^cuentas_cobrar_promotor_detalle/filter', ControlIngresosPromotorDetallesView.as_view(), name="cuentas_cobrar_promotor_detalle/filter"),
]