
import datetime

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic import TemplateView

from AE_academico.forms import AulaForm, MarcarAsistenciaForm, SubirNotasForm
from AE_academico.forms import CursoDocenteForm
from AE_academico.models import Aula, Asistencia, Notas, AulaCurso
from AE_academico.models import CursoDocente
from AE_academico.models import Curso
from enrollment.models import Matricula
from register.models import Docente, Personal, PersonalColegio, Alumno
from django.conf import settings
from utils.middleware import validar_roles, get_current_request, get_current_colegio, get_current_user
from django.http import HttpResponseRedirect
from utils.views import MyLoginRequiredMixin
import logging
logger = logging.getLogger("project")

#################################################
#####            CRUD DE AULA               #####
#################################################


class AulaListView(MyLoginRequiredMixin, ListView):
    model = Aula
    template_name = 'aula_list.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']
        if validar_roles(roles=roles):
            return super(AulaListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):

            context = super(AulaListView, self).get_context_data(**kwargs)

            request = get_current_request()

            if request.session.get('colegio'):
                id = request.session.get('colegio')
                context['idcolegio'] = id
            return context


class AulaDetailView(UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aula_detail.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']
        if validar_roles(roles=roles):
            return super(AulaDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class AulaCreationView(CreateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            return super(AulaCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_form.html'


class AulaDeleteView(DeleteView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(AulaDeleteView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


#################################################
#####            CRUD DE CURSO DOCENTE      #####
#################################################

class CursoDocenteCreateView(CreateView):
    model = CursoDocente
    form_class = CursoDocenteForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'cursodocente_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            personalcolegio = PersonalColegio.objects.filter(colegio_id=get_current_colegio(), activo=True)
            personal = []
            for personalcol in personalcolegio:
                personal.append(personalcol.personal)
            cursos = AulaCurso.objects.filter(aula__tipo_servicio__colegio_id=get_current_colegio(), activo= True)
            docentes = Docente.objects.filter(empleado=personal)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'docentes': docentes,
                'cursos': cursos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

#################################################
#####            CRUD DE  AULA CURSO    #####
#################################################

class AulaCursoCreateView(TemplateView):
    model = AulaCurso
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'cursodocente_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            aula_actual = Aula.objects.get(id_aula= request.GET['aula'])
            cursos = Curso.objects.filter(aula__tipo_servicio__colegio_id=get_current_colegio(), activo=True)
            return render(request, template_name=self.template_name, context={
                'aula': aula_actual,
                'cursos': cursos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        return HttpResponseRedirect(reverse('AE_academico:aula_list'))

#################################################
#####            ASISTENCIA ALUMNOS         #####
#################################################

class MarcarAsistenciaView(CreateView):

    model = Asistencia
    template_name = 'marcar_asistencia.html'
    form_class = MarcarAsistenciaForm
    success_url = reverse_lazy('academic:aula_list')

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            # AQUI VA EL ID DE TIPO DE SERVICIO
            id_tipo_servicio = 4
            id_colegio = get_current_colegio()
            matriculadosaula = Matricula.objects.filter(colegio_id=id_colegio, activo=True, tipo_servicio=id_tipo_servicio)
            logger.info("Datos son {0}".format(matriculadosaula))

            alumnos = []
            for matriculado in matriculadosaula:
                alumnos.append(matriculado.alumno)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'alumnos': alumnos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        logger.info("Estoy en el POST")
        logger.info("Los datos de llegada son {0}".format(request.POST))
        data_post = request.POST

        ids = data_post['id']
        logger.info(ids)
        estados = data_post['estado_asistencia']
        logger.info(estados)


        #id_colegio = get_current_colegio()


        contexto = {}
        return render(request, template_name=self.template_name, context=contexto)

"""
class ResumenAsistenciaView(FormView):

    model = Asistencia
    template_name = "control_ingresos_promotor_detalle.html"
    #form_class = CuentasCobrarPromotorDetalleForm

    def cargarformPromotordetalle(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos los meses
            meses_todos = ["Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                           "Setiembre", "Octubre", "Noviembre", "Diciembre"]
            num_mes = datetime.today().month
            meses = []
            for i in range(0, num_mes + 1):
                meses.append(meses_todos[i])

            # Cargamos los estados
            estados = ["Todos", "Pagado", "No pagado"]

            return {'meses': meses_todos, 'estados': estados}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context


    def get(self, request, *args, **kwargs):
        super(ResumenAsistenciaView, self).get(request, *args, **kwargs)

        contexto = self.cargarformPromotordetalle(request)

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context


    def post(self, request, *args, **kwargs):

        alumno = request.POST["alumno"]
        anio = request.POST["anio"]
        mes = request.POST["mes"]
        estado = request.POST["estado"]

        logger.info(alumno)
        colegio = get_current_colegio()

        # Proceso de filtrado según el colegio
        cuentas_cobrar_colegio = self.model.objetos.filter(matricula__colegio__id_colegio=colegio, activo=True)

        # Proceso de filtrado según el alumno
        if alumno == "":
            por_cobrar1 = cuentas_cobrar_colegio
        else:
            por_cobrar1 = cuentas_cobrar_colegio.filter(Q(matricula__alumno__nombre=alumno) | Q(matricula__alumno__apellido_pa=alumno) | Q(matricula__alumno__apellido_ma=alumno))

        # Proceso de filtrado según el año
        if anio == "Todos":
            por_cobrar2 = por_cobrar1
        else:
            anio = int(anio)
            por_cobrar2 = por_cobrar1.filter(fecha_ven__year=anio)

        # Proceso de filtrado según el mes
        if mes == "Todos":
            por_cobrar3 = por_cobrar2
        else:
            num_mes = obtener_mes(mes)
            por_cobrar3 = por_cobrar2.filter(fecha_ven__month=num_mes)

        # Proceso de filtrado según el estado o tipo
        if estado == "Todos":
            por_cobrar = por_cobrar3
        elif estado == "Pagado":
            por_cobrar = por_cobrar3.filter(estado=False)
        elif estado == "No_pagado":
            por_cobrar = por_cobrar3.filter(estado=True)

        contexto = self.cargarformPromotordetalle(request)

        if len(por_cobrar) != 0:
            contexto['object_list'] = por_cobrar
            contexto['form'] = ResumenAsistenciaView
            return render(request, template_name=self.template_name, context=contexto)
        else:
            contexto['object_list'] = []
            contexto['form'] = ResumenAsistenciaView
            return render(request, template_name=self.template_name, context=contexto)
"""

class SubirNotasView(CreateView):

    model = Notas
    template_name = 'subir_notas.html'
    form_class = SubirNotasForm
    success_url = reverse_lazy('academic:aula_list')

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            # AQUI VA EL ID DE TIPO DE SERVICIO
            id_tipo_servicio = 4
            id_colegio = get_current_colegio()
            matriculadosaula = Matricula.objects.filter(colegio_id=id_colegio, activo=True, tipo_servicio=id_tipo_servicio)
            logger.info("Datos son {0}".format(matriculadosaula))



            alumnos = []
            for matriculado in matriculadosaula:
                alumnos.append(matriculado.alumno)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'alumnos': alumnos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        logger.info("Estoy en el POST")
        data_post = request.POST
        logger.info("Los datos de llegada son {0}".format(data_post))





        #id_colegio = get_current_colegio()


        contexto = {}
        return render(request, template_name=self.template_name, context=contexto)
