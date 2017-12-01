
from django.shortcuts import render

# Create your views here.
from AE_academico.models import Asistencia, Aula, AulaMatricula, CursoDocente, AulaCurso
from enrollment.models import Matricula
from register.models import Profile ,Personal ,PersonalColegio ,Colegio, Alumno
from .serializers import ColegioSerializer, ProfileSerializer, AsistenciaSerializer, AulaSerializer, \
    CursoDocenteSerializer, MatriculaSerializer, AlumnoSerializer, AulaCursoSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.views.generic import ListView
from utils.middleware import get_current_request, get_current_user, get_current_colegio
from authtools.models import User
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
        #personalcolegio_id = PersonalColegio.objects.values('pk').filter(personal_id=personal_id)[0]['pk']
        context['id_usuario'] = iduser
        context['nombre_usuario'] = User.objects.values('name').filter(id=iduser)[0]['name']
        context['usuario_email'] = User.objects.values('email').filter(id=iduser)[0]['email']
        context['nombre_profile'] = Profile.objects.values('nombre').filter(user_id=iduser)[0]['nombre']
        context['nombre2_profile'] = Profile.objects.values('segundo_nombre').filter(user_id=iduser)[0]['segundo_nombre']
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


class AulaCursoList(APIView):

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
            for curso_docente in cursos_docente:
                aula_curso = curso_docente.curso
                aula_cursos.append(aula_curso)
        else:
            cursos_docente = CursoDocente.objects.filter(curso__curso__colegio=colegio_id)
            for curso_docente in cursos_docente:
                aula_curso = curso_docente.curso
                aula_cursos.append(aula_curso)
        # cursos_asociados = list(cursos)
        logger.info("Los cursos asociados al docente son : {0}".format(aula_cursos))
        serializer = AulaCursoSerializer(aula_cursos, many=True)
        return Response(serializer.data)


class AulaDocenteList(APIView):

    def get_object(self, pk):
        try:
            return CursoDocente.objects.get(pk=pk)
        except CursoDocente.DoesNotExist:
            raise Http404

    def get(self, request, pk, docente, format=None):
        colegio_id = get_current_colegio()
        aulas_docente = []
        if pk == "1":
            cursos_docente = CursoDocente.objects.filter(docente=docente)
            for curso_docente in cursos_docente:
                aula = curso_docente.curso.aula
                if aula not in aulas_docente:
                    aulas_docente.append(aula)
        else:
            cursos_docente = CursoDocente.objects.filter(curso__curso__colegio=colegio_id)
            for curso_docente in cursos_docente:
                aula = curso_docente.curso.aula
                if aula not in aulas_docente:
                    aulas_docente.append(aula)
        # cursos_asociados = list(cursos)
        logger.info("Los cursos asociados al docente son : {0}".format(aulas_docente))
        serializer = AulaSerializer(aulas_docente, many=True)
        return Response(serializer.data)

"""

class AulaCursoList(APIView):

    def get_object(self, pk):
        try:
            return CursoDocente.objects.get(pk=pk)
        except CursoDocente.DoesNotExist:
            raise Http404

    def get(self, request, pk, docente, format=None):
        colegio_id = get_current_colegio()
        if pk == "1":
            cursos = CursoDocente.objects.filter(docente=docente)
            for curso in cursos:
                aula_curso = AulaCurso.objects.filter(curso__curso=curso)
        else:
            cursos = CursoDocente.objects.filter(curso__curso__colegio=colegio_id)
            for curso in cursos:
                aula_curso = AulaCurso.objects.filter(curso__curso=curso)
        cursos_asociados = list(cursos)
        logger.info("Las aulas asociadas son {0}".format(aula_curso))
        serializer = CursoDocenteSerializer(cursos_asociados, many=True)
        return Response(serializer.data)
"""
"""
class ListaAsistencia(APIView):

    def get_object(self, pk):
        try:
            return CursoDocente.objects.get(pk=pk)
        except CursoDocente.DoesNotExist:
            raise Http404

    def get(self, request, pk, docente, format=None):
        cursos = CursoDocente.objects.filter(docente=docente)
        cursos_asociados = list(cursos)
        serializer = CursoDocenteSerializer(cursos_asociados, many=True)
        return Response(serializer.data)
"""