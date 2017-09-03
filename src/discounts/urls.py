from django.conf.urls import url
from discounts.views import SolicitarDescuentoView
from discounts.views import CrearSolicitudView
from discounts.views import AprobarDescuentoView

urlpatterns = [
    # URL para tipos de servicios
    url(r'^solicitar/$', SolicitarDescuentoView.as_view(), name="solicitar_descuento"),
    url(r'^solicitar/create$', CrearSolicitudView.as_view(), name="crear_solicitud"),
    url(r'^aprobar/$', AprobarDescuentoView.as_view(), name="aprobar_solicitud"),
]