from django.conf.urls import url, include
from rest_framework import routers

from . import views

from .views import (
    # Registro de Usuarios
    RegistroUsarioListView,
    RegistroUsarioDetailView,
    RegistroUsarioUpdateView,

    # Sistemas, Director, Cajero, Tesorero
    RegistroUsarioCreationViewSistema,
    RegistroUsarioCreationViewDirector,
    RegistroUsarioCreationViewCajero,
    RegistroUsarioCreationViewTesorero,

    RegistroUsuario, RegistroUsuarioApoderado, RegistroUsarioCreationViewApoderado)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [

    url(r'^error_usuario_sin_perfil/$', views.UsuarioSinPerfil),

    url(r'^api', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^rest-auth/', include('rest_auth.urls')),

    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^me$', views.AsignColegioView.as_view(), name='tocolegio_self'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^password-change/$', views.PasswordChangeView.as_view(),
        name='password-change'),
    url(r'^password-reset/$', views.PasswordResetView.as_view(),
        name='password-reset'),
    url(r'^password-reset-done/$', views.PasswordResetDoneView.as_view(),
        name='password-reset-done'),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$$',
        views.PasswordResetConfirmView.as_view(),  # NOQA
        name='password-reset-confirm'),

    # Registro de Usuarios
    url(r'^register/$', RegistroUsarioListView.as_view(), name='register_accounts_list'),
    url(r'^register/(?P<pk>\d+)$', RegistroUsarioDetailView.as_view(), name='register_accounts_detail'),
    url(r'^register/update/(?P<pk>\d+)$', RegistroUsarioUpdateView.as_view(), name='register_accounts_edit'),

    # Sistemas, Director, Cajero, Tesorero
    url(r'^register/createSistema$', RegistroUsarioCreationViewSistema.as_view(),
        name='register_accounts_createSistema'),
    url(r'^register/createDirector$', RegistroUsarioCreationViewDirector.as_view(),
        name='register_accounts_createDirector'),
    url(r'^register/createCajero$', RegistroUsarioCreationViewCajero.as_view(), name='register_accounts_createCajero'),
    url(r'^register/createTesorero$', RegistroUsarioCreationViewTesorero.as_view(),
        name='register_accounts_createTesorero'),

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Registers
    url(r'^register/create$', RegistroUsuario.as_view(), name='register_create'),
    url(r'^register/create2$', RegistroUsuarioApoderado.as_view(), name='register_apoderado_create'),
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    url(r'^register/createApoderado$', RegistroUsarioCreationViewApoderado.as_view(),
        name='register_accounts_createApoderado'),
]
