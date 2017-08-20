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
                copiarVal(form=form, parent=persona_registrada)
                rpta = hijo().saveFromPersona(per=persona_registrada, parentesco=form.cleaned_data["parentesco"])
                logger.debug("Se guardó un registró a partir de la persona existente")
                return rpta
            else:
                instance = form.save()
                instance.save()
                logger.debug("Se creó un nuevo registro")
                return instance

        elif padre is Personal:

            if persona_registrada is not None:
                copiarVal(child=form, parent=persona_registrada)
                rpta = hijo().saveFromPersonal(per=persona_registrada, **atributos)
                logger.debug("se creó un personal a partir de la persona")
                return rpta
            else:
                instance = form.save()
                instance.save()
                logger.debug("Se creó un nuevo personal")
                return instance


def copiarVal(form, parent: Profile):

    parent.nombre = form.cleaned_data["nombre"]
    logger.debug("se modificó nombre: " + form.cleaned_data["nombre"])

    parent.segundo_nombre = form.cleaned_data["segundo_nombre"]
    logger.debug("Se modificó el segundo_nombre: " + form.cleaned_data["segundo_nombre"])

    parent.apellido_pa = form.cleaned_data["apellido_pa"]
    logger.debug("Se modificó el apellido_pa: " + form.cleaned_data["apellido_pa"])

    parent.apellido_ma = form.cleaned_data["apellido_ma"]
    logger.debug("Se modificó apellido_pa: " + form.cleaned_data["apellido_ma"])

    parent.correo = form.cleaned_data["correo"]
    logger.debug("Se modificó correo: " + form.cleaned_data["correo"])

    parent.save()
    logger.debug("actualizado los campos del profile")