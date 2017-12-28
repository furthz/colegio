
from django.conf.urls import url, include
from .views import *


urlpatterns = [

    url(r'^alerta_tabla/$', AlertaListView.as_view(), name='consignment_list'),
    url(r'^alerta_tabla/create$', AlertaCreationView.as_view(), name='consignment_create'),


]


