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
from .forms import CashierForm, BoxCashierForm, ConsignmentForm, CajaChicaConsignmentForm
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

from utils.middleware import get_current_user, get_current_colegio
from register.models import PersonalColegio, Personal, Profile

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
            roles = ['administrativo', 'tesorero']
            context['es_tesorero'] = validar_roles(roles = roles)

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

            roles = ['cajero']
            context['es_cajero'] = validar_roles(roles=roles)
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


    #Paso el ID del usuario al template y en el template selecciono la opción con ese ID del usuario que crea

    def get_context_data(self, **kwargs):
            context = super(BoxCashierCreationView, self).get_context_data(**kwargs)

            usuario = get_current_user()
            if usuario is not None:
                iduser = usuario.id
            else:
                iduser = -1

            a = Profile.objects.get(user_id=iduser)
            b = Personal.objects.get(persona=a)
#            c = PersonalColegio.objects.get(personal_id=b)
#           d = PersonalColegio.objects.filter(personal_id=b).values('pk')
#            print(PersonalColegio.objects.values('pk').filter(personal_id=b)[0]['pk'])

#            print(Caja.objects.filter(colegio_id=1))
            # creacion
            #context['yolencios'] = d
#            print(PersonalColegio.objects.values('pk').filter(personal_id=b)[0]['pk'])
            personal_colegio = PersonalColegio.objects.get(personal=b)
            context['yolencios'] = personal_colegio.id_personal_colegio
            return context

    @method_decorator(permission_required('cash.Box_Cashier_Creation', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['cajero']


        if validar_roles(roles=roles):
            usuario = get_current_user()
            perfil = Profile.objects.get(user=usuario)
            personal = Personal.objects.filter(persona=perfil)
            personal_colegio = PersonalColegio.objects.get(personal=personal)
            cajas = Caja.objects.filter(colegio__id_colegio= get_current_colegio(), activo=True)

            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'cajas': cajas,
                'yolencios': personal_colegio.id_personal_colegio
            })


        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.estado = True
        obj.save()
        return super(BoxCashierCreationView, self).form_valid(form)


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

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.estado = False
        obj.save()
        return super(BoxCashierUpdateView, self).form_valid(form)



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
            Remesa.objects.filter(movimiento__caja__colegio_id=get_current_colegio())
            return super(ConsignmentListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):
            context = super(CashierListView, self).get_context_data(**kwargs)
            roles = ['cajero']
            context['es_cajero'] = validar_roles(roles = roles)
            return context

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
            try:
                usuario = get_current_user()
                mov = CajaCajero.objects.get(estado=True, usuario_modificacion= str(usuario.id))
                alerta = False
            except:
                alerta = True
            personal = PersonalColegio.objects.filter(colegio=get_current_colegio(), activo=True)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'personal': personal,
                'alerta': alerta,
            })
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



class RecargarCajaChicaView(CreateView):
    model = Remesa
    form_class = CajaChicaConsignmentForm
    success_url = reverse_lazy('cash:consignment_list')
    template_name = 'consignment/consignment_form_cajachica.html'

    @method_decorator(permission_required('cash.Consigment_Creation', login_url=settings.REDIRECT_PERMISOS,
                                          raise_exception=False))
    def get(self, request, *args, **kwargs):
        roles = ['cajero']

        if validar_roles(roles=roles):
            persona = Profile.objects.get(user=get_current_user())
            personal = Personal.objects.get(persona=persona)
            personal = PersonalColegio.objects.filter(personal=personal,colegio=get_current_colegio(), activo=True)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'personal': personal,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
