import datetime
import json
import calendar

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic import TemplateView

from AE_academico.forms import AulaForm, MarcarAsistenciaForm, SubirNotasForm, CursoForm, EventoForm, PeriodoAcademicoForm, \
    HorarioAulaForm, RegistrarNotas2Form
from AE_academico.forms import CursoDocenteForm
from AE_academico.models import Aula, Asistencia, Notas, AulaCurso, Evento, HorarioAula, AulaMatricula, PeriodoAcademico
from AE_academico.models import CursoDocente
from AE_academico.models import Curso
from enrollment.models import Matricula
from income.models import obtener_mes
from register.models import Docente, Personal, PersonalColegio, Alumno, Colegio
from django.conf import settings
from utils.middleware import validar_roles, get_current_request, get_current_colegio, get_current_user
from django.http import HttpResponseRedirect
from utils.views import MyLoginRequiredMixin
import logging
logger = logging.getLogger("project")


#####################################################
#####              CRUD DE AULA                 #####
#####################################################

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
            aula_id = request.GET["aula"]
            id_colegio = get_current_colegio()
            matriculadosaula = Matricula.objects.filter(colegio_id=id_colegio, activo=True,
                                                        tipo_servicio=1).order_by('alumno__apellido_pa')
            aula = Aula.objects.get(id_aula=aula_id)
            matriculadosaula = AulaMatricula.objects.filter(aula=aula, activo=True).order_by('matricula__alumno__apellido_pa')
            lista_matriculados = []
            cursos = AulaCurso.objects.filter(aula=aula,
                                              activo=True)
            for matricula in matriculadosaula:
                lista_matriculados.append(matricula.matricula)
            cursos_docentes = []
            for curso in cursos:
                try:
                    cursos_docentes.append(CursoDocente.objects.get(curso=curso, activo=True))
                except:
                    logger.info("No hay docente aun")
            return render(request, template_name=self.template_name, context={
                'matriculados_aula': lista_matriculados,
                'aula': aula,
                'cursos':cursos,
                'cursos_docentes':cursos_docentes,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class AulaCreationView(CreateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_form.html'

    def form_valid(self, form):
        form.instance.colegio = Colegio.objects.get(pk=get_current_colegio())
        form.instance.tipo = 1
        return super(AulaCreationView, self).form_valid(form)

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


#####################################################
#####              CRUD DE CURSO                #####
#####################################################


class CursoListView(MyLoginRequiredMixin, ListView):
    model = Curso
    template_name = 'curso_list.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(CursoListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):

        context = super(CursoListView, self).get_context_data(**kwargs)

        request = get_current_request()

        if request.session.get('colegio'):
            id = request.session.get('colegio')
            context['idcolegio'] = id
        return context

class CursoDetailView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso_detail.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(CursoDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class CursoCreationView(CreateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('academic:curso_list')
    template_name = 'curso_form.html'

    def form_valid(self, form):
        form.instance.colegio = Colegio.objects.get(pk=get_current_colegio())
        return super(CursoCreationView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(CursoCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('academic:curso_list')
    template_name = 'curso_form.html'

class CursoDeleteView(DeleteView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'curso_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(CursoDeleteView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


#####################################################
#####            CRUD DE CURSO DOCENTE          #####
#####################################################

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
            docentes = []
            for personalcol in personalcolegio:
                personal.append(personalcol.personal)
            cursos = AulaCurso.objects.filter(id_aula_curso=request.GET['curso'],
                                              activo=True)
            for persona in personal:
                try:
                    docentes.append(Docente.objects.get(empleado=persona))
                except:
                    logger.info("Persona no es un docente ---- AE_academico")
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'docentes': docentes,
                'cursos': cursos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


#####################################################
#####              CRUD DE  AULA CURSO          #####
#####################################################

class AulaCursoCreateView(TemplateView):
    model = AulaCurso
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aulacurso_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            aula_actual = Aula.objects.get(id_aula=request.GET['aula'])
            cursos = Curso.objects.filter(colegio_id=get_current_colegio(), activo=True)
            return render(request, template_name=self.template_name, context={
                'aula': aula_actual,
                'cursos': cursos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        cursos = Curso.objects.filter(colegio_id=get_current_colegio(), activo=True)
        aula = Aula.objects.get(id_aula=request.POST['aula'])
        data_form = request.POST
        try:
            for curso in cursos:
                text = "item{0}".format(curso.id_curso)

                if data_form[text]:
                    aulacurso = self.model(
                        aula=aula,
                        curso=curso,
                    )
                    aulacurso.save()
                    print("se creo un registro")
        except:
            print("hay un error")

        return HttpResponseRedirect(reverse('academic:aula_list'))


#####################################################
#####            ASISTENCIA ALUMNOS             #####
#####################################################

class MarcarAsistenciaView(CreateView):

    model = Asistencia
    template_name = 'marcar_asistencia.html'
    form_class = MarcarAsistenciaForm
    success_url = reverse_lazy('academic:asistencia_ver')

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            # AQUI VA EL ID DE TIPO DE SERVICIO
            id_tipo_servicio = 1
            docente = True
            id_colegio = get_current_colegio()
            matriculadosaula = Matricula.objects.filter(colegio_id=id_colegio, activo=True, tipo_servicio=id_tipo_servicio).order_by('alumno__apellido_pa')
            logger.info("Datos son {0}".format(matriculadosaula))

            alumnos = []
            for matriculado in matriculadosaula:
                alumnos.append(matriculado.alumno)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'alumnos': alumnos,
                'docente': docente,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        logger.info("Estoy en el POST")
        logger.info("Los datos de llegada son {0}".format(request.POST))
        data_post = request.POST

        alumnos_id = data_post.getlist('id')
        estado_asistencias = data_post.getlist('estado_asistencia')
        logger.info("Los estados son {0}".format(estado_asistencias))
        num = len(alumnos_id)

        for n in range(0,num):
            alumno = Alumno.objects.get(id_alumno = alumnos_id[n])
            asistencia = Asistencia(alumno=alumno, fecha=datetime.date.today(), estado_asistencia=estado_asistencias[n])
            asistencia.save()

        contexto = {}
        return redirect('academic:asistencia_ver')


class MarcarAsistenciaDiaView(TemplateView):

    model = Asistencia
    template_name = 'asistencia_marcar.html'
    success_url = reverse_lazy('academic:asistencia_registrar_dia')

    def MarcarAsistencia1Form(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos las aulas relacionadas al colegio
            id_colegio = get_current_colegio()
            aulas_colegio = Aula.objects.filter(tipo_servicio__colegio=id_colegio).order_by('nombre')

            return {'aulas_colegio': aulas_colegio}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context

    def MarcarAsistencia2Form(self, request):

        roles = ['promotor', 'director']
        if validar_roles(roles=roles):

            # Cargamos los estados de asistencia
            estado_asistencia = ["Sin registro", "Presente", "Tardanza", "Ausente"]

            return {'estado_asistencia': estado_asistencia}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context


    def get(self, request, *args, **kwargs):
        super(MarcarAsistenciaDiaView, self).get(request, *args, **kwargs)

        contexto = self.MarcarAsistencia1Form(request)
        contexto.update(self.MarcarAsistencia2Form(request))

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context

    def post(self, request, *args, **kwargs):
        logger.info("Estoy en el POST")
        logger.info("Los datos de llegada son {0}".format(request.POST))

        if 'aula' in request.POST.keys():

            aula = request.POST["aula"]

            matriculadosaula = AulaMatricula.objects.filter(aula=aula).order_by('matricula__alumno__apellido_pa')
            logger.info("Datos son {0}".format(matriculadosaula))
            alumnos = []
            for matriculado in matriculadosaula:
                alumnos.append(matriculado.matricula.alumno)

            asistencia_hoy = []
            num = len(alumnos)
            for n in range (0, num):
                asistencia_hoy.append(Asistencia.objects.filter(alumno=alumnos[n], fecha=datetime.date.today()))
            logger.info("Las asistencias de hoy son {0}".format(asistencia_hoy))

            contexto = self.MarcarAsistencia1Form(request)
            contexto.update(self.MarcarAsistencia2Form(request))
            contexto['alumnos'] = alumnos
            contexto['asistencias'] = asistencia_hoy

            return render(request, template_name=self.template_name, context=contexto)

        else:
            logger.info("Estoy en el POST")
            logger.info("Los datos de llegada son {0}".format(request.POST))
            data_post = request.POST

            alumnos_id = data_post.getlist('id')
            estado_asistencias = data_post.getlist('estado_asistencia')

            estados = []
            for estado in estado_asistencias:
                if estado == 'Presente':
                    estados.append(1)
                elif estado == 'Tardanza':
                    estados.append(2)
                elif estado == 'Ausente':
                    estados.append(3)
                else:
                    estados.append(4)

            logger.info("Los estados son {0}".format(estado_asistencias))
            num = len(alumnos_id)

            for n in range(0, num):
                alumno = Alumno.objects.get(id_alumno=alumnos_id[n])
                asistencia_primera = Asistencia.objects.filter(alumno=alumno, fecha=datetime.date.today())
                logger.info("{0}".format(asistencia_primera.count()))
                if asistencia_primera.count() == 0:
                    asistencia = Asistencia(alumno=alumno, fecha=datetime.date.today(),
                                            estado_asistencia=estados[n])
                    asistencia.save()
                else:
                    for asistencia in asistencia_primera:
                        asistencia.estado_asistencia = estados[n]
                        asistencia.save()

            return redirect('academic:asistencia_ver')


class VisualizarAsistenciaView(TemplateView):

    model = Asistencia
    template_name = "asistencia_ver.html"
    #form_class = CuentasCobrarPromotorDetalleForm

    def VisualizarAsistenciaform(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos los meses
            meses_todos = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                           "Setiembre", "Octubre", "Noviembre", "Diciembre"]
            num_mes = datetime.date.today().month
            meses = []
            for i in range(0, num_mes + 1):
                meses.append(meses_todos[i])

            id_colegio = get_current_colegio()
            aulas = Aula.objects.filter(tipo_servicio__colegio=id_colegio).order_by('nombre')

            return {'meses': meses_todos, 'aulas': aulas}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context


    def get(self, request, *args, **kwargs):
        super(VisualizarAsistenciaView, self).get(request, *args, **kwargs)

        contexto = self.VisualizarAsistenciaform(request)

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context


    def post(self, request, *args, **kwargs):

        mes = request.POST["mes"]
        aula = request.POST["aula"]
        num_mes = obtener_mes(mes)

        logger.info("Estoy en el Post, datos de llegada son {0}".format(request.POST))

        meses_dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        num_dias = meses_dias[num_mes-1]

        #id_curso =

        asistencias_curso = self.model.objects.filter()

        # Proceso de filtrado según el año
        anio = datetime.date.today().year
        asistencias_curso_anio = asistencias_curso.filter(fecha__year=anio)

        # Proceso de filtrado según el mes
        asistencias_curso_mes = asistencias_curso_anio.filter(fecha__month=num_mes)
        logger.info("La lista de asistencias de mes son {0}".format(asistencias_curso_mes))

        matriculados_aula = AulaMatricula.objects.filter(aula=aula).order_by('matricula__alumno__apellido_pa')
        alumnos = []
        for matriculado in matriculados_aula:
            alumnos.append(matriculado.matricula.alumno)
        num_alumnos = len(alumnos)
        logger.info("El número de alumnos matriculados en esta aula es {0}".format(num_alumnos))

        fechas = []
        lista_asistencias_dia = []
        for dia in range(0, num_dias):
            asistencias_curso_dia = asistencias_curso_mes.filter(fecha__day=dia+1)
            logger.info("La lista de asistencias del día {0} mes son {1}".format(dia+1, asistencias_curso_dia))
            n = 0
            for asistencias_dias in asistencias_curso_dia:
                lista_asistencias_dia.append(asistencias_dias.estado_asistencia)
                if n == 0:
                    fechas.append(asistencias_dias.fecha)
                n = n + 1
        num_horizontal = len(fechas)
        num_vertical = len(alumnos)
        aula_selected = Aula.objects.get(id_aula=aula)

        logger.info("La lista de asistencias de mes son {0}".format(lista_asistencias_dia))
        logger.info("La lista de fechas de mes son {0}".format(fechas))

        contexto = self.VisualizarAsistenciaform(request)

        contexto['asistencias'] = asistencias_curso_mes
        contexto['num_hor'] = num_horizontal
        contexto['num_ver'] = num_vertical
        contexto['fechas'] = fechas
        contexto['alumnos'] = alumnos
        contexto['mes_selected'] = mes
        contexto['aula_selected'] = aula_selected

        return render(request, template_name=self.template_name, context=contexto)


#################################################
#####             NOTAS ALUMNOS             #####
#################################################

#################################################
#####                EVENTOS                #####
#################################################

class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = "evento_form.html"
    success_url = reverse_lazy("academic:evento_list")

    def form_valid(self, form):
        form.instance.colegio = Colegio.objects.get(pk=get_current_colegio())
        return super(EventoCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            personalcolegio = PersonalColegio.objects.filter(colegio_id=get_current_colegio(), activo=True)
            personal = []
            for personalcol in personalcolegio:
                personal.append(personalcol.personal)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'empleados': personal,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class EventoListView(ListView):
    model = Evento
    form_class = EventoForm
    template_name = "evento_list.html"

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            evento = Evento.objects.filter(colegio_id=get_current_colegio())
            return render(request, template_name=self.template_name, context={
                'eventos':evento,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class EventoDetailView(DetailView):
    model = Evento
    form_class = EventoForm
    template_name = "evento_detail.html"


    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            evento = Evento.objects.get(id_evento=request.GET['evento'])
            return render(request, template_name=self.template_name, context={
                'evento':evento,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


#################################################
#####        CRUD DE  MATRICULA AULA        #####
#################################################

class AulaMatriculaCreateView(TemplateView):
    model = AulaMatricula
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aulamatricula_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            aula_actual = Aula.objects.get(id_aula=request.GET['aula'])
            matriculas = Matricula.objects.filter(tipo_servicio=aula_actual.tipo_servicio,colegio_id=get_current_colegio(), activo=True)
            return render(request, template_name=self.template_name, context={
                'aula': aula_actual,
                'matriculas': matriculas,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        aula_actual = Aula.objects.get(id_aula=request.POST['aula'])
        matriculas = Matricula.objects.filter(tipo_servicio=aula_actual.tipo_servicio, colegio_id=get_current_colegio(),
                                              activo=True)

        data_form = request.POST
        try:
            for matricula in matriculas:
                text = "item{0}".format(matricula.id_matricula)

                if data_form[text]:
                    aulamatricula = self.model(
                        aula=aula_actual,
                        matricula=matricula,
                    )
                    aulamatricula.save()
                    print("se creo un registro")
        except:
            print("hay un error")

        return HttpResponseRedirect(reverse('academic:aula_list'))


#################################################
#####       CRUD DE PERIODO ACADEMICO       #####
#################################################

class PeriodoAcademicoListView(MyLoginRequiredMixin, ListView):
    model = PeriodoAcademico
    template_name = 'periodo_list.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(PeriodoAcademicoListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):
        context = super(PeriodoAcademicoListView, self).get_context_data(**kwargs)
        request = get_current_request()
        if request.session.get('colegio'):
            id = request.session.get('colegio')
            context['idcolegio'] = id
        return context

class PeriodoAcademicoDetailView(UpdateView):
    model = PeriodoAcademico
    form_class = PeriodoAcademicoForm
    template_name = 'periodo_detail.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(PeriodoAcademicoDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class PeriodoAcademicoCreationView(CreateView):
    model = PeriodoAcademico
    form_class = PeriodoAcademicoForm
    success_url = reverse_lazy('academic:periodo_list')
    template_name = 'periodo_form.html'

    def form_valid(self, form):
        form.instance.colegio = Colegio.objects.get(pk=get_current_colegio())
        return super(PeriodoAcademicoCreationView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(PeriodoAcademicoCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class PeriodoAcademicoUpdateView(UpdateView):
    model = PeriodoAcademico
    form_class = PeriodoAcademicoForm
    success_url = reverse_lazy('academic:periodo_list')
    template_name = 'periodo_form.html'


#####################################################
#####              NOTAS DE  ALUMNOS            #####
#####################################################

class RegistrarNotasAlumnosView(TemplateView):

    model = Notas
    template_name = 'notas_registrar.html'
    success_url = reverse_lazy('academic:asistencia_registrar_dia')
    form2 = RegistrarNotas2Form

    def RegistrarNotas1Form(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos las aulas relacionadas al colegio
            id_colegio = get_current_colegio()
            periodos_colegio = PeriodoAcademico.objects.filter(colegio=id_colegio).order_by('nombre')
            if periodos_colegio.count() == 0:
                periodos_colegio = ["No hay periodos registrados"]

            # Cargamos las aulas relacionadas al colegio
            id_colegio = get_current_colegio()
            aulas_colegio = Aula.objects.filter(tipo_servicio__colegio=id_colegio).order_by('nombre')
            if aulas_colegio.count() == 0:
                aulas_colegio = ["No hay aulas registradas"]

            cursos =[]
            cursos_aula = AulaCurso.objects.filter(curso__colegio=id_colegio)
            for curso_aula in cursos_aula:
                cursos.append(curso_aula.curso)

            return {'aulas_colegio': aulas_colegio, 'periodos_colegio': periodos_colegio, 'cursos_aula': cursos}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context

    def get(self, request, *args, **kwargs):
        super(RegistrarNotasAlumnosView, self).get(request, *args, **kwargs)

        contexto = self.RegistrarNotas1Form(request)
        contexto2 ={'form2': self.form2}
        contexto.update(contexto2)

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context

    def post(self, request, *args, **kwargs):
        logger.info("Estoy en el POST")
        logger.info("Los datos de llegada son {0}".format(request.POST))

        if 'aula' in request.POST.keys():

            aula = request.POST["aula"]
            periodo = request.POST["periodo_academico"]
            curso = request.POST["curso"]

            aula_selected = Aula.objects.get(id_aula=aula)
            periodo_selected = PeriodoAcademico.objects.get(id_periodo_academico=periodo)
            curso_selected = Curso.objects.get(id_curso=curso)

            matriculadosaula = AulaMatricula.objects.filter(aula=aula).order_by('matricula__alumno__apellido_pa')
            logger.info("Datos son {0}".format(matriculadosaula))
            alumnos = []
            for matriculado in matriculadosaula:
                alumnos.append(matriculado.matricula.alumno)

            contexto = self.RegistrarNotas1Form(request)
            contexto2 = {'form2': self.form2}
            contexto.update(contexto2)
            contexto['alumnos'] = alumnos
            contexto['aula_selected'] = aula_selected
            contexto['periodo_selected'] = periodo_selected
            contexto['curso_selected'] = curso_selected

            return render(request, template_name=self.template_name, context=contexto)

        else:
            logger.info("Estoy en el POST")
            logger.info("Los datos de llegada son {0}".format(request.POST))
            data_post = request.POST

            alumnos_id = data_post.getlist('id')
            notas = data_post.getlist('nota')
            curso_id = data_post['curso']
            periodo_id = data_post['periodo']
            colegio_id = get_current_colegio()

            curso = Curso.objects.get(id_curso=curso_id)
            periodo = PeriodoAcademico.objects.get(id_periodo_academico=periodo_id)
            colegio = Colegio.objects.get(id_colegio=colegio_id)

            num = len(alumnos_id)

            for n in range(0, num):
                alumno = Alumno.objects.get(id_alumno=alumnos_id[n])
                nota = Notas(alumno=alumno, curso=curso, periodo_academico=periodo, nota=notas[n], colegio=colegio)
                nota.save()

            return redirect('academic:notas_ver')


class VisualizarNotasView(TemplateView):

    model = Notas
    template_name = "notas_ver.html"

    def VisualizarNotasform(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos los meses
            meses_todos = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                           "Setiembre", "Octubre", "Noviembre", "Diciembre"]
            num_mes = datetime.date.today().month
            meses = []
            for i in range(0, num_mes + 1):
                meses.append(meses_todos[i])

            id_colegio = get_current_colegio()
            aulas = Aula.objects.filter(tipo_servicio__colegio=id_colegio).order_by('nombre')

            return {'meses': meses_todos, 'aulas': aulas}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context

    def get(self, request, *args, **kwargs):
        super(VisualizarAsistenciaView, self).get(request, *args, **kwargs)

        contexto = self.VisualizarAsistenciaform(request)

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context

    def post(self, request, *args, **kwargs):

        mes = request.POST["mes"]
        aula = request.POST["aula"]
        num_mes = obtener_mes(mes)

        logger.info("Estoy en el Post, datos de llegada son {0}".format(request.POST))

        meses_dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        num_dias = meses_dias[num_mes - 1]

        # id_curso =

        asistencias_curso = self.model.objects.filter()

        # Proceso de filtrado según el año
        anio = datetime.date.today().year
        asistencias_curso_anio = asistencias_curso.filter(fecha__year=anio)

        # Proceso de filtrado según el mes
        asistencias_curso_mes = asistencias_curso_anio.filter(fecha__month=num_mes)
        logger.info("La lista de asistencias de mes son {0}".format(asistencias_curso_mes))

        matriculados_aula = AulaMatricula.objects.filter(aula=aula).order_by('matricula__alumno__apellido_pa')
        alumnos = []
        for matriculado in matriculados_aula:
            alumnos.append(matriculado.matricula.alumno)
        num_alumnos = len(alumnos)
        logger.info("El número de alumnos matriculados en esta aula es {0}".format(num_alumnos))

        fechas = []
        lista_asistencias_dia = []
        for dia in range(0, num_dias):
            asistencias_curso_dia = asistencias_curso_mes.filter(fecha__day=dia + 1)
            logger.info(
                "La lista de asistencias del día {0} mes son {1}".format(dia + 1, asistencias_curso_dia))
            n = 0
            for asistencias_dias in asistencias_curso_dia:
                lista_asistencias_dia.append(asistencias_dias.estado_asistencia)
                if n == 0:
                    fechas.append(asistencias_dias.fecha)
                n = n + 1
        num_horizontal = len(fechas)
        num_vertical = len(alumnos)
        aula_selected = Aula.objects.get(id_aula=aula)

        logger.info("La lista de asistencias de mes son {0}".format(lista_asistencias_dia))
        logger.info("La lista de fechas de mes son {0}".format(fechas))

        contexto = self.VisualizarAsistenciaform(request)

        contexto['asistencias'] = asistencias_curso_mes
        contexto['num_hor'] = num_horizontal
        contexto['num_ver'] = num_vertical
        contexto['fechas'] = fechas
        contexto['alumnos'] = alumnos
        contexto['mes_selected'] = mes
        contexto['aula_selected'] = aula_selected

        return render(request, template_name=self.template_name, context=contexto)


#################################################
#####          HORARIOS DE CURSOS           #####
#################################################

class HorarioAulaCreateView(CreateView):
    model = HorarioAula
    form_class = HorarioAulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'horarios_aula.html'

    """
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            curso = CursoDocente.objects.filter(curso=request.GET["curso"], activo=True)

            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'curso': curso,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
    """


def get_cursos(request):
    if request.is_ajax():
        id_aula = request.GET.get("id_aula", " ")
        aula_cursos = AulaCurso.objects.filter(aula__id_aula=int(id_aula))
        results = []
        for aula_curso in aula_cursos:
            aula_curso_json = {}
            aula_curso_json['id'] = aula_curso.curso.id_curso
            aula_curso_json['value'] = aula_curso.curso.nombre
            results.append(aula_curso_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'

    return HttpResponse(data, mimetype)