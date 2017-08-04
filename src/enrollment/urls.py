from django.conf.urls import url
#from enrollment.views import CrearTipodeServicios
#from enrollment.views import ConfigurarIngresos
#from enrollment.views import CrearServicios
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

urlpatterns = [
    #url(r'^crearservicio$', CrearServicios.as_view(),name='crearservicio'),
    #url(r'^creartipodeservicio$', CrearTipodeServicios.as_view(),name='creartipodeservicio'),
    #url(r'^configuraringreso$', ConfigurarIngresos.as_view(),name='configuraringresos'),
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
]
