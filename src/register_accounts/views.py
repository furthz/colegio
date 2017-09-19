from authtools.models import User
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse_lazy
from .forms import RegistroUsuarioForm
from django.core.urlresolvers import reverse
from django.shortcuts import render

def index(request):
    return render(request, 'redir.html')



#################################################
#####          CRUD DE USUARIOS             #####
#################################################

class RegistroUsarioListView(ListView):
    model = User
    template_name = 'register_accounts/register_accounts_list.html'


class RegistroUsarioDetailView(DetailView):
    model = User
    template_name = 'register_accounts/register_accounts_detail.html'


class RegistroUsarioCreationView(CreateView):
    model = User
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = '/register_accounts/registe/'


class RegistroUsarioUpdateView(UpdateView):
    model = User
    template_name = "register_accounts/register_accounts_form.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('register_accounts:register_accounts_list')
