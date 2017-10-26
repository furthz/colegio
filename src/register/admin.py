from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Alumno
# Register your models here.
class AlumnoResource(resources.ModelResource):

    class Meta:
        model = Alumno
        exclude = ('id',)
        import_id_fields = ('id_alumno',)
        skip_unchanged = True
        fields = ['id_alumno', 'id_persona']

class AlumnoAdmin(ImportExportModelAdmin):
    resource_class = AlumnoResource

admin.site.register(Alumno, AlumnoAdmin)
#admin.site.register(Alumno)
