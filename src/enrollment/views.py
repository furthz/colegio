from django.shortcuts import render
#from . import forms
from datetime import date
from enrollment.models import Servicio
from enrollment.models import TipoServicio
from enrollment.models import Colegio
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.core.urlresolvers import reverse_lazy
from enrollment.forms import ServicioForm
from enrollment.forms import TipoServicioForm
from django.urls import reverse
import logging
# Create your views here.

logger = logging.getLogger("project")

#logger.info(dato) para mostrar los reportes de eventos

#################################################
#   CRUD (Create, Retrieve, Update, Delete)
#   Tipos de Servicios
#################################################

class TipoServicioList(ListView):
    """

    """
    logger.info("Hola")
    model = TipoServicio
    template_name = "tiposervicio_list.html"

    #def get_context_data(self, **kwargs):
    #    context = super(TipoServicioList, self).get_context_data(**kwargs)
    #    return context

class TipoServicioDetail(DetailView):
    """

    """
    model = TipoServicio
    template_name = "tiposervicio_detail.html"


class TipoServicioCreate(CreateView):
    """

    """
    colegio = Colegio.objects.get(pk=1)
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = "tiposervicio_form.html"
    def form_valid(self, form):
        form.instance.colegio = self.colegio
        form.instance.fecha_creacion = date.today()
        form.instance.fecha_modificacion = date.today()
        return super(TipoServicioCreate, self).form_valid(form)

class TipoServicioUpdate(UpdateView):
    """

    """
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = "tiposervicio_form.html"
    def form_valid(self, form):
        form.instance.fecha_modificacion = date.today()
        return super(TipoServicioUpdate, self).form_valid(form)

class TipoServicioDelete(DeleteView):
    """

    """
    model = TipoServicio
    success_url = reverse_lazy('enrollments:tiposervicio_list')
    template_name = "tiposervicio_confirm_delete.html"

##########################################################
#   CRUD (Create, Retrieve, Update, Delete)
#   Servicios
##########################################################

class ServicioList(ListView):
    """

    """
    model = Servicio
    template_name = "servicio_list.html"
    def get_queryset(self):
        return self.model.objects.filter(tipo_servicio = self.kwargs["pkts"])
    #def get_context_data(self, **kwargs):
    #    context = super(ServicioList, self).get_context_data(**kwargs)
    #    return context

class ServicioDetail(DetailView):
    """

    """
    model = Servicio
    template_name = "servicio_detail.html"

class ServicioCreate(CreateView):
    """

    """
    tiposervicio = TipoServicio
    model = Servicio
    form_class = ServicioForm
    template_name = "servicio_form.html"
    def form_valid(self, form):
        form.instance.tipo_servicio = self.tiposervicio.objects.get(pk=self.kwargs["pkts"])
        form.instance.fecha_creacion = date.today()
        form.instance.fecha_modificacion = date.today()
        return super(ServicioCreate, self).form_valid(form)

class ServicioUpdate(UpdateView):
    """

    """
    model = Servicio
    form_class = ServicioForm
    template_name = "servicio_form.html"

    def form_valid(self, form):
        form.instance.fecha_modificacion = date.today()
        return super(ServicioUpdate, self).form_valid(form)

class ServicioDelete(DeleteView):
    """

    """
    model = Servicio
    template_name = "servicio_confirm_delete.html"
    def get_success_url(self):
        tiposervicio = self.object.tipo_servicio
        return reverse_lazy('enrollments:servicio_list', kwargs={'pkts': tiposervicio.id_tipo_servicio})
        #return "/servicios/impdates/list/{id_tipo_servicio}/listservicios"
