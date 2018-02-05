from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from register.views import CreatePersonaView, PersonaDetail, AlumnoCreateView, AlumnoDetail, ApoderadoCreateView, \
    ApoderadoDetailView, PersonalDetailView, PersonalCreateView, PromotorCreateView, PromotorDetailView, \
    DirectorDetailView, DirectorCreateView, CajeroCreateView, CajeroDetailView, TesoreroCreateView, TesoreroDetailView, \
    ProveedorCreateView, ProveedorDetailView, PersonaListView, PersonaDetailView, ColegioCreateView, ColegioListView, \
    PersonalUpdateView, PersonalDeleteView, \
    SistemasCreateView, SistemasDetailView, ProveedorListView, ProveedorDeleteView, ProveedorUpdateView, \
    AlumnoAutocomplete, DocenteCreateView, DocenteDetailView, EmpresaCreateView, EmpresaListView, \
    ConfiguracionSistemaUpdateView, CorrelativoDocumentoCreateView, CorrelativoDocumentoListView, \
    CorrelativoDocumentoDetailView, CorrelativoDocumentoDeleteView, CorrelativoDocumentoUpdateView
from utils.views import get_provincias, get_distritos

from .import_export import exportCSV,exportJSON, simple_upload

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

    url(r'^promotores/create/$',PromotorCreateView.as_view(), name="promotor_create"),  #No agregar ---
    url(r'^promotores/(?P<pk>\d+)/$',PromotorDetailView.as_view(), name='promotor_detail'),

    url(r'^sistemas/create/$', SistemasCreateView.as_view(), name="sistemas_create"),
    url(r'^sistemas/(?P<pk>\d+)/$', SistemasDetailView.as_view(), name='sistemas_detail'),

    url(r'^directores/create/$',DirectorCreateView.as_view(), name="director_create"),
    url(r'^directores/(?P<pk>\d+)/$',DirectorDetailView.as_view(), name='director_detail'),

    url(r'^cajeros/create/$',CajeroCreateView.as_view(), name="cajero_create"),
    url(r'^cajeros/(?P<pk>\d+)/$',CajeroDetailView.as_view(), name='cajero_detail'),

    url(r'^tesoreros/create/$',TesoreroCreateView.as_view(), name="tesorero_create"),
    url(r'^tesoreros/(?P<pk>\d+)/$',TesoreroDetailView.as_view(), name='tesorero_detail'),

    url(r'^docentes/create/$', DocenteCreateView.as_view(), name="docente_create"),
    url(r'^docentes/(?P<pk>\d+)/$', DocenteDetailView.as_view(), name='docente_detail'),

    url(r'^proveedores/create/$',ProveedorCreateView.as_view(), name="proveedor_create"),
    url(r'^proveedores/(?P<pk>\d+)/$',ProveedorDetailView.as_view(), name='proveedor_detail'),
    url(r'^proveedores/list/$', ProveedorListView.as_view(), name="proveedor_list"),
    url(r'^proveedores/delete', ProveedorDeleteView.as_view(), name="proveedor_delete"),
    url(r'^proveedores/update/(?P<pk>\d+)/$', ProveedorUpdateView.as_view(), name="proveedor_update"),

    url(r'^list/$', PersonaListView.as_view(), name="personal_list"),
    url(r'^registers/(?P<pk>\d+)/$',PersonaDetailView.as_view(), name='personal_detail'),
    url(r'^registers/update/(?P<pk>\d+)/$', PersonalUpdateView.as_view(), name="personal_update"),
    url(r'^registers/delete', PersonalDeleteView.as_view(), name="personal_delete"),

    url(r'^colegios/create/$', ColegioCreateView.as_view(), name="colegio_create"),
    url(r'^colegios/$', ColegioListView.as_view(), name="colegio_list"),

    url(r'^alumno/autocomplete/$', AlumnoAutocomplete.as_view(), name='alumno_autocomplete'),

    url(r'^api/get_provincias/', get_provincias, name='get_provincias'),
    url(r'^api/get_distritos/', get_distritos, name='get_distritos'),

    url(r'^exportCSV/', exportCSV, name='export'),
    url(r'^exportJSON/', exportJSON, name='export'),
    url(r'^import/', simple_upload, name='import'),

    url(r'^empresas/create/$', EmpresaCreateView.as_view(), name="empresa_create"),
    url(r'^empresas/$', EmpresaListView.as_view(), name="empresa_list"),
    url(r'^empresas/configuracion/update/(?P<pk>\d+)/$', ConfiguracionSistemaUpdateView.as_view(), name="configuracionsistema_update"),

    url(r'^configuracion/correlativo/create/$', CorrelativoDocumentoCreateView.as_view(), name="correlativodocumento_create"),
    url(r'^configuracion/correlativo/list/$', CorrelativoDocumentoListView.as_view(), name="correlativodocumento_list"),
    url(r'^configuracion/correlativo/list/(?P<pk>\d+)/$',CorrelativoDocumentoDetailView.as_view(), name='documento_detail'),
    url(r'^configuracion/correlativo/list/delete/$',CorrelativoDocumentoDeleteView.as_view(), name='documento_delete'),
    url(r'^configuracion/correlativo/list/update/(?P<pk>\d+)/$',CorrelativoDocumentoUpdateView.as_view(), name='documento_update'),

]