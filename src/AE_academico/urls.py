"""
from django.conf.urls import url

from AE_academico.views import AulaListView, AulaDetailView, AulaCreationView, AulaUpdateView, AulaDeleteView, \
    MarcarAsistenciaView, SubirNotasView
from AE_academico.views import CursoDocenteCreateView
urlpatterns = [

    # URL's del CRUD de AULA
    url(r'^aula/$', AulaListView.as_view(), name='aula_list'),
    url(r'^aula/(?P<pk>\d+)$', AulaDetailView.as_view(), name='aula_detail'),
    url(r'^aula/create$', AulaCreationView.as_view(), name='aula_create'),
    url(r'^aula/update/(?P<pk>\d+)$', AulaUpdateView.as_view(), name='aula_edit'),
    url(r'^aula/delete/(?P<pk>\d+)$', AulaDeleteView.as_view(), name='aula_delete'),

    url(r'^curso/create/$', CursoDocenteCreateView.as_view(), name='cursodocente_create'),

    url(r'^asistencia/create/$', MarcarAsistenciaView.as_view(), name='asistencia_create'),

    url(r'^notas/create/$', SubirNotasView.as_view(), name='notas_create'),
]
"""