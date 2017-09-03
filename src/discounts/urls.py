from django.conf.urls import url
from discounts.views import SolicitarDescuentoView
from discounts.views import CrearSolicitudView

urlpatterns = [
    # URL para tipos de servicios
    url(r'^Solicitar/$', SolicitarDescuentoView.as_view(), name="solicitar_descuento"),
    url(r'^Solicitar/create$', CrearSolicitudView.as_view(), name="crear_solicitud"),
]