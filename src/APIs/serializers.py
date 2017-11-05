from rest_framework import serializers

from AE_academico.models import Asistencia
from register.models import Profile, Colegio


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

