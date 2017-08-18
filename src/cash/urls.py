from django.conf.urls import url
from .views import (
    RemesaListView,
    RemesaDetailView,
    RemesaCreationView,
    RemesaUpdateView,
    RemesaDeleteView
)

urlpatterns = [

    url(r'^remesa/$', RemesaListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', RemesaDetailView.as_view(), name='detail'),
    url(r'^nuevo$', RemesaCreationView.as_view(), name='new'),
    url(r'^editar/(?P<pk>\d+)$', RemesaUpdateView.as_view(), name='edit'),
    url(r'^borrar/(?P<pk>\d+)$', RemesaDeleteView.as_view(), name='delete'),
]
