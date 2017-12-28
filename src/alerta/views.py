from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from .models import *
from .forms import *


class AlertaListView(ListView):
    model = Alerta
    template_name = 'alertas/cashier_list.html'


class AlertaCreationView(CreateView):
    model = Alerta
    form_class = AlertaForm
    template_name = 'alertas/cashier_form.html'
    success_url = reverse_lazy('alerta:cashier_list')
