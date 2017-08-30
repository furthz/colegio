from django.conf.urls import url
from .views import (
    # Import de vistas CRUD de TipoPago
    TipoPagoListView, TipoPagoDetailView, TipoPagoCreationView, TipoPagoUpdateView, TipoPagoDeleteView,

)
from payments.views import RegistrarPagoCreateView

urlpatterns = [
    # URL's del CRUD de TipoPago
    url(r'^tipo_pago/$', TipoPagoListView.as_view(), name='tipopago_list'),
    url(r'^tipo_pago/(?P<pk>\d+)$', TipoPagoDetailView.as_view(), name='tipopago_detail'),
    url(r'^tipo_pago/create$', TipoPagoCreationView.as_view(), name='tipopago_create'),
    url(r'^tipo_pago/update/(?P<pk>\d+)$', TipoPagoUpdateView.as_view(), name='tipopago_edit'),
    url(r'^tipo_pago/delete/(?P<pk>\d+)$', TipoPagoDeleteView.as_view(), name='tipopago_delete'),
    url(r'^register/create/$', RegistrarPagoCreateView.as_view(), name='registrarpago_create'),

]

