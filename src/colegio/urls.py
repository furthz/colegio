from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import profiles.urls
import accounts.urls
import enrollment.urls
import register.urls
import income.urls
import cash.urls
import payments.urls
from . import views

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^users/', include(profiles.urls, namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(accounts.urls, namespace='accounts')),
    url(r'^enrollments/', include(enrollment.urls, namespace='enrollments')),
    url(r'^registers/', include(register.urls, namespace='registers')),
    url(r'^cash/', include(cash.urls, namespace='cash')),
    url(r'^income/', include(income.urls, namespace='income')),
    url(r'^payments/', include(payments.urls, namespace='payments')),
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
