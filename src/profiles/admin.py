from __future__ import unicode_literals
from django.contrib import admin
from authtools.admin import NamedUserAdmin
from .models import Profile, TokenFirebase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from import_export.admin import ImportExportModelAdmin
from import_export import resources


User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = Profile
    #model = Persona



class NewUserAdmin(NamedUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('is_active', 'email', 'name', 'permalink',
                    'is_superuser', 'is_staff',)

    # 'View on site' didn't work since the original User model needs to
    # have get_absolute_url defined. So showing on the list display
    # was a workaround.
    def permalink(self, obj):
        url = reverse("profiles:show",
                      kwargs={"slug": obj.profile.slug})
        # Unicode hex b6 is the Pilcrow sign
        return '<a href="{}">{}</a>'.format(url, '\xb6')
    permalink.allow_tags = True


class ProfileResource(resources.ModelResource):

    class Meta:
        model = Profile
        exclude = ('id',)
        import_id_fields = ('id_persona',)
        skip_unchanged = True
        fields = ['id_persona', 'email_verified', 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento',
                  'numero_documento', 'sexo', 'correo', 'fecha_nac']

class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource

admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TokenFirebase)


