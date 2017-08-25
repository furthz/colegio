from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from .models import Caja, CajaCajero, Remesa
from .forms import CashierForm, BoxCashierForm, ConsignmentForm


def index(request):
    return HttpResponse("Modulo Cash")


#################################################
#####          CRUD DE CAJA                 #####
#################################################

class CashierListView(ListView):
    model = Caja
    template_name = 'cashier/cashier_list.html'


class CashierDetailView(DetailView):
    model = Caja
    template_name = 'cashier/cashier_detail.html'


class CashierCreationView(CreateView):
    model = Caja
    form_class = CashierForm
    success_url = reverse_lazy('cash:cashier_list')
    template_name = 'cashier/cashier_form.html'


class CashierUpdateView(UpdateView):
    model = Caja
    form_class = CashierForm
    success_url = reverse_lazy('cash:cashier_list')
    template_name = 'cashier/cashier_form.html'
    # fields = ['id_remesa', 'id_persona', 'id_movimiento', 'fechacreacion', 'monto', 'comentario']


class CashierDeleteView(DeleteView):
    model = Caja
    success_url = reverse_lazy('cash:cashier_list')
    template_name = 'cashier/cashier_confirm_delete.html'


#################################################
#####          CRUD DE CAJACAJERO           #####
#################################################

class BoxCashierListView(ListView):
    model = CajaCajero
    template_name = 'boxcashier/boxcashier_list.html'


class BoxCashierDetailView(DetailView):
    model = CajaCajero
    template_name = 'boxcashier/boxcashier_detail.html'


class BoxCashierCreationView(CreateView):
    model = CajaCajero
    form_class = BoxCashierForm
    success_url = reverse_lazy('cash:boxcashier_list')
    template_name = 'boxcashier/boxcashier_formApertura.html'


class BoxCashierUpdateView(UpdateView):
    model = CajaCajero
    form_class = BoxCashierForm
    success_url = reverse_lazy('cash:boxcashier_list')
    template_name = 'boxcashier/boxcashier_formCierre.html'
    # fields = ['id_remesa', 'id_persona', 'id_movimiento', 'fechacreacion', 'monto', 'comentario']


class BoxCashierDeleteView(DeleteView):
    model = CajaCajero
    success_url = reverse_lazy('cash:boxcashier_list')
    template_name = 'boxcashier/boxcashier_confirm_delete.html'


#################################################
#####          CRUD DE REMESAS              #####
#################################################

class ConsignmentListView(ListView):
    model = Remesa
    template_name = 'consignment/consignment_list.html'


class ConsignmentDetailView(DetailView):
    model = Remesa
    template_name = 'consignment/consignment_detail.html'


class ConsignmentCreationView(CreateView):
    model = Remesa
    form_class = ConsignmentForm
    success_url = reverse_lazy('cash:consignment_list')
    template_name = 'consignment/consignment_form.html'


class ConsignmentUpdateView(UpdateView):
    model = Remesa
    form_class = ConsignmentForm
    success_url = reverse_lazy('cash:consignment_list')
    template_name = 'consignment/consignment_form.html'
    # fields = ['id_remesa', 'id_persona', 'id_movimiento', 'fechacreacion', 'monto', 'comentario']


class ConsignmentDeleteView(DeleteView):
    model = Remesa
    success_url = reverse_lazy('cash:consignment_list')
    template_name = 'consignment/consignment_confirm_delete.html'

#################################################
#####          FILTRADO                     #####
#################################################


class FiltrarPersonalColegioView(ListView):
    model = Remesa
    template_name = 'consignment/consignment_filterlist.html'
