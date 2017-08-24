from django.conf.urls import url
from enrollment.views import TipoServicioRegularCreateView
from income.views import RegistrarPagoListView


urlpatterns = [
    # URL para tipos de servicios
    url(r'^register/$', RegistrarPagoListView.as_view(), name="register"),

]