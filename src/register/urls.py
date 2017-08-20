from django.conf.urls import url

from register.views import CreatePersonaView, PersonaDetail, AlumnoCreateView, AlumnoDetail, ApoderadoCreateView, \
    ApoderadoDetailView
from . import views

urlpatterns = [
    # url(r'^person/create/$', CreatePersonaView.as_view(), name="persona_create"),
    url(r'^personas/create/$',CreatePersonaView.as_view(), name="persona_create"),
    url(r'^personas/(?P<pk>\d+)/$',PersonaDetail.as_view(), name='persona_detail'),

    url(r'^alumnos/create/$',AlumnoCreateView.as_view(), name="alumno_create"),
    url(r'^alumnos/(?P<pk>\d+)/$',AlumnoDetail.as_view(), name='alumno_detail'),

    url(r'^apoderados/create/$',ApoderadoCreateView.as_view(), name="apoderado_create"),
    url(r'^apoderados/(?P<pk>\d+)/$',ApoderadoDetailView.as_view(), name='apoderado_detail'),


]