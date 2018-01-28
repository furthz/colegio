from rest_framework import serializers

from AE_academico.models import Asistencia, Aula, AulaMatricula, CursoDocente, Curso, AulaCurso
from enrollment.models import Matricula
from register.models import Profile, Colegio, Apoderado, Alumno, ApoderadoAlumno, Direccion, Telefono
from profiles.models import TokenFirebase
from alerta.models import *
from authtools.models import User
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    id_rol = serializers.IntegerField(source='id')
    rol = serializers.CharField(source='name')

    class Meta:
        model = Group
        fields = ('id_rol', 'rol',)


class Usuario_permisoSerializer(serializers.ModelSerializer):
    roles = GroupSerializer(many=True, source='groups')

    class Meta:
        model = User
        fields = ('roles',)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    permisos = Usuario_permisoSerializer(source='user')

    class Meta:
        model = Profile
        fields = ('id_persona', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'picture', 'permisos')

        # fields = ('id_persona', 'user_id', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'name', 'email')


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('calle', 'dpto')


class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = ('id_colegio', 'nombre', 'ruc', 'ugel',)


class ColegioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colegio
        fields = ('id_colegio', 'nombre', 'ruc', 'ugel',)


class ApoderadoSerializer(serializers.ModelSerializer):
    nombre_apoderado = serializers.CharField(source='nombre')
    apellido_pa_apoderado = serializers.CharField(source='apellido_pa')

    class Meta:
        model = Apoderado
        fields = ('id_apoderado', 'persona_id', 'nombre_apoderado', 'apellido_pa_apoderado')


class FotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('picture',)

        # fields = ('id_persona', 'user_id', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'name', 'email')


class AlumnoSerializer(serializers.ModelSerializer):
    # matricula_id = serializers.IntegerField(source='alumno.matricula.id', read_only=True)
    class Meta:
        model = Alumno
        fields = ('id_alumno', 'persona_id', 'picture', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma',
                  'tipo_documento', 'numero_documento')


class ApoderadoAlumnoSerializer(serializers.ModelSerializer):
    nombre_alumno = serializers.CharField(source='alumno.nombre', read_only=True)
    apellido_alumno = serializers.CharField(source='alumno.apellido_pa', read_only=True)
    alumno_foto = FotoSerializer(source='alumno')

    class Meta:
        model = ApoderadoAlumno
        fields = ('id_apoderadoalumno', 'alumno_id', 'apoderado_id', 'nombre_alumno', 'apellido_alumno', 'alumno_foto')


class MatriculaSerializer(serializers.ModelSerializer):
    persona_id = serializers.IntegerField(source='alumno.persona_id', read_only=True)
    picture = serializers.ImageField(source='alumno.picture', read_only=True)
    nombre_alumno = serializers.CharField(source='alumno.nombre', read_only=True)
    segundo_nombre_alumno = serializers.CharField(source='alumno.segundo_nombre', read_only=True)
    apellido_pa_alumno = serializers.CharField(source='alumno.apellido_pa', read_only=True)
    apellido_ma_alumno = serializers.CharField(source='alumno.apellido_ma', read_only=True)
    tipo_documento_alumno = serializers.IntegerField(source='alumno.tipo_documento', read_only=True)
    numero_documento_alumno = serializers.CharField(source='alumno.numero_documento', read_only=True)

    # nombre_alumno = serializers.CharField(source='alumno.nombre', read_only=True)
    # apellido_alumno = serializers.CharField(source='alumno.apellido_pa', read_only=True)
    class Meta:
        model = Matricula
        fields = (
            'id_matricula', 'alumno_id', 'colegio_id', 'persona_id', 'picture', 'nombre_alumno',
            'segundo_nombre_alumno',
            'apellido_pa_alumno', 'apellido_ma_alumno', 'tipo_documento_alumno', 'numero_documento_alumno')


###############################################
#####     SERIALIZER MODULO ACADEMICO     #####
###############################################


class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ('id_asistencia', 'alumno', 'fecha', 'estado_asistencia')


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
        fields = ('id_aula', 'nombre', 'get_tipo_servicio')


class AlumnoSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id_alumno', 'getNombreFormal')


class MatriculaSerializer(serializers.ModelSerializer):
    alumno = AlumnoSerializer2()

    class Meta:
        model = Matricula
        fields = ('id_matricula', 'colegio', 'tipo_servicio', 'alumno')


class RelacionUsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id_persona', 'id_personal', 'numero_documento', 'apellido_pa', 'nombre')


class RelacionPerfilAlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id_colegio', 'id_matricula', 'id_alumno', 'id_persona', 'apellido_pa', 'nombre')


class PersonaEmisorSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = PersonaEmisor
        fields = '__all__'


class PersonaReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaReceptor
        fields = '__all__'


class TipoAlertaSerializer(serializers.ModelSerializer):
    activo = serializers.BooleanField(initial=True)

    class Meta:
        model = TipoAlerta
        fields = ('id_tipo_alerta', 'descripcion', 'activo')
        # fields = ('id_tipo_alerta', 'descripcion', 'activo', 'fecha_creacion')
        # read_only_fields = ('fecha_creacion',)


class EstadoAlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoAlerta
        fields = ('id_estado_alerta', 'descripcion')


class ContenidoAlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoAlerta
        fields = '__all__'


class AlertaSerializer(serializers.ModelSerializer):
    contenido_alerta_string = serializers.CharField(source='contenido_alerta.contenido', read_only=True)
    tipo_alerta_string = serializers.CharField(source='tipo_alerta.descripcion', read_only=True)
    persona_emisor = PersonaEmisorSerializer()

    # contenido_alerta = ContenidoAlertaSerializer()
    class Meta:
        model = Alerta
        # fields = '__all__'
        fields = ('id_alerta', 'matricula', 'persona_emisor', 'persona_receptor', 'tipo_alerta', 'estado_alerta',
                  'contenido_alerta', 'fecha_creacion', 'visto', 'contenido_alerta_string', 'tipo_alerta_string')
        read_only_fields = ('fecha_creacion',)

        # depth = 1,2,etc


class TokenFirebaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenFirebase
        fields = ('persona', 'codigo', 'alumno_id')
