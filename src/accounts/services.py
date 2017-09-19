
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.conf import settings
from enrollment.models import Matricula
from profiles.models import Profile
from register.models import Colegio, Personal, Promotor, Director, Cajero, Tesorero, Administrativo, Apoderado
from utils.middleware import get_current_colegio, get_current_user

import logging

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


logger = logging.getLogger("project")


class Roles:

    @staticmethod
    def get_roles():
        logger.debug("Inicio de get_roles")

        usuario = get_current_user()
        logger.debug("Usuario ID: " + str(usuario.id))

        roles = {}

        if usuario.is_superuser:
            logger.debug("Usuario SUPERUSUARIO")

            roles['promotor'] = 1
            roles['director'] = 1
            roles['cajero'] = 1
            roles['tesorero'] = 1
            roles['administrativo'] = 1
            roles['apoderado'] = 1

            logger.debug("Se asignaron los permisos de SUPERUSUARIO")
            logger.info("Se asignaron los permisos de SUPERUSUARIO")

        else:

            logger.debug("usuario NO SUPERUSUARIO")

            id_colegio = get_current_colegio()
            colegio = Colegio.objects.get(pk=id_colegio, activo=True)
            logger.debug("ID Colegio: " + str(id_colegio))

            profile = Profile.objects.get(user_id=usuario.id)
            logger.debug("Profile: " + profile.apellido_pa )

            # determinar si es un personal asociado al colegio logueado
            empleados = Personal.objects.filter(persona=profile, personalcolegio__colegio=colegio,
                                                personalcolegio__activo=True)
            logger.debug("Cantidad de empleados asociados a la cuenta: " + str(empleados.count()))

            for empleado in empleados:
                try:
                    promotor = Promotor.objects.get(empleado=empleado, activo_promotor=True)
                    roles['promotor'] = promotor.id_promotor
                    logger.debug("Promotor: " + str(promotor.id_promotor))

                except Promotor.DoesNotExist:
                    roles['promotor'] = -1
                    logger.debug("No es un profile Promotor")

                try:
                    director = Director.objects.get(empleado=empleado, activo_director=True)
                    roles['director'] = director.id_director
                    logger.debug("Director: " + str(director.id_director))

                except Director.DoesNotExist:
                    roles['director'] = -1
                    logger.debug("No es un profile Director")

                try:
                    cajero = Cajero.objects.get(empleado=empleado, activo_cajero=True)
                    roles['cajero'] = cajero.id_cajero
                    logger.debug("Cajero: " + str(cajero.id_cajero))

                except Cajero.DoesNotExist:
                    roles['cajero'] = -1
                    logger.debug("No es un profile Cajero")

                try:
                    tesorero = Tesorero.objects.get(empleado=empleado, activo_tesorero=True)
                    roles['tesorero'] = tesorero.id_tesorero
                    logger.debug("Tesorero: " + str(tesorero.id_tesorero))

                except Tesorero.DoesNotExist:
                    roles['tesorero'] = -1
                    logger.debug("No es un profile Tesorero")

                try:
                    administrativo = Administrativo.objects.get(empleado=empleado, activo_administrativo=True)
                    roles['administrativo'] = administrativo.id_administrativo
                    logger.debug("Administrativo: " + str(administrativo.id_administrativo))

                except Administrativo.DoesNotExist:
                    roles['administrativo'] = -1
                    logger.debug("No es un profile Administrativo")

            # determinar si es un apoderado
            try:
                apoderado = Apoderado.objects.get(persona=profile)

                apoderados = Matricula.objects.filter(colegio=colegio, activo=True,
                                                      alumno__apoderadoalumno__apoderado=apoderado)

                logger.debug("Apoderados asociados a matriculas: " + str(apoderados.count()))

                if apoderados.count() == 0:
                    roles['apoderado'] = -1
                    logger.debug("No es profile Apoderado")

                for apo in apoderados:
                    roles['apoderado'] = apo.id_matricula
                    logger.debug("usuario Apoderado: " + str(apo.id_matricula))

            except Apoderado.DoesNotExist:
                roles['apoderado'] = -1
                logger.debug("No es un profile Apoderado")

        logger.info("Se asignaron los roles al profile")
        logger.debug("Fin de get_roles")
        return roles
