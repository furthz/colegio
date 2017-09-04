from django.conf.urls import url
from discounts.views import SolicitarDescuentoView
from discounts.views import CrearSolicitudView
from discounts.views import TipoDescuentoCreateView
from discounts.views import AprobarDescuentoView
from discounts.views import DetalleDescuentoView

urlpatterns = [
    # URL para tipos de servicios
    url(r'^solicitar/$', SolicitarDescuentoView.as_view(), name="solicitar_descuento"),
    url(r'^solicitar/create$', CrearSolicitudView.as_view(), name="crear_solicitud"),
    url(r'^tipodescuento/create$', TipoDescuentoCreateView.as_view(), name="tipo_descuento_create"),
    url(r'^approve/$', AprobarDescuentoView.as_view(), name="aprobar_descuentos"),
    url(r'^detail/$', DetalleDescuentoView.as_view(), name="detalle_descuentos"),
]
