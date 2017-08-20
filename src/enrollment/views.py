from django.shortcuts import render
# from . import forms
from datetime import date
from enrollment.models import Servicio
from enrollment.models import TipoServicio
from enrollment.models import Matricula
from enrollment.models import Cuentascobrar
from register.models import Colegio
from profiles.models import Profile
from register.models import Alumno
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
from enrollment.forms import ServicioForm
from enrollment.forms import TipoServicioForm
from enrollment.forms import MatriculaForm
from django.urls import reverse
from utils.models import TiposNivel
from utils.models import TiposGrados
from utils.views import MyLoginRequiredMixin
import logging

# Create your views here.

logger = logging.getLogger("project")

# logger.info(dato) para mostrar los reportes de eventos
# logger.debug("usuario logueado: " + str(request.user.is_authenticated()))
# logger.debug("colegio: " + str(request.session.get('colegio')))
#################################################
#   CRUD (Create, Retrieve, Update, Delete)
#   Tipos de Servicios
#################################################

class TipoServicioListView(MyLoginRequiredMixin, ListView):
    """

    """
    logger.info("Hola")
    model = TipoServicio
    template_name = "tiposervicio_list.html"

    # def get_context_data(self, **kwargs):
    #    context = super(TipoServicioList, self).get_context_data(**kwargs)
    #    return context


class TipoServicioDetailView(MyLoginRequiredMixin, DetailView):
    """

    """
    model = TipoServicio
    template_name = "tiposervicio_detail.html"


class TipoServicioCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = "tiposervicio_form.html"

    def form_valid(self, form):
        form.instance.colegio = Colegio.objects.get(pk=self.request.session.get('colegio'))
        return super(TipoServicioCreateView, self).form_valid(form)

        # def get_context_data(self, **kwargs):
        #    context = super(TipoServicioCreate, self).get_context_data(**kwargs)
        #    context['nivel'] = Colegio.objects.all()
        #    return context


class TipoServicioUpdateView(MyLoginRequiredMixin, UpdateView):
    """

    """
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = "tiposervicio_form.html"


class TipoServicioDeleteView(MyLoginRequiredMixin, DeleteView):
    """

    """
    model = TipoServicio
    success_url = reverse_lazy('enrollments:tiposervicio_list')
    template_name = "tiposervicio_confirm_delete.html"


##########################################################
#   CRUD (Create, Retrieve, Update, Delete)
#   Servicios
##########################################################

class ServicioListView(MyLoginRequiredMixin, ListView):
    """

    """
    model = Servicio
    template_name = "servicio_list.html"

    def get_queryset(self):
        return self.model.objects.filter(tipo_servicio=self.kwargs["pkts"])
        # def get_context_data(self, **kwargs):
        #    context = super(ServicioList, self).get_context_data(**kwargs)
        #    return context


class ServicioDetailView(MyLoginRequiredMixin, DetailView):
    """

    """
    model = Servicio
    template_name = "servicio_detail.html"



class ServicioCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    tiposervicio = TipoServicio
    model = Servicio
    form_class = ServicioForm
    template_name = "servicio_form.html"

    def form_valid(self, form):
        form.instance.tipo_servicio = self.tiposervicio.objects.get(pk=self.kwargs["pkts"])
        return super(ServicioCreateView, self).form_valid(form)


class ServicioUpdateView(MyLoginRequiredMixin, UpdateView):
    """

    """
    model = Servicio
    form_class = ServicioForm
    template_name = "servicio_form.html"

    def form_valid(self, form):
        form.instance.fecha_modificacion = date.today()
        return super(ServicioUpdateView, self).form_valid(form)


class ServicioDeleteView(MyLoginRequiredMixin, DeleteView):
    """

    """
    model = Servicio
    template_name = "servicio_confirm_delete.html"

    def get_success_url(self):
        tiposervicio = self.object.tipo_servicio
        return reverse_lazy('enrollments:servicio_list', kwargs={'pkts': tiposervicio.id_tipo_servicio})
        # return "/servicios/impdates/list/{id_tipo_servicio}/listservicios"


#################################################
#
#
#################################################

class MatriculaListView(MyLoginRequiredMixin, ListView):
    """

    """
    model = Matricula
    template_name = "matricula_list.html"
    # def get_queryset(self):
    #    return self.model.objects.filter(tipo_servicio = self.kwargs["pkts"])
    #def get_context_data(self,request, **kwargs):
    #    context = super(ServicioList, self).get_context_data(**kwargs)
    #    return context


class MatriculaDetailView(MyLoginRequiredMixin, DetailView):
    """

    """
    model = Matricula
    template_name = "matricula_detail.html"


class MatriculaCreateView(MyLoginRequiredMixin, CreateView):
    """

    """
    model = Matricula
    form_class = MatriculaForm
    template_name = "matricula_form.html"

    def form_valid(self, form):
        logger.info("Se ejecuto")
        form.instance.colegio = Colegio.objects.get(pk=self.request.session.get('colegio'))
        return super(MatriculaCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        return render(request,template_name=self.template_name,context={
            'alumno':Alumno.objects.get(pk=request.GET["alumno"]),
            'form': self.form_class,
        })


    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        logger.debug("POST")

        form = self.form_class(request.POST)
        logger.debug("leer datos request post")

        if form.is_valid():
            logger.debug("Formulario valido")

            data_form = form.cleaned_data
            logger.debug("form en dict")
            logger.debug(data_form)

            matricula = Matricula(alumno=data_form["alumno"],
                                  colegio_id=self.request.session.get('colegio'),
                                  tipo_servicio=data_form["tipo_servicio"]
                                  )
            matricula.save()
            logger.debug(matricula)
            logger.info(matricula)

            estado = self.CrearCuentasCobrar(data_form, matricula)
            logger.debug("se creo la cuantas {0}".format(estado))

            return HttpResponseRedirect(matricula.get_absolute_url())

        return HttpResponseRedirect(reverse('enrollments:matricula_create'))

    def CrearCuentasCobrar(self, data_form, matricula):
        """
        Este metodo permite generar las Cuantas por Cobrar producto de una matricula
        :param data_form: datos del formulario de matricula como diccionario
        :param matricula: objeto matricula que tiene la relacion de Alumno, Colegio, Tipo de Servicio
        :return: retorna un mensaje de exito al concluir el metodo
        """
        logger.debug("Inicio de metodo CrearCuantasCobrar")
        logger.info("Inicio de metodo CrearCuantasCobrar")

        list_servicios = Servicio.objects.filter(tipo_servicio_id=data_form["tipo_servicio"])
        logger.debug(list_servicios.all())
        logger.info(list_servicios.all())

        fecha_actual = date.today()

        for servicio in list_servicios:
            logger.debug("inicia la lecturas de las cuentas")
            logger.info(servicio)

            fecha_facturar = servicio.fecha_facturar
            if fecha_facturar.month < fecha_actual.month:
                fecha_facturar = fecha_facturar.replace(month= fecha_actual.month)
            logger.info("la fecha a facturar es: {0}".format(fecha_facturar))

            if servicio.is_periodic:
                logger.debug(str(servicio.is_periodic))
                logger.info("El servicio es periodico {0}".format(servicio.is_periodic))

                if servicio.fecha_facturar.month < fecha_actual.month:
                    numero_cuotas = servicio.cuotas - (fecha_actual.month - servicio.fecha_facturar.month)
                else:
                    numero_cuotas = servicio.cuotas

                for cuota in range(numero_cuotas):
                    logger.info("El servicio tiene {0} cuotas".format(servicio.cuotas))
                    logger.info("El servicio cobrara {0} cuotas".format(numero_cuotas))
                    logger.debug("Cuota Nro. {0}".format(cuota))

                    if (fecha_facturar.month + cuota) < 13:
                        fecha_vencimiento = fecha_facturar.replace(month=fecha_facturar.month + cuota)
                        cuentas = Cuentascobrar(matricula=matricula,
                                                servicio=servicio,
                                                fecha_ven=fecha_vencimiento,
                                                estado=True,
                                                precio=servicio.precio,
                                                deuda=servicio.precio
                                                )
                        logger.debug(cuentas.matricula)
                        logger.info(cuentas.matricula)

                        cuentas.save()

            else:
                logger.debug(str(servicio.is_periodic))
                logger.info("El servicio es periodico {0}".format(servicio.is_periodic))

                cuentas = Cuentascobrar(matricula=matricula,
                                        servicio=servicio,
                                        fecha_ven=servicio.fecha_facturar,
                                        estado=True,
                                        precio=servicio.precio,
                                        deuda=servicio.precio
                                        )
                cuentas.save()

        return "Exito"

class MatriculaUpdateView(MyLoginRequiredMixin, UpdateView):
    """

    """
    model = Matricula
    form_class = MatriculaForm
    template_name = "matricula_form.html"

    def form_valid(self, form):
        form.instance.fecha_modificacion = date.today()
        return super(MatriculaUpdateView, self).form_valid(form)

class CargarMatriculaUpdateView(MyLoginRequiredMixin, TemplateView):
    template_name = "matricula_form.html"
    model = Matricula
    form_class = MatriculaForm

    def post(self, request, *args, **kwargs):

        matricula = self.model.objects.get(pk=request.POST["matricula"])
        form = self.form_class(instance=matricula)
        return render(request, template_name=self.template_name, context={
            'form': form,
            'alumno':matricula.alumno,
        })

class MatriculaDeleteView(MyLoginRequiredMixin, DeleteView):
    """

    """
    model = Matricula
    template_name = "matricula_confirm_delete.html"

    def get_success_url(self):
        # tiposervicio = self.object.tipo_servicio
        return reverse_lazy('enrollments:matricula_list')

class FiltrarAlumnoView(ListView):
    """
    Este View permite filtrar a los alumnos por nombre y/o apellido
    """
    model = Alumno
    template_name = "alumno_form.html"

    def post(self, request, *args, **kwargs):


        object_list_alumnos1 =  self.model.objects.filter(nombre=request.POST["nombre"])
        object_list_alumnos2 = self.model.objects.filter(apellido_pa=request.POST["apellido_pa"])
        object_list_alumnos3 = self.model.objects.filter(nombre=request.POST["nombre"],apellido_pa=request.POST["apellido_pa"])

        if len(object_list_alumnos3) is not 0:
            return render(request, template_name=self.template_name, context={
                'object_list': object_list_alumnos3,
            })
        elif len(object_list_alumnos1) is not 0:
            return render(request, template_name=self.template_name, context={
                'object_list': object_list_alumnos1,
            })
        elif len(object_list_alumnos2) is not 0:
            return render(request, template_name=self.template_name, context={
                'object_list': object_list_alumnos2,
            })
        else:
            return render(request, template_name=self.template_name, context={
                'object_list': [],
            })

class CargarMatriculaCreateView(TemplateView):
    template_name = "matricula_form.html"
    model = Alumno
    form_class = MatriculaForm
    def post(self, request, *args, **kwargs):

        return render(request, template_name=self.template_name, context={
                'alumno': self.model.objects.get(pk = request.POST["alumno"]),
                'form': self.form_class,
            })

#######################################################################
#
#
#######################################################################


from django.http import JsonResponse
from django.views.generic.edit import CreateView

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class AuthorCreate(AjaxableResponseMixin, CreateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = "tiposervicio_form.html"


















class testform(ListView):
    model = Alumno
    template_name = "persona_form.html"

    def post(self, request, *args, **kwargs):
        logger.info("entre en el GET testform")
        return render(request,template_name=self.template_name,context={
            'gato': "Gato Rojo",
            'hola':"Gato Negro",
        })


    # def get_queryset(self):
    #    return self.model.objects.filter(tipo_servicio = self.kwargs["pkts"])
    # def get_context_data(self,request, **kwargs):
    #    context = super(ServicioList, self).get_context_data(**kwargs)
    #    return context

class testpersonaform(View):

    template_name = "ProyectoMundoPixel/CrearServicio.html"

    def get(self, request, *args, **kwargs):
        logger.info("Llegue aqui GET {0}".format(request.GET["gato"]))
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        logger.info("LLegue al POST {0}".format(request.POST["gato"]))
        return HttpResponseRedirect("/success/")

