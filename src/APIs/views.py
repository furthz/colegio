from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view

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
from register.models import Docente

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


@api_view(['GET'])
def ApoderadoInfo(request):
    user = request.user
    iduser = user.pk
    profile_id = Profile.objects.get(user_id=iduser)
    id_apoderado = Apoderado.objects.values('pk').filter(persona_id=profile_id)[0]['pk']
    nombre_apoderado = Profile.objects.values('nombre').filter(user_id=iduser)[0]['nombre']
    apellido_pa_apoderado = Profile.objects.values('apellido_pa').filter(user_id=iduser)[0]['apellido_pa']

    persona_id = Profile.objects.values('pk').filter(user_id=iduser)[0]['pk']

    # ==== Query for token_firebase ===

    # query = TokenFirebase.objects.all()
    # tokens_firebase = query.filter(persona_id=profile_id)
    # serializer_data_token = TokenFirebaseSerializer(tokens_firebase, many=True)

    return Response({
        'id_apoderado': id_apoderado,
        'nombre_apoderado': nombre_apoderado,
        'apellido_pa_apoderado': apellido_pa_apoderado,
        #    'token_firebase': serializer_data_token.data

        'id_persona': persona_id,
        # 'username': user.name,
        # 'email': user.email,
    })


@api_view(['GET'])
def DocenteInfo(request):
    user = request.user
    iduser = user.pk
    profile_id = Profile.objects.get(user_id=iduser)
    personal_id = Personal.objects.get(persona_id=profile_id)
    id_docente = Docente.objects.values('pk').filter(empleado_id=personal_id)[0]['pk']
    nombre_docente = Profile.objects.values('nombre').filter(user_id=iduser)[0]['nombre']
    apellido_pa_docente = Profile.objects.values('apellido_pa').filter(user_id=iduser)[0]['apellido_pa']

    # ==== Query for token_firebase ===

    # query = TokenFirebase.objects.all()
    # tokens_firebase = query.filter(persona_id=profile_id)
    # serializer_data_token = TokenFirebaseSerializer(tokens_firebase, many=True)

    return Response({
        'apellido_pa_docente': apellido_pa_docente,
        'id_docente': id_docente,
        'nombre_docente': nombre_docente,
        #    'token_firebase': serializer_data_token.data

    })


class ColegioList(generics.ListCreateAPIView):
    queryset = Colegio.objects.all()
    serializer_class = ColegioSerializer
    filter_fields = ('id_colegio',)

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'colegios': serializer.data})


class ColegioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colegio.objects.all()
    serializer_class = ColegioSerializer


class PerfilList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_fields = ('id_persona',)


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
    filter_fields = ('apoderado_id',)

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'alumnos': serializer.data})


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
        # snippet = self.get_object(pk)
        snippet = Colegio.objects.get(id_colegio=nombre)
        # snippet = Colegio.objects.get(nombre="Mundopixel")

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

        prueba = RelacionUsuarioPerfil(id_persona=1, id_personal=1, numero_documento=74926380, nombre="Marco",
                                       apellido_pa="Silva")

        serializer = RelacionUsuarioPerfilSerializer(prueba, many=False)
        return Response(serializer.data)


class RelacionPerfilAlumnoView(APIView):
    def get_object(self, pk):
        try:
            return CursoDocente.objects.get(pk=pk)
        except CursoDocente.DoesNotExist:
            raise Http404

    def get(self, request, pk, docente, format=None):

        prueba = RelacionPerfilAlumno(id_persona=1, id_matricula=1, id_alumno=1, id_colegio=1, nombre="Marco",
                                      apellido_pa="Perez")

        serializer = RelacionPerfilAlumnoSerializer(prueba, many=False)
        return Response(serializer.data)


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
        mes = int(mes)  # El mes es un número del 1 al 12, correspondiendo de Enero a Diciembre respectivamente

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
        logger.info("Los alumnos del aula {0} son {1}".format(aula, alumnos_aula))
        serializer = AlumnoSerializer2(alumnos_aula, many=True)

        return Response(serializer.data)


class PersonaEmisorList(generics.ListCreateAPIView):
    queryset = PersonaEmisor.objects.all()
    serializer_class = PersonaEmisorSerializer

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'persona_emisor': serializer.data})


class PersonaEmisorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonaEmisor.objects.all()
    serializer_class = PersonaEmisorSerializer


class PersonaReceptorList(generics.ListCreateAPIView):
    queryset = PersonaReceptor.objects.all()
    serializer_class = PersonaReceptorSerializer

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'persona_receptor': serializer.data})


class PersonaReceptorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonaReceptor.objects.all()
    serializer_class = PersonaReceptorSerializer


class TipoAlertaList(generics.ListCreateAPIView):
    queryset = TipoAlerta.objects.all()
    serializer_class = TipoAlertaSerializer

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'tipo_alerta': serializer.data})


class TipoAlertaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipoAlerta.objects.all()
    serializer_class = TipoAlertaSerializer


class EstadoAlertaList(generics.ListCreateAPIView):
    queryset = EstadoAlerta.objects.all()
    serializer_class = EstadoAlertaSerializer

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'estado_alerta': serializer.data})


class EstadoAlertaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EstadoAlerta.objects.all()
    serializer_class = EstadoAlertaSerializer


class ContenidoAlertaList(generics.ListCreateAPIView):
    queryset = ContenidoAlerta.objects.all()
    serializer_class = ContenidoAlertaSerializer

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'contenido_alerta': serializer.data})


class ContenidoAlertaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContenidoAlerta.objects.all()
    serializer_class = ContenidoAlertaSerializer


class AlertaList(generics.ListCreateAPIView):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    filter_fields = ('persona_receptor',)

    def filter_queryset(self, queryset):
        queryset = super(AlertaList, self).filter_queryset(queryset)
        return queryset.order_by('-fecha_creacion')


class AlertaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer


class TokenFirebaseList(generics.ListCreateAPIView):
    queryset = TokenFirebase.objects.all()
    serializer_class = TokenFirebaseSerializer
    filter_fields = ('alumno_id',)

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'token_firebase': serializer.data})


class TokenFirebaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TokenFirebase.objects.all()
    serializer_class = TokenFirebaseSerializer


class GroupList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = Usuario_permisoSerializer


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = Usuario_permisoSerializer
