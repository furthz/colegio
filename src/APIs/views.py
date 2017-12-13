
from django.shortcuts import render

# Create your views here.
from AE_academico.models import Asistencia, Aula, AulaMatricula, CursoDocente, AulaCurso
from enrollment.models import Matricula
from register.models import Profile, Personal, PersonalColegio, Colegio, Apoderado, Alumno, ApoderadoAlumno
from APIs.models import RelacionUsuarioPerfil
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from django.views.generic import ListView
from utils.middleware import get_current_request, get_current_user, get_current_colegio
from authtools.models import User
from django.http import Http404
from rest_framework.response import Response
import logging
logger = logging.getLogger("project")

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.http import Http404
from rest_framework.response import Response
import logging
logger = logging.getLogger("project")

class UserInfoListView(ListView):
    model = Profile
    template_name = 'UserInfo.html'

    def get_context_data(self, **kwargs):
        context = super(UserInfoListView, self).get_context_data(**kwargs)
        usuario = get_current_user()
        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1
        profile_id = Profile.objects.get(user_id=iduser)
        personal_id = Personal.objects.get(persona_id=profile_id)
        # personalcolegio_id = PersonalColegio.objects.values('pk').filter(personal_id=personal_id)[0]['pk']
        context['id_usuario'] = iduser
        context['nombre_usuario'] = User.objects.values('name').filter(id=iduser)[0]['name']
        context['usuario_email'] = User.objects.values('email').filter(id=iduser)[0]['email']
        context['nombre_profile'] = Profile.objects.values('nombre').filter(user_id=iduser)[0]['nombre']
        context['nombre2_profile'] = Profile.objects.values('segundo_nombre').filter(user_id=iduser)[0][
            'segundo_nombre']
        context['apellido_pa_profile'] = Profile.objects.values('apellido_pa').filter(user_id=iduser)[0]['apellido_pa']
        context['apellido_ma_profile'] = Profile.objects.values('apellido_ma').filter(user_id=iduser)[0]['apellido_ma']
        id_colegio = PersonalColegio.objects.values('colegio_id').filter(personal_id=personal_id)[0]['colegio_id']
        context['id_colegio'] = id_colegio
        context['nombre_colegio'] = Colegio.objects.values('nombre').filter(id_colegio=id_colegio)[0]['nombre']
        return context


class ColegioList(generics.ListCreateAPIView):
    queryset = Colegio.objects.all()
    serializer_class = ColegioSerializer

class ColegioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colegio.objects.all()
    serializer_class = ColegioSerializer


class PerfilList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class PerfilDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ApoderadoList(generics.ListCreateAPIView):
    queryset = Apoderado.objects.all()
    serializer_class = ApoderadoSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['=numero_documento', ]


class ApoderadoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Apoderado.objects.all()
    serializer_class = ApoderadoSerializer


class AlumnoList(generics.ListCreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['=id_alumno', ]


class AlumnoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer


class ApoderadoAlumnoList(generics.ListCreateAPIView):
    queryset = ApoderadoAlumno.objects.all()
    serializer_class = ApoderadoAlumnoSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['=apoderado_id__id_apoderado', ]


class ApoderadoAlumnoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApoderadoAlumno.objects.all()
    serializer_class = ApoderadoAlumnoSerializer


class MatriculaList(generics.ListCreateAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['=alumno_id__id_alumno', ]


class MatriculaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer


class AsistenciaList(generics.ListCreateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class AsistenciaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer


class AulaList(generics.ListCreateAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer

class AulaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer

# AULA DOCENTE



class MatriculaList(generics.ListCreateAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

class MatriculaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer


class AlumnoList(generics.ListCreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class AlumnoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Colegio.objects.get(pk=pk)
        except Colegio.DoesNotExist:
            raise Http404

    def get(self, request, pk, nombre, format=None):
        #snippet = self.get_object(pk)
        snippet = Colegio.objects.get(id_colegio=nombre)
        #snippet = Colegio.objects.get(nombre="Mundopixel")

        serializer = ColegioSerializer(snippet)
        return Response(serializer.data)

class CursoDocenteList(APIView):

    def get_object(self, pk):
        try:
            return CursoDocente.objects.get(pk=pk)
        except CursoDocente.DoesNotExist:
            raise Http404

    def get(self, request, pk, docente, format=None):
        colegio_id = get_current_colegio()
        aula_cursos = []
        if pk == "1":
            cursos_docente = CursoDocente.objects.filter(docente=docente)
        else:
            cursos_docente = CursoDocente.objects.filter(curso__curso__colegio=colegio_id)
        cursos_asociados = list(cursos_docente)
        serializer = CursoDocenteSerializer(cursos_asociados, many=True)
        return Response(serializer.data)


#########################################################
######   WEB SERVICE CURSOS ASOCIADAS A DOCENTE   #######
#########################################################

class DocenteCursoList(APIView):

    def get_object(self, pk):
        try:
            return CursoDocente.objects.get(pk=pk)
        except CursoDocente.DoesNotExist:
            raise Http404

    def get(self, request, pk, docente):

        # Obteniendo los cursos asociadas a un docente
        aula_cursos = []
        cursos_docente = CursoDocente.objects.filter(docente=docente)
        for curso_docente in cursos_docente:
            aula_curso = curso_docente.curso
            aula_cursos.append(aula_curso)

        # Serializando: Se entregan los siguientes datos: 'id_aula_curso', 'getDetalle (ejemplo:Ciencia y Ambiente del salón 5°A)'
        logger.info("Los cursos asociados al docente son: {0}".format(aula_cursos))
        serializer = AulaCursoSerializer(aula_cursos, many=True)
        return Response(serializer.data)


#########################################################
######   WEB SERVICE AULAS ASOCIADAS A DOCENTE   ########
#########################################################

class DocenteAulaList(APIView):

    def get_object(self, pk):
        try:
            return CursoDocente.objects.get(pk=pk)
        except CursoDocente.DoesNotExist:
            raise Http404

    def get(self, request, pk, docente):
        colegio_id = get_current_colegio()

        # Obteniendo las aulas asociadas a un docente
        aulas_docente = []
        cursos_docente = CursoDocente.objects.filter(docente=docente)
        for curso_docente in cursos_docente:
            aula = curso_docente.curso.aula
            if aula not in aulas_docente:
                aulas_docente.append(aula)

        # Serializando: Se entregan los siguientes datos: 'id_aula', 'nombre', 'get_tipo_servicio'
        logger.info("Las aulas asociadas al docente son : {0}".format(aulas_docente))
        serializer = AulaSerializer(aulas_docente, many=True)
        return Response(serializer.data)

<<<<<<< HEAD
=======
#################################################################################
#           views de prueba
#################################################################################

class RelacionUsuarioPerfilView(APIView):

    def get_object(self, pk):
        try:
            return CursoDocente.objects.get(pk=pk)
        except CursoDocente.DoesNotExist:
            raise Http404

    def get(self, request, pk, docente, format=None):

        prueba = RelacionUsuarioPerfil(id_persona=1,id_personal=1,numero_documento=74926380,nombre="Marco",apellido_pa="Silva")

        serializer = RelacionUsuarioPerfilSerializer(prueba, many=False)
        return Response(serializer.data)

class RelacionPerfilAlumnoView(APIView):

    def get_object(self, pk):
        try:
            return CursoDocente.objects.get(pk=pk)
        except CursoDocente.DoesNotExist:
            raise Http404

    def get(self, request, pk, docente, format=None):

        prueba = RelacionPerfilAlumno(id_persona=1,id_matricula=1,id_alumno=1,id_colegio=1,nombre="Marco",apellido_pa="Perez")

        serializer = RelacionPerfilAlumnoSerializer(prueba, many=False)
        return Response(serializer.data)


"""
>>>>>>> af04c901496b74f5772570bdede0c8a062d6ecab

#########################################################
######   WEB SERVICE VISUALIZAR ASISTENCIA MES   ########
#########################################################

class AulaAsistenciaList(APIView):

    def get_object(self, pk):
        try:
            return Asistencia.objects.get(pk=pk)
        except Asistencia.DoesNotExist:
            raise Http404

    def get(self, request, pk, aula, mes):

        aula = int(aula)
        mes = int(mes) # El mes es un número del 1 al 12, correspondiendo de Enero a Diciembre respectivamente

        # Obteniendo la lista de alumnos matriculados en dicha aula
        alumnos_aula = []
        matriculados_aula = AulaMatricula.objects.filter(aula=aula)
        for matriculado_aula in matriculados_aula:
            alumnos_aula.append(matriculado_aula.matricula.alumno)

        # Obteniendo la lista de asistencias del mes por alumno
        asistencias_aula_mes = []
        for alumno in alumnos_aula:
            asistencias_alumno = Asistencia.objects.filter(alumno=alumno, fecha__month=mes)
            for asistencia_alumno in asistencias_alumno:
                asistencias_aula_mes.append(asistencia_alumno)

        # Serializando: Se entregan los siguientes datos: 'id_asistencia', 'alumno', 'fecha', 'estado_asistencia'
        logger.info("Los asistencias del mes del aula {0} son {1}".format(aula, asistencias_aula_mes))
        serializer = AsistenciaSerializer(asistencias_aula_mes, many=True)

        return Response(serializer.data)


#########################################################
#######   WEB SERVICE ALUMNOS ASOCIADOS A AULA   ########
#########################################################

class AulaAlumnosList(APIView):

    def get_object(self, pk):
        try:
            return Alumno.objects.get(pk=pk)
        except Alumno.DoesNotExist:
            raise Http404

    def get(self, request, pk, aula):

        aula = int(aula)

        # Obteniendo la lista de alumnos matriculados en dicha aula
        alumnos_aula = []
        matriculados_aula = AulaMatricula.objects.filter(aula=aula)
        for matriculado_aula in matriculados_aula:
            alumnos_aula.append(matriculado_aula.matricula.alumno)

        # Serializando: Se entregan los siguientes datos: 'id_asistencia', 'alumno', 'fecha', 'estado_asistencia'
        logger.info("Los alumnos del aula {0} son {1}".format(aula,alumnos_aula))
        serializer = AlumnoSerializer2(alumnos_aula, many=True)

        return Response(serializer.data)

