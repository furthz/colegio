from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import UserInfoListView
urlpatterns = [


    url(r'^colegio_api/$', views.ColegioList.as_view()),
    url(r'^colegio_api/(?P<pk>\d+)/$', views.ColegioDetail.as_view()),
    url(r'^perfil_api/$', views.PerfilList.as_view()),
    url(r'^perfil_api/(?P<pk>\d+)/$', views.PerfilDetail.as_view()),


    # URL para el Web Service del Módulo Académico
    url(r'^asistencia_api/$', views.AsistenciaList.as_view()),
    url(r'^asistencia_api/(?P<pk>\d+)/$', views.AsistenciaDetail.as_view()),



    url(r'^user_info/$', UserInfoListView.as_view(), name='user_info'),

]

urlpatterns = format_suffix_patterns(urlpatterns)