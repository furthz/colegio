from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Remesa
from .forms import RemesaForm

#RemesaListView
class RemesaListView(ListView):
    model = Remesa
    template_name = 'cash_list.html'


class RemesaDetailView(DetailView):
    model = Remesa


class RemesaCreationView(CreateView):
    model = Remesa
    form_class = RemesaForm
    success_url = reverse_lazy('remesas:list')


class RemesaUpdateView(UpdateView):
    model = Remesa
    success_url = reverse_lazy('remesas:list')
    fields = ['id_remesa', 'id_persona', 'id_movimiento', 'fechacreacion', 'monto', 'comentario']


class RemesaDeleteView(DeleteView):
    model = Remesa
    success_url = reverse_lazy('remesas:list')
