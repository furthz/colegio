from django.conf.urls import url
from .views import (
    index,
    # Import de vistas CRUD de Cashier
    CashierListView, CashierDetailView, CashierCreationView, CashierUpdateView, CashierDeleteView,
    # Import de vistas CRUD de BoxCashier
    BoxCashierListView, BoxCashierDetailView, BoxCashierCreationView, BoxCashierUpdateView, BoxCashierDeleteView,
    # Import de vistas CRUD de Consignment
    ConsignmentListView, ConsignmentDetailView, ConsignmentCreationView, ConsignmentUpdateView, ConsignmentDeleteView,
    # Import de vistas de Filtrado
    FiltrarPersonalColegioView
)

urlpatterns = [
    # URL index 'localhost:8000/cash
    url(r'^$', index),

    # URL's del CRUD de CAJA
    url(r'^cashier/$', CashierListView.as_view(), name='cashier_list'),

    #url(r'^cashier/(?P<pk>\d+)$', CashierDetailView.as_view(), name='cashier_detail'),
    url(r'^cashier/(?P<pk>\d+)$', CashierDetailView.as_view(), name='cashier_detail'),

    url(r'^cashier/create$', CashierCreationView.as_view(), name='cashier_create'),
    url(r'^cashier/update/(?P<pk>\d+)$', CashierUpdateView.as_view(), name='cashier_edit'),
    url(r'^cashier/delete/(?P<pk>\d+)$', CashierDeleteView.as_view(), name='cashier_delete'),

    # URL's del CRUD de CAJACAJERO
    url(r'^boxcashier/$', BoxCashierListView.as_view(), name='boxcashier_list'),
    url(r'^boxcashier/(?P<pk>\d+)$', BoxCashierDetailView.as_view(), name='boxcashier_detail'),

    url(r'^boxcashier/Aperturar$', BoxCashierCreationView.as_view(), name='boxcashier_AperturarCaja'),
    url(r'^boxcashier/Cerrar/(?P<pk>\d+)$', BoxCashierUpdateView.as_view(), name='boxcashier_CerrarCaja'),

    url(r'^boxcashier/delete/(?P<pk>\d+)$', BoxCashierDeleteView.as_view(), name='boxcashier_delete'),

    # URL's del CRUD de Remesas
    url(r'^consignment/$', ConsignmentListView.as_view(), name='consignment_list'),
    url(r'^consignment/(?P<pk>\d+)$', ConsignmentDetailView.as_view(), name='consignment_detail'),
    url(r'^consignment/create$', ConsignmentCreationView.as_view(), name='consignment_create'),
    url(r'^consignment/update/(?P<pk>\d+)$', ConsignmentUpdateView.as_view(), name='consignment_edit'),
    url(r'^consignment/delete/(?P<pk>\d+)$', ConsignmentDeleteView.as_view(), name='consignment_delete'),

    # URL'S de Filtrado
    url(r'^filterPC', FiltrarPersonalColegioView.as_view(), name="filtrar_PersonalColegio"),


]

