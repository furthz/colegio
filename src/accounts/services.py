from django.core import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.conf import settings
from enrollment.models import Matricula
from profiles.models import Profile
from register.models import Colegio, Personal, Promotor, Director, Cajero, Tesorero, Administrativo, Apoderado
from utils.middleware import get_current_colegio, get_current_user

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class Roles:

    @staticmethod
    def get_roles():
        id_colegio = get_current_colegio()
        colegio = Colegio.objects.get(pk=id_colegio, activo=True)

        id_user = get_current_user()
        profile = Profile.objects.get(user_id=id_user)

        # determinar si es un personal asociado al colegio logueado
        empleados = Personal.objects.filter(persona=profile, personalcolegio__colegio=colegio,
                                            personalcolegio__activo=True)

        roles = {}
        for empleado in empleados:
            try:
                promotor = Promotor.objects.get(empleado=empleado, activo_promotor=True)
                roles['promotor'] = promotor.id_promotor
            except Promotor.DoesNotExist:
                promotor = None

            try:
                director = Director.objects.get(empleado=empleado, activo_director=True)
                roles['director'] = director.id_director
            except Director.DoesNotExist:
                director = None

            try:
                cajero = Cajero.objects.get(empleado=empleado, activo_cajero=True)
                roles['cajero'] = cajero.id_cajero
            except Cajero.DoesNotExist:
                cajero = None

            try:
                tesorero = Tesorero.objects.get(empleado=empleado, activo_tesorero=True)
                roles['tesorero'] = tesorero.id_tesorero
            except Tesorero.DoesNotExist:
                tesorero = None

            try:
                administrativo = Administrativo.objects.get(empleado=empleado, activo_administrativo=True)
                roles['administrativo'] = administrativo.id_administrativo
            except Administrativo.DoesNotExist:
                administrativo = None

        # determinar si es un apoderado
        try:
            apoderado = Apoderado.objects.get(persona=profile)

            apoderados = Matricula.objects.filter(colegio=colegio, activo=True,
                                                  alumno__apoderadoalumno__apoderado=apoderado)

            for apo in apoderados:
                roles['apoderado'] = apo.id_apoderado
        except Apoderado.DoesNotExist:
            pass

        return roles
