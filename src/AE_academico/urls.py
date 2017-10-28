from django.conf.urls import url
from AE_academico.views import AulaListView, AulaDetailView, AulaCreationView, AulaUpdateView, AulaDeleteView, \
    MarcarAsistenciaView, SubirNotasView, CursoListView, CursoDetailView, CursoCreationView, CursoUpdateView, \
    CursoDeleteView, AulaCursoCreateView, VisualizarAsistenciaView, EventoCreateView, EventoDetailView, EventoListView, \
    MarcarAsistenciaDiaView, PeriodoAcademicoListView, PeriodoAcademicoDetailView, PeriodoAcademicoCreationView, \
    PeriodoAcademicoUpdateView
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

    # URL's de relación Aula Curso
    #url(r'^aula/curso/create/$', AulaCursoCreateView.as_view(), name='aulacurso_create'),

    # URL's de relación Curso Docente
    url(r'^curso/docente/create/$', CursoDocenteCreateView.as_view(), name='cursodocente_create'),

    # URL's de registro de asistencia
    url(r'^asistencia/registrar/$', MarcarAsistenciaView.as_view(), name='asistencia_registrar'),
    url(r'^asistencia/registrar/dia/$', MarcarAsistenciaDiaView.as_view(), name='asistencia_registrar_dia'),
    url(r'^asistencia/ver/$', VisualizarAsistenciaView.as_view(), name='asistencia_ver'),


    # URL's de la asignación de notas
    url(r'^notas/registrar/$', SubirNotasView.as_view(), name='notas_registrar'),
    #url(r'^asistencia/ver/$', VisualizarAsistenciaView.as_view(), name='asistencia_ver'),

    url(r'^aula/curso/create/$', AulaCursoCreateView.as_view(), name='aulacurso_create'),

    # URL para creacion de evento
    url(r'^evento/create/$', EventoCreateView.as_view(), name='evento_create'),
    url(r'^evento/list/$', EventoListView.as_view(), name='evento_list'),
    url(r'^evento/detail/$', EventoDetailView.as_view(), name='evento_detail'),

    # URL's del CRUD de Periodo Academico
    url(r'^periodo/$', PeriodoAcademicoListView.as_view(), name='periodo_list'),
    url(r'^periodo/(?P<pk>\d+)$', PeriodoAcademicoDetailView.as_view(), name='periodo_detail'),
    url(r'^periodo/create$', PeriodoAcademicoCreationView.as_view(), name='periodo_create'),
    url(r'^periodo/update/(?P<pk>\d+)$', PeriodoAcademicoUpdateView.as_view(), name='periodo_edit'),

]
