from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render

import logging

logger = logging.getLogger("project")

# Create your views here.
class ContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Es posible agregar valores al contexto
        return context


class MyLoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        logger.debug("MIXIN LOGGIN: ")
        logger.debug("usuario logueado: " + str(request.user.is_authenticated()))
        logger.debug("colegio: " + str(request.session.get('colegio')))
        if not request.user.is_authenticated() or not request.session.get('colegio'):
            return HttpResponseRedirect('/login/')
        return super().dispatch(request, *args, **kwargs)
