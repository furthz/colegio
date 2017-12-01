
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import UserInfoListView, SnippetDetail

urlpatterns = [


    url(r'^colegio_api/$', views.ColegioList.as_view()),
    url(r'^colegio_api/(?P<pk>\d+)/$', views.ColegioDetail.as_view()),
    url(r'^perfil_api/$', views.PerfilList.as_view()),
    url(r'^perfil_api/(?P<pk>\d+)/$', views.PerfilDetail.as_view()),


    # URL para el Web Service del Módulo Académico
    url(r'^asistencia_api/$', views.AsistenciaList.as_view()),
    url(r'^asistencia_api/(?P<pk>\d+)/$', views.AsistenciaDetail.as_view()),

    url(r'^aula_api/$', views.AulaList.as_view()),
    url(r'^aula_api/(?P<pk>\d+)/$', views.AulaDetail.as_view()),

    #url(r'^curso_docente_api/$', views.CursoDocenteList.as_view()),


    url(r'^matricula_api/$', views.MatriculaList.as_view()),
    url(r'^matricula_api/(?P<pk>\d+)/$', views.MatriculaDetail.as_view()),

    url(r'^alumno_api/$', views.AlumnoList.as_view()),
    url(r'^alumno_api/(?P<pk>\d+)/$', views.AlumnoDetail.as_view()),

    url(r'^user_info/$', UserInfoListView.as_view(), name='user_info'),


    url(r'^colegio/(?P<pk>[0-9]+)/(?P<nombre>\w+)/$', SnippetDetail.as_view()),

    url(r'^curso_docente_api/(?P<pk>[0-9]+)/(?P<docente>\w+)/$', views.CursoDocenteList.as_view()),

    url(r'^aula_curso_api/(?P<pk>[0-9]+)/(?P<docente>\w+)/$', views.AulaCursoList.as_view()),

    url(r'^aula_docente_api/(?P<pk>[0-9]+)/(?P<docente>\w+)/$', views.AulaDocenteList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
