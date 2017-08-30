from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView
)
from .models import TipoPago
from .forms import TipoPagoForm

#################################################
#####          CRUD DE TIPO PAGO            #####
#################################################

class TipoPagoListView(ListView):
    model = TipoPago
    template_name = 'TipoPago/tipopago_list.html'


class TipoPagoDetailView(DetailView):
    template_name = 'TipoPago/tipopago_detail.html'
    model = TipoPago


class TipoPagoCreationView(CreateView):
    model = TipoPago
    form_class = TipoPagoForm
    success_url = reverse_lazy('payments:cashier_list')
    template_name = 'TipoPago/tipopago_form.html'


class TipoPagoUpdateView(UpdateView):
    model = TipoPago
    form_class = TipoPagoForm
    success_url = reverse_lazy('payments:cashier_list')
    template_name = 'TipoPago/tipopago_form.html'


class TipoPagoDeleteView(UpdateView):
    model = TipoPago
    form_class = TipoPagoForm
    success_url = reverse_lazy('payments:cashier_list')
    template_name = 'TipoPago/tipopago_list.html'