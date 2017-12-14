
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import UserInfoListView, SnippetDetail
from .serializers import CustomJWTSerializer
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [


    url(r'^verify_token/', verify_jwt_token),
    url(r'^login2/', obtain_jwt_token),
    #url(r'^login/$', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),
    #url(r'^login/$', CustomObtainJSONWebToken.as_view()),

    url(r'^colegio_api/$', views.ColegioList.as_view()),
    url(r'^colegio_api/(?P<pk>\d+)/$', views.ColegioDetail.as_view()),
    url(r'^perfil_api/$', views.PerfilList.as_view()),
    url(r'^perfil_api/(?P<pk>\d+)/$', views.PerfilDetail.as_view()),
####################
    url(r'^apoderado_api/$', views.ApoderadoList.as_view()),
    url(r'^apoderado_api/(?P<pk>\d+)/$', views.ApoderadoDetail.as_view()),
###################
    url(r'^alumno_api/$', views.AlumnoList.as_view()),
    url(r'^alumno_api/(?P<pk>\d+)/$', views.AlumnoDetail.as_view()),
###################
    url(r'^apoderadoalumno_api/$', views.ApoderadoAlumnoList.as_view()),
    url(r'^apoderadoalumno_api/(?P<pk>\d+)/$', views.ApoderadoAlumnoDetail.as_view()),
###################
    url(r'^matricula_api/$', views.MatriculaList.as_view()),
    url(r'^matricula_api/(?P<pk>\d+)/$', views.MatriculaDetail.as_view()),
###################

    # URL para el Web Service del Módulo Académico
    url(r'^asistencia_api/$', views.AsistenciaList.as_view()),
    url(r'^asistencia_api/(?P<pk>\d+)/$', views.AsistenciaDetail.as_view()),

    url(r'^aula_api/$', views.AulaList.as_view()),
    url(r'^aula_api/(?P<pk>\d+)/$', views.AulaDetail.as_view()),

    #url(r'^curso_docente_api/$', views.CursoDocenteList.as_view()),

    url(r'^alumno_api/$', views.AlumnoList.as_view()),
    url(r'^alumno_api/(?P<pk>\d+)/$', views.AlumnoDetail.as_view()),


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



    # Web Service para obtener las ALUMNOS asociados a un aula determinado
    url(r'^aula_alumnos_api/(?P<pk>[0-9]+)/(?P<aula>\w+)/$', views.AulaAlumnosList.as_view()),

    # Web Service para obtener las CURSOS a las que enseña un docente determinado
    url(r'^docente_curso_api/(?P<pk>[0-9]+)/(?P<docente>\w+)/$', views.DocenteCursoList.as_view()),

    # Web Service para obtener las AULAS a las que enseña un docente determinado
    url(r'^docente_aula_api/(?P<pk>[0-9]+)/(?P<docente>\w+)/$', views.DocenteAulaList.as_view()),

    # Web Service para visualizar las ASISTENCIAS POR MES de un aula determinada
    url(r'^aula_asistencia_api/(?P<pk>[0-9]+)/(?P<aula>\w+)/(?P<mes>\w+)/$', views.AulaAsistenciaList.as_view()),



    # webservice prueba
    url(r'^relacionusuarioperfil/(?P<pk>[0-9]+)/(?P<docente>\w+)/$', views.RelacionUsuarioPerfilView.as_view()),
    url(r'^relacionperfilalumno/(?P<pk>[0-9]+)/(?P<docente>\w+)/$', views.RelacionPerfilAlumnoView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)

