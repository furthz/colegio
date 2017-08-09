from django.conf.urls import url
from enrollment.views import TipoServicioCreate
from enrollment.views import TipoServicioUpdate
from enrollment.views import TipoServicioDetail
from enrollment.views import TipoServicioDelete
from enrollment.views import TipoServicioList
from enrollment.views import ServicioList
from enrollment.views import ServicioCreate
from enrollment.views import ServicioDelete
from enrollment.views import ServicioUpdate
from enrollment.views import ServicioDetail
from enrollment.views import MatriculaCreate
from enrollment.views import MatriculaCreate2
from enrollment.views import MatriculaDelete
from enrollment.views import MatriculaDetail
from enrollment.views import MatriculaList
from enrollment.views import MatriculaUpdate
from enrollment.views import AlumnoCreate

urlpatterns = [
    url(r'^impdates/list/create/$',TipoServicioCreate.as_view(), name="tiposervicio_create"),
    url(r'^impdates/list/(?P<pk>\d+)/$',TipoServicioDetail.as_view(), name='tiposervicio_detail'),
    url(r'^impdates/list/(?P<pk>\d+)/update/$',TipoServicioUpdate.as_view(), name="tiposervicio_update"),
    url(r'^impdates/list/(?P<pk>\d+)/delete/$',TipoServicioDelete.as_view(), name="tiposervicio_delete"),
    url(r'^impdates/list/$', TipoServicioList.as_view(), name="tiposervicio_list"),
    url(r'^impdates/list/(?P<pkts>\d+)/listservicios/create/$',ServicioCreate.as_view(), name="servicio_create"),
    url(r'^impdates/list/(?P<pkts>\d+)/listservicios/(?P<pk>\d+)/$',ServicioDetail.as_view(), name='servicio_detail'),
    url(r'^impdates/list/(?P<pkts>\d+)/listservicios/(?P<pk>\d+)/update/$',ServicioUpdate.as_view(), name="servicio_update"),
    url(r'^impdates/list/(?P<pkts>\d+)/listservicios/(?P<pk>\d+)/delete/$',ServicioDelete.as_view(), name="servicio_delete"),
    url(r'^impdates/list/(?P<pkts>\d+)/listservicios/$', ServicioList.as_view(), name="servicio_list"),
    url(r'^matricula/list/create/$', MatriculaCreate.as_view(), name="matricula_create"),
    url(r'^matricula/list/create/(?P<pk>\d+)/$', MatriculaCreate2.as_view(), name="matricula_create2"),
    url(r'^matricula/list/(?P<pk>\d+)/$', MatriculaDetail.as_view(), name='matricula_detail'),
    url(r'^matricula/list/(?P<pk>\d+)/update/$', MatriculaUpdate.as_view(), name="matricula_update"),
    url(r'^matricula/list/(?P<pk>\d+)/delete/$', MatriculaDelete.as_view(), name="matricula_delete"),
    url(r'^matricula/list/$', MatriculaList.as_view(), name="matricula_list"),
    url(r'^persona/list/create/$', AlumnoCreate.as_view(), name="alumno_create"),
]
