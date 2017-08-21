from django.conf.urls import url
from enrollment.views import TipoServicioRegularCreateView
from enrollment.views import TipoServicioExtraCreateView
from enrollment.views import CargarTipoServicioCreateView
from enrollment.views import TipoServicioRegularEndUpdateView
from enrollment.views import TipoServicioExtraEndUpdateView
from enrollment.views import TipoServicioRegularUpdateView
from enrollment.views import TipoServicioExtraUpdateView
from enrollment.views import TipoServicioDetailView
from enrollment.views import TipoServicioDeleteView
from enrollment.views import TipoServicioListView

from enrollment.views import ServicioListView
from enrollment.views import ServicioRegularCreateView
from enrollment.views import ServicioExtraCreateView
from enrollment.views import ServicioDeleteView
from enrollment.views import ServicioUpdateView
from enrollment.views import ServicioDetailView

from enrollment.views import MatriculaCreateView
from enrollment.views import MatriculaDeleteView
from enrollment.views import MatriculaDetailView
from enrollment.views import MatriculaListView
from enrollment.views import MatriculaUpdateView
from enrollment.views import FiltrarAlumnoView
from enrollment.views import CargarMatriculaCreateView
from enrollment.views import CargarMatriculaUpdateView
#
from enrollment.views import testform
from enrollment.views import testpersonaform
from enrollment.views import AuthorCreate

urlpatterns = [
    # URL para tipos de servicios
    url(r'^typeservice/create/$', CargarTipoServicioCreateView.as_view(), name="tiposervicio_create"),
    url(r'^typeservice/create/end1/$', TipoServicioRegularCreateView.as_view(), name="tiposervicio_create_regular"),
    url(r'^typeservice/create/end2/$', TipoServicioExtraCreateView.as_view(), name="tiposervicio_create_extra"),
    url(r'^typeservice/detail/(?P<pk>\d+)/$', TipoServicioDetailView.as_view(), name='tiposervicio_detail'),
    url(r'^typeservice/update/end1/(?P<pk>\d+)/$', TipoServicioRegularEndUpdateView.as_view(), name="tiposervicioregularend_update"),
    url(r'^typeservice/update/end2/(?P<pk>\d+)/$', TipoServicioExtraEndUpdateView.as_view(), name="tiposervicioextraend_update"),
    url(r'^typeservice/update/regular', TipoServicioRegularUpdateView.as_view(), name="tiposervicioregular_update"),
    url(r'^typeservice/update/extra', TipoServicioExtraUpdateView.as_view(), name="tiposervicioextra_update"),
    url(r'^typeservice/delete', TipoServicioDeleteView.as_view(), name="tiposervicio_delete"),
    url(r'^typeservice/$', TipoServicioListView.as_view(), name="tiposervicio_list"),

    # URL para servicios
    url(r'^service/create/regular/$', ServicioRegularCreateView.as_view(), name="servicioregular_create"),
    url(r'^service/create/extra/$', ServicioExtraCreateView.as_view(), name="servicioextra_create"),
    url(r'^service/detail/(?P<pk>\d+)/$', ServicioDetailView.as_view(), name='servicio_detail'),
    url(r'^service/update/$', ServicioUpdateView.as_view(), name="servicio_update"),
    url(r'^service/delete/$', ServicioDeleteView.as_view(), name="servicio_delete"),
    url(r'^service/$', ServicioListView.as_view(), name="servicio_list"),

    # URL para matricula
    url(r'^create/end/$', MatriculaCreateView.as_view(), name="matricula_create_end"),
    url(r'^create', CargarMatriculaCreateView.as_view(), name="matricula_create"),
    url(r'^detail/(?P<pk>\d+)/$', MatriculaDetailView.as_view(), name='matricula_detail'),
    url(r'^update/end', MatriculaUpdateView.as_view(), name="matricula_update_end"),
    url(r'^update', CargarMatriculaUpdateView.as_view(), name="matricula_update"),
    url(r'^delete/$', MatriculaDeleteView.as_view(), name="matricula_delete"),
    url(r'^list/$', MatriculaListView.as_view(), name="matricula_list"),

    # URL para filtrar y crear matriculas
    url(r'^filter', FiltrarAlumnoView.as_view(), name="filtrar_alumno"),

    url(r'^test', AuthorCreate.as_view(), name="test"),
    url(r'^persona', testpersonaform.as_view(), name="test_persona"),
]