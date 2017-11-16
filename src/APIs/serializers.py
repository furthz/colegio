from rest_framework import serializers

from AE_academico.models import Asistencia, Aula, AulaMatricula, CursoDocente, Curso, AulaCurso
from enrollment.models import Matricula
from register.models import Profile, Colegio, Alumno


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id_persona', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma')

        #fields = ('id_persona', 'user_id', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'name', 'email')

class ColegioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colegio
        fields = ('id_colegio', 'nombre', 'ruc', 'ugel', 'personales')


###############################################
#####     SERIALIZER MODULO ACADEMICO     #####
###############################################

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ('id_asistencia', 'alumno', 'curso', 'fecha', 'estado_asistencia')

class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = ('id_aula', 'tipo_servicio', 'nombre')


class CursoDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoDocente
        fields = ('id_curso_docente', 'docente', 'curso')

class AulaCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AulaCurso
        fields = ('id_aula_curso', 'getDetalle')


class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = ('id_aula', 'nombre')


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = ('id_matricula', 'alumno', 'colegio', 'tipo_servicio')


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id_alumno', 'persona')