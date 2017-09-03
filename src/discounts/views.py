from datetime import date
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from utils.views import MyLoginRequiredMixin
from discounts.models import Descuento
from discounts.models import TipoDescuento
from enrollment.models import Matricula
from enrollment.models import Servicio
from register.models import Colegio
from register.models import PersonalColegio
from discounts.forms import SolicitarDescuentoForm
from discounts.forms import TipoDescuentForm
import logging

# Create your views here.

logger = logging.getLogger("project")

# logger.info(dato) para mostrar los reportes de eventos
# logger.debug("usuario logueado: " + str(request.user.is_authenticated()))
# logger.debug("colegio: " + str(request.session.get('colegio')))
#################################################
#       Solicitar Descuentos
#################################################

class SolicitarDescuentoView(MyLoginRequiredMixin,TemplateView):
    model = Descuento
    template_name = "solicitar_descuento.html"
    form_class = SolicitarDescuentoForm

    def post(self, request, *args, **kwargs):
        form = SolicitarDescuentoForm(initial={'matricula':Matricula.objects.get(pk=request.POST['matricula'])})
        return render(request, template_name=self.template_name, context={
            'form': form,
        })

class CrearSolicitudView(MyLoginRequiredMixin,TemplateView):
    model = Descuento
    form_class = SolicitarDescuentoForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        logger.info(form)

        data_form = form.cleaned_data
        logger.info(data_form)
        solicitud = Descuento(
            personal_colegio=PersonalColegio.objects.get(personal__user=request.user),
            estado=1,
            fecha_solicitud=date.today(),
            matricula=data_form['matricula'],
            comentario=data_form['comentario'],
            tipo_descuento=data_form['tipo_descuento'],
            numero_expediente=data_form['numero_expediente'],
            fecha_aprobacion=date.today()
        )
        solicitud.save()

        return HttpResponseRedirect(reverse('enrollments:matricula_list'))

class TipoDescuentoCreateView(MyLoginRequiredMixin,CreateView):
    model = TipoDescuento
    template_name = "tipo_descuento.html"
    form_class = TipoDescuentForm
    #success_url = reverse('enrollments:matricula_list')
    def get_success_url(self):
        return reverse_lazy('enrollments:matricula_list')

    def form_valid(self, form):
        form.instance.colegio = Colegio.objects.get(pk = self.request.session.get('colegio'))
        return super(TipoDescuentoCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'servicio':Servicio.objects.filter(tipo_servicio__colegio__id_colegio=self.request.session.get('colegio'), activo=True)})
        return render(request, template_name=self.template_name, context={
            'form': form,
        })
#################################################
#       Aprobar Descuentos
#################################################
