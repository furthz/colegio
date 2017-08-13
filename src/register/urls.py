from django.conf.urls import url

from register.views import CreatePersonaView, PersonaDetail
from . import views

urlpatterns = [
    # url(r'^person/create/$', CreatePersonaView.as_view(), name="persona_create"),
    url(r'^impdates/list/create/$',CreatePersonaView.as_view(), name="persona_create"),
    url(r'^impdates/list/(?P<pk>\d+)/$',PersonaDetail.as_view(), name='persona_detail'),

]