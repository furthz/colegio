from django.conf.urls import url
from.views import (
#Alumno
    RegistroUsarioListView,
    RegistroUsarioDetailView,
    RegistroUsarioCreationView,
    RegistroUsarioUpdateView,
    index

)

urlpatterns = [

    url(r'^register/$', RegistroUsarioListView.as_view(), name='register_accounts_list'),
    url(r'^register/(?P<pk>\d+)$', RegistroUsarioDetailView.as_view(), name='register_accounts_detail'),
    url(r'^register/create$', RegistroUsarioCreationView.as_view(), name='register_accounts_create'),
    url(r'^register/update/(?P<pk>\d+)$', RegistroUsarioUpdateView.as_view(), name='register_accounts_edit'),

    url(r'^registe/$', index),

]

