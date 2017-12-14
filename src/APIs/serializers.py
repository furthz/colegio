
from rest_framework import serializers

from AE_academico.models import Asistencia, Aula, AulaMatricula, CursoDocente, Curso, AulaCurso
from enrollment.models import Matricula
from register.models import Profile, Colegio, Apoderado, Alumno, ApoderadoAlumno
from rest_framework_jwt.views import JSONWebTokenSerializer
from authtools.models import User
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CustomJWTSerializer(JSONWebTokenSerializer):
    username_field = 'username_or_email'

    def validate(self, attrs):

        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get("username_or_email")).first() or User.objects.filter(name=attrs.get("username_or_email")).first()
        if user_obj is not None:
            credentials = {
                'username':user_obj.email,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = ('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = ('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)

            else:
                msg = ('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)

        else:
            msg = ('Account with this email/username does not exists')
            raise serializers.ValidationError(msg)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id_persona', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma')

        # fields = ('id_persona', 'user_id', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'name', 'email')


class ColegioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colegio
        fields = ('id_colegio', 'nombre', 'ruc', 'ugel', 'personales')


class ApoderadoSerializer(serializers.ModelSerializer):
    nombre_apoderado = serializers.CharField(source='nombre')
    apellido_pa_apoderado = serializers.CharField(source='apellido_pa')
    class Meta:
        model = Apoderado
        fields = ('id_apoderado', 'persona_id', 'nombre_apoderado', 'apellido_pa_apoderado')


class AlumnoSerializer(serializers.ModelSerializer):
    #matricula_id = serializers.IntegerField(source='alumno.matricula.id', read_only=True)
    class Meta:
        model = Alumno
        fields = ('id_alumno', 'persona_id', 'picture', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento')


class ApoderadoAlumnoSerializer(serializers.ModelSerializer):
    nombre_alumno = serializers.CharField(source='alumno.nombre', read_only=True)
    apellido_alumno = serializers.CharField(source='alumno.apellido_pa', read_only=True)
    class Meta:
        model = ApoderadoAlumno
        fields = ('id_apoderadoalumno', 'alumno_id', 'apoderado_id', 'nombre_alumno', 'apellido_alumno')


class MatriculaSerializer(serializers.ModelSerializer):
    persona_id = serializers.IntegerField(source='alumno.persona_id', read_only=True)
    picture = serializers.ImageField(source='alumno.picture', read_only=True)
    nombre_alumno = serializers.CharField(source='alumno.nombre', read_only=True)
    segundo_nombre_alumno = serializers.CharField(source='alumno.segundo_nombre', read_only=True)
    apellido_pa_alumno = serializers.CharField(source='alumno.apellido_pa', read_only=True)
    apellido_ma_alumno = serializers.CharField(source='alumno.apellido_ma', read_only=True)
    tipo_documento_alumno = serializers.IntegerField(source='alumno.tipo_documento', read_only=True)
    numero_documento_alumno = serializers.CharField(source='alumno.numero_documento', read_only=True)

    #nombre_alumno = serializers.CharField(source='alumno.nombre', read_only=True)
    #apellido_alumno = serializers.CharField(source='alumno.apellido_pa', read_only=True)
    class Meta:
        model = Matricula
        fields = ('id_matricula', 'alumno_id', 'colegio_id', 'persona_id', 'picture', 'nombre_alumno', 'segundo_nombre_alumno', 'apellido_pa_alumno', 'apellido_ma_alumno', 'tipo_documento_alumno', 'numero_documento_alumno')


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


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = ('id_matricula', 'alumno', 'colegio', 'tipo_servicio')


class AlumnoSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id_alumno', 'getNombreFormal')

      
    
    
class RelacionUsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id_persona', 'id_personal', 'numero_documento', 'apellido_pa', 'nombre')


class RelacionPerfilAlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id_colegio', 'id_matricula',  'id_alumno', 'id_persona', 'apellido_pa', 'nombre')

        
