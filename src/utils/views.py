from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render

import logging

from profiles.models import Profile
from register.models import Personal

logger = logging.getLogger("project")


# Create your views here.
class ContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Es posible agregar valores al contexto
        return context


class MyLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        logger.debug("MIXIN LOGGIN: ")
        logger.debug("usuario logueado: " + str(request.user.is_authenticated()))
        logger.debug("colegio: " + str(request.session.get('colegio')))
        if not request.user.is_authenticated() or not request.session.get('colegio'):
            return HttpResponseRedirect('/login/')
        return super().dispatch(request, *args, **kwargs)


class SaveGeneric:

    @staticmethod
    def saveGeneric(padre, form, hijo, **atributos):

        try:
            persona_registrada = Profile.objects.get(numero_documento=form.cleaned_data["numero_documento"],
                                                     tipo_documento=form.cleaned_data["tipo_documento"])

            logger.debug("Persona ya registrada en la tabla Profile con ID: " + str(persona_registrada.id_persona))

        except Profile.DoesNotExist:
            persona_registrada = None


        if padre is Profile:

            if persona_registrada is not None:
                # SaveGeneric().copiarVal(child=hijo, parent=padre)
                rpta = hijo().saveFromPersona(per=persona_registrada, **atributos)
                return rpta
            else:
                instance = form.save()
                instance.save()
                return instance

        elif padre is Personal:

            if persona_registrada is not None:
                # SaveGeneric().copiarVal(child=hijo, parent=padre)
                rpta = hijo().saveFromPersonal(per=persona_registrada, **atributos)
                return rpta
            else:
                instance = form.save()
                instance.save()
                return instance


def copiarVal(child, parent: Profile):
    parent.nombre = child.nombre
    parent.segundo_nombre = child.segundo_nombre
    parent.apellido_pa = child.apellido_pa
    parent.apellido_ma = child.apellido_ma
    parent.correo = child.correo

    parent.save()
