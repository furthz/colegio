
from django.conf.urls import url

from AE_academico.views import AulaListView, AulaDetailView, AulaCreationView, AulaUpdateView, AulaDeleteView, \
    MarcarAsistenciaView, SubirNotasView, CursoListView, CursoDetailView, CursoCreationView, CursoUpdateView, \
    CursoDeleteView
from AE_academico.views import CursoDocenteCreateView
urlpatterns = [

    # URL's del CRUD de Aula
    url(r'^aula/$', AulaListView.as_view(), name='aula_list'),
    url(r'^aula/(?P<pk>\d+)$', AulaDetailView.as_view(), name='aula_detail'),
    url(r'^aula/create$', AulaCreationView.as_view(), name='aula_create'),
    url(r'^aula/update/(?P<pk>\d+)$', AulaUpdateView.as_view(), name='aula_edit'),
    url(r'^aula/delete/(?P<pk>\d+)$', AulaDeleteView.as_view(), name='aula_delete'),

    # URL's del CRUD de Curso
    url(r'^curso/$', CursoListView.as_view(), name='curso_list'),
    url(r'^curso/(?P<pk>\d+)$', CursoDetailView.as_view(), name='curso_detail'),
    url(r'^curso/create$', CursoCreationView.as_view(), name='curso_create'),
    url(r'^curso/update/(?P<pk>\d+)$', CursoUpdateView.as_view(), name='curso_edit'),
    url(r'^curso/delete/(?P<pk>\d+)$', CursoDeleteView.as_view(), name='curso_delete'),

    # URL's de relación Curso Docente
    url(r'^curso/create/$', CursoDocenteCreateView.as_view(), name='cursodocente_create'),

    # URL's de registro de asistencia
    url(r'^asistencia/create/$', MarcarAsistenciaView.as_view(), name='asistencia_create'),

    # URL's de la asignación de notas
    url(r'^notas/create/$', SubirNotasView.as_view(), name='notas_create'),
]
