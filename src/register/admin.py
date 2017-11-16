from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Alumno, Direccion


# Register your models here.
class AlumnoResource(resources.ModelResource):
    class Meta:
        model = Alumno
        exclude = ('id',)
        import_id_fields = ('id_alumno',)
        skip_unchanged = True
        fields = ['id_alumno', 'codigoint', 'id_persona', 'email_verified',
                  'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma',
                  'tipo_documento', 'numero_documento', 'fecha_nac', 'sexo',
                  'correo', 'usuario_creacion_persona', 'usuario_modificacion_persona',
                  'usuario_creacion_alumno', 'usuario_modificacion_alumno', 'fecha_creacion_persona',
                  'fecha_modificacion_persona', 'fecha_creacion_alumno', 'fecha_modificacion_alumno']


class AlumnoAdmin(ImportExportModelAdmin):
    resource_class = AlumnoResource


admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Direccion)
# admin.site.register(Alumno)
