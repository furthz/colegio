"""
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from AE_academico.forms import AulaForm
from AE_academico.models import Aula
from django.conf import settings
from utils.middleware import validar_roles, get_current_request
from django.http import HttpResponseRedirect
from utils.views import MyLoginRequiredMixin


#################################################
#####            CRUD DE AULA               #####
#################################################


class AulaListView(MyLoginRequiredMixin, ListView):
    model = Aula
    template_name = 'aula_list.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']
        if validar_roles(roles=roles):
            return super(AulaListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):

            context = super(AulaListView, self).get_context_data(**kwargs)

            request = get_current_request()

            if request.session.get('colegio'):
                id = request.session.get('colegio')
                context['idcolegio'] = id
            return context


class AulaDetailView(UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aula_detail.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']
        if validar_roles(roles=roles):
            return super(AulaDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class AulaCreationView(CreateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            return super(AulaCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_form.html'


class AulaDeleteView(DeleteView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(AulaDeleteView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

"""