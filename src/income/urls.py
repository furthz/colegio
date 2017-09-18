from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

from income.views import ControlIngresosPadresView, ControlIngresosPromotorView, ControlIngresosPromotorDetallesView2
from income.views import ControlIngresosPromotorDetallesView
from income.views import RegistrarPagoListView
from income.views import generar_pdf


urlpatterns = [
    url(r'^register/$', RegistrarPagoListView.as_view(), name="register"),

    url(r'^cuentas_cobrar_padres/filter', ControlIngresosPadresView.as_view(), name="cuentas_cobrar_padres"),

    url(r'^cuentas_cobrar_promotor/filter', ControlIngresosPromotorView.as_view(), name="cuentas_cobrar_promotor"),

    url(r'^cuentas_cobrar_promotor_detalle/filter', ControlIngresosPromotorDetallesView.as_view(), name="cuentas_cobrar_promotor_detalle"),

    url(r'^register/pdf/$', generar_pdf, name="generar_pdf"),

    url(r'^cuentas_cobrar_promotor_detalle2/filter', ControlIngresosPromotorDetallesView2.as_view(), name="cuentas_cobrar_promotor_detalle2"),

]
