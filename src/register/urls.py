from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from register.views import CreatePersonaView, PersonaDetail, AlumnoCreateView, AlumnoDetail, ApoderadoCreateView, \
    ApoderadoDetailView, PersonalDetailView, PersonalCreateView, PromotorCreateView, PromotorDetailView, \
    DirectorDetailView, DirectorCreateView, CajeroCreateView, CajeroDetailView, TesoreroCreateView, TesoreroDetailView, \
    ProveedorCreateView, ProveedorDetailView, PersonaListView, PersonaDetailView
from . import views

urlpatterns = [
    # url(r'^person/create/$', CreatePersonaView.as_view(), name="persona_create"),
    url(r'^personas/create/$',CreatePersonaView.as_view(), name="persona_create"),
    url(r'^personas/(?P<pk>\d+)/$',PersonaDetail.as_view(), name='persona_detail'),

    url(r'^alumnos/create/$',AlumnoCreateView.as_view(), name="alumno_create"),
    url(r'^alumnos/(?P<pk>\d+)/$',AlumnoDetail.as_view(), name='alumno_detail'),

    url(r'^apoderados/create/$',ApoderadoCreateView.as_view(), name="apoderado_create"),
    url(r'^apoderados/(?P<pk>\d+)/$',ApoderadoDetailView.as_view(), name='apoderado_detail'),

    #url(r'^personales/create/$',PersonalCreateView.as_view(), name="personal_create"),
    #url(r'^personales/(?P<pk>\d+)/$',PersonalDetailView.as_view(), name='personal_detail'),

    url(r'^promotores/create/$',PromotorCreateView.as_view(), name="promotor_create"),
    url(r'^promotores/(?P<pk>\d+)/$',PromotorDetailView.as_view(), name='promotor_detail'),

    url(r'^directores/create/$',DirectorCreateView.as_view(), name="director_create"),
    url(r'^directores/(?P<pk>\d+)/$',DirectorDetailView.as_view(), name='director_detail'),

    url(r'^cajeros/create/$',CajeroCreateView.as_view(), name="cajero_create"),
    url(r'^cajeros/(?P<pk>\d+)/$',CajeroDetailView.as_view(), name='cajero_detail'),

    url(r'^tesoreros/create/$',TesoreroCreateView.as_view(), name="tesorero_create"),
    url(r'^tesoreros/(?P<pk>\d+)/$',TesoreroDetailView.as_view(), name='tesorero_detail'),

    url(r'^proveedores/create/$',ProveedorCreateView.as_view(), name="proveedor_create"),
    url(r'^proveedores/(?P<pk>\d+)/$',ProveedorDetailView.as_view(), name='proveedor_detail'),

    url(r'^list/$', PersonaListView.as_view(), name="personal_list"),
    url(r'^registers/(?P<pk>\d+)/$',PersonaDetailView.as_view(), name='personal_detail'),

]