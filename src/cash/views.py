from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Caja, CajaCajero, Remesa
from .forms import CashierForm, BoxCashierForm, ConsignmentForm
from .filters import ConsignmentFilter
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.conf import settings
from utils.middleware import validar_roles
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.db import models
from profiles.models import BaseProfile as Profile

from utils.middleware import get_current_request


from utils.views import MyLoginRequiredMixin



def index(request):
    return render(request, 'cash/index.html')


#################################################
#####          CRUD DE CAJA                 #####
#################################################

class CashierListView(MyLoginRequiredMixin, ListView):
    model = Caja
    template_name = 'cashier/cashier_list.html'

    @method_decorator(permission_required('cash.Cashier_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']

        if validar_roles(roles=roles):

            return super(CashierListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):
            context = super(CashierListView, self).get_context_data(**kwargs)


            request = get_current_request()

            if request.session.get('colegio'):
                id = request.session.get('colegio')
                context['idcolegio'] = id
            return context
"""
class CashierDetailView(DetailView):
    template_name = 'cashier/cashier_detail.html'
    model = Caja
"""

class CashierDetailView(UpdateView):
    model = Caja
    form_class = CashierForm
    template_name = 'cashier/cashier_detail.html'

    @method_decorator(permission_required('cash.Cashier_Detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']

        if validar_roles(roles=roles):
            return super(CashierDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class CashierCreationView(CreateView):
    model = Caja
    form_class = CashierForm
    success_url = reverse_lazy('cash:cashier_list')
    template_name = 'cashier/cashier_form.html'

    @method_decorator(permission_required('cash.Cashier_Creation', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']

        if validar_roles(roles=roles):
            return super(CashierCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class CashierUpdateView(UpdateView):
    model = Caja
    form_class = CashierForm
    success_url = reverse_lazy('cash:cashier_list')
    template_name = 'cashier/cashier_form.html'
    # fields = ['id_remesa', 'id_persona', 'id_movimiento', 'fechacreacion', 'monto', 'comentario']

"""

class CashierDeleteView(DeleteView):
    model = Caja
    success_url = reverse_lazy('cash:cashier_list')
    template_name = 'cashier/cashier_confirm_delete.html'
"""

class CashierDeleteView(UpdateView):
    model = Caja
    form_class = CashierForm
    success_url = reverse_lazy('cash:cashier_list')
    template_name = 'cashier/cashier_confirm_delete.html'

    @method_decorator(permission_required('cash.Cashier_Delete', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']

        if validar_roles(roles=roles):
            return super(CashierDeleteView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)





#################################################
#####          CRUD DE CAJACAJERO           #####
#################################################

class BoxCashierListView(ListView):
    model = CajaCajero
    template_name = 'boxcashier/boxcashier_list.html'

    @method_decorator(permission_required('cash.Box_Cashier_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']

        if validar_roles(roles=roles):
            return super(BoxCashierListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):
            context = super(BoxCashierListView, self).get_context_data(**kwargs)


            request = get_current_request()

            if request.session.get('colegio'):
                id = request.session.get('colegio')
                context['idcolegio'] = id
            return context


class BoxCashierDetailView(DetailView):
    model = CajaCajero
    template_name = 'boxcashier/boxcashier_detail.html'

    @method_decorator(permission_required('cash.Box_Cashier_Detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']

        if validar_roles(roles=roles):
            return super(BoxCashierDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class BoxCashierCreationView(CreateView):
    model = CajaCajero
    form_class = BoxCashierForm
    success_url = reverse_lazy('cash:boxcashier_list')
    template_name = 'boxcashier/boxcashier_formApertura.html'


    @method_decorator(permission_required('cash.Box_Cashier_Creation', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['cajero']

        if validar_roles(roles=roles):
            return super(BoxCashierCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class BoxCashierUpdateView(UpdateView):
    model = CajaCajero
    form_class = BoxCashierForm
    success_url = reverse_lazy('cash:boxcashier_list')
    template_name = 'boxcashier/boxcashier_formCierre.html'
    # fields = ['id_remesa', 'id_persona', 'id_movimiento', 'fechacreacion', 'monto', 'comentario']

    @method_decorator(permission_required('cash.Box_Cashier_Update', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['cajero']

        if validar_roles(roles=roles):
            return super(BoxCashierUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class BoxCashierDeleteView(DeleteView):
    model = CajaCajero
    success_url = reverse_lazy('cash:boxcashier_list')
    template_name = 'boxcashier/boxcashier_confirm_delete.html'


#################################################
#####          CRUD DE REMESAS              #####
#################################################

class ConsignmentListView(ListView):
    model = Remesa
    filterset_class = ConsignmentFilter
    template_name = 'consignment/consignment_list.html'

    @method_decorator(permission_required('cash.Consigment_List', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']

        if validar_roles(roles=roles):
            return super(ConsignmentListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class ConsignmentDetailView(DetailView):
    model = Remesa
    template_name = 'consignment/consignment_detail.html'

    @method_decorator(permission_required('cash.Consigment_Detail', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']

        if validar_roles(roles=roles):
            return super(ConsignmentDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class ConsignmentCreationView(CreateView):
    model = Remesa
    form_class = ConsignmentForm
    success_url = reverse_lazy('cash:consignment_list')
    template_name = 'consignment/consignment_form.html'

    @method_decorator(permission_required('cash.Consigment_Creation', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['cajero']

        if validar_roles(roles=roles):
            return super(ConsignmentCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
"""
    def post(self, request, *args, **kwargs):

        a = request.POST.get('personal_colegio')
        print(a)
        #print(Profile.objects.all())
        print(Profile.objects.get(pk=a))

        #print(User.objects.get(pk=a))
        #print(User.objects.select_related('profile').get(id=a))

        return render(request, template_name=self.template_name)
"""
"""
        profile = User.objects.filter(pk=a)
        for prof in profile:

            print(profile.email)
"""





class ConsignmentUpdateView(UpdateView):
    model = Remesa
    form_class = ConsignmentForm
    success_url = reverse_lazy('cash:consignment_list')
    template_name = 'consignment/consignment_form.html'
    # fields = ['id_remesa', 'id_persona', 'id_movimiento', 'fechacreacion', 'monto', 'comentario']


class ConsignmentDeleteView(DeleteView):
    model = Remesa
    success_url = reverse_lazy('cash:consignment_list')
    template_name = 'consignment/consignment_confirm_delete.html'


#################################################
#####          FILTRADO                     #####
#################################################

def search(request):
    comentario_list = Remesa.objects.all()
    comentario_filter = ConsignmentFilter(request.GET, queryset=comentario_list)
    return render(request, 'consignment/consignment_list.html', {'filter': comentario_filter})