import logging
import json

from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from profiles.models import Profile
from register.models import Personal, Colegio, PersonalColegio, Direccion, Telefono, ApoderadoAlumno, Apoderado
from utils.middleware import get_current_colegio
from utils.models import Provincia, Distrito, TiposGrados, TiposNivel

logger = logging.getLogger("project")


# Create your views here.
class ContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Es posible agregar valores al contexto
        return context


class MyLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        logger.debug("MIXIN LOGGIN: ")
        logger.debug("usuario logueado: " + str(request.user.is_authenticated()))
        logger.debug("colegio: " + str(request.session.get('colegio')))
        if not request.user.is_authenticated():
            if not request.user.is_superuser and not request.session.get('colegio'):
                return HttpResponseRedirect('/login/')
            # return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def get_provincias(request):

    if request.is_ajax():
        id_dpto = request.GET.get("id_dpto"," ")
        provincias = Provincia.objects.filter(departamento__id_departamento=id_dpto)
        results = []
        for prov in provincias:
            prov_json = {}
            prov_json['id'] = prov.id_provincia
            prov_json['value'] = prov.descripcion
            results.append(prov_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def get_distritos(request):

    if request.is_ajax():
        id_prov = request.GET.get("id_prov", " ")
        distritos = Distrito.objects.filter(provincia__id_provincia=id_prov)
        results = []
        for dist in distritos:
            dist_json = {}
            dist_json['id'] = dist.id_distrito
            dist_json['value'] = dist.descripcion
            results.append(dist_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'

    return HttpResponse(data, mimetype)

def get_grados(request):

    if request.is_ajax():
        id_nivel = request.GET.get("id_nivel", " ")
        grados = TiposGrados.objects.filter(nivel__id_tipo=id_nivel)
        results = []
        for grado in grados:
            grado_json = {}
            grado_json['id'] = grado.id_tipo_grado
            grado_json['value'] = grado.descripcion
            results.append(grado_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'

    return HttpResponse(data, mimetype)

class SaveGeneric(MyLoginRequiredMixin):

    @staticmethod
    def saveGeneric(padre, form, hijo, **atributos):

        try:
            persona_registrada = Profile.objects.get(numero_documento=form.cleaned_data["numero_documento"],
                                                     tipo_documento=form.cleaned_data["tipo_documento"])
            logger.debug("Persona ya registrada en la tabla Profile con ID: " + str(persona_registrada.id_persona))

        except Profile.DoesNotExist:
            persona_registrada = None

        # Obtener los datos de la dirección del formulario
        direccion = Direccion()
        direccion.calle = form.cleaned_data["direccion"]
        direccion.referencia = form.cleaned_data["referencia"]
        direccion.dpto = form.cleaned_data["departamento"]
        direccion.provincia = form.data["provincia"]
        direccion.distrito = form.data["distrito"]

        logger.debug("Se obtuvieron los datos de la direccion")

        # obtener los telefonos que vienen en el formulario
        celulares = form.data['nros']
        lst_celulares = celulares.split(',')
        lista_numeros=[]
        for cel in lst_celulares:
            telef = Telefono(numero=cel, tipo="Celular")
            lista_numeros.append(telef)

        logger.debug("Se obtuvieron los datos del telefono")

        if padre is Profile:

            logger.debug("El ingreso es un Profile")
            logger.info("El ingreso es un Profile")

            if persona_registrada is not None:
                copiarVal(form=form, parent=persona_registrada)
                logger.debug("Es una nuevo profile a crear")

                rpta = hijo().saveFromPersona(per=persona_registrada, parentesco=form.cleaned_data["parentesco"],
                                              alumno=form.cleaned_data["alumno"])
                logger.debug("Se guardó un registró a partir de la persona existente")
                logger.info("Se creó un registro a partir de la persona existente")

                if hijo is Apoderado:

                    alumnos = form.cleaned_data['alumno']

                    for alumno in alumnos:
                        apo_alu = ApoderadoAlumno()
                        apo_alu.parentesco = form.cleaned_data['parentesco']
                        apo_alu.alumno = alumno
                        apo_alu.apoderado = rpta
                        apo_alu.save()

                    #hijo.alumnos.add(apo_alu.alumno)

                direccion.persona = rpta.persona
                direccion.save()
                logger.info("Se creó la dirección de la nueva persona")
                logger.debug("Se creo la direccion")

                try:
                    for t in lista_numeros:
                        t.persona = rpta.persona
                        t.save()
                    logger.debug("Se guardaron los numeros de telefono")
                    logger.info("Se guardaron los numeros de telefono")
                except:
                    logger.debug("error")
                    logger.error("Se capturo el error a la hora de guardar los telefonos")
                    pass

                return rpta
            else:
                logger.debug("Se va a crear una nueva persona")
                instance = form.save()
                logger.info("Se va a crear una nueva persona")

                direccion.persona = instance.persona
                direccion.save()
                logger.debug("Se guardó la direccion")
                logger.info("Se guardó la nueva direccion")

                if hijo is Apoderado:
                    logger.debug("Se guardará la relación Apoderado-Alumno")
                    alumnos = form.cleaned_data['alumno']

                    for alumno in alumnos:
                        apo_alu = ApoderadoAlumno()
                        apo_alu.parentesco = form.cleaned_data['parentesco']
                        logger.debug("Parentesco: " + str(form.cleaned_data['parentesco']))

                        apo_alu.alumno = alumno
                        logger.debug("Alumno: " + str(form.cleaned_data['alumno']))

                        apo_alu.apoderado = instance

                        rpta = apo_alu.save()
                        logger.debug("respuesta: " + str(rpta))

                    # instance.alumnos.add(apo_alu.alumno)

                instance.save()
                logger.debug("Se creó un nuevo registro")

                try:
                    for t in lista_numeros:
                        t.persona = instance.persona
                        t.save()
                    logger.debug("Se guardaron los numeros de telefono")
                    logger.info("Se guardaron los numeros de telefono")
                except:
                    logger.debug("error")
                    logger.error("Error a la hora de registrar los telefonos")
                    pass

                return instance

        elif padre is Personal:
            id_colegio = get_current_colegio()

            colegio = Colegio.objects.get(id_colegio=id_colegio)
            logger.debug("Colegio logueado: " + str(colegio))

            # Si la persona existe
            if persona_registrada is not None:

                copiarVal(form=form, parent=persona_registrada)
                rpta = hijo().saveFromPersonal(per=persona_registrada, **atributos)
                logger.debug("se creó un personal a partir de la persona")
                logger.info("se creo un personal a partir de la persona")

                #agregar la dirección
                direccion.persona = rpta.personal.persona
                direccion.save()
                logger.debug("Se guardo la direccion asociada a la persona")
                logger.info("Se guardo la direccion asociada a la persona")

                try:
                    for t in lista_numeros:
                        t.persona = rpta.personal.persona
                        t.save()
                        logger.debug("Se guardaron los numeros de telefono")
                        logger.info("Se guardaron los numeros de telefono")
                except:
                    logger.debug("error")
                    logger.error("Error a la hora de registrar los telefonos")
                    pass

                # Verificar que no exista la relación del personal con el colegio previamente
                try:
                    per_col = PersonalColegio.objects.get(personal=rpta)
                    per_col.activo = True
                    per_col.save()
                    logger.debug("Se actualiza la relación colegio y personal a activo")
                    logger.info("Se actualiza la relacion del colegio y personal a activo")
                except PersonalColegio.DoesNotExist:
                    per_col = PersonalColegio()
                    per_col.personal = rpta
                    per_col.colegio = colegio
                    per_col.save()
                    logger.debug("Se creó la relación personal colegio")
                    logger.info("Se creo la relacion personal colegio")
                return rpta

            else:  # Si la persona no existe

                instance = form.save()
                logger.debug("Instancia guardada: " + str(instance))

                instance.save()
                logger.debug("Se creó el registro")
                logger.info("Se creo el registro de la persona")

                direccion.persona = instance.personal.persona
                direccion.save()
                logger.debug("se guardo la direccion")
                logger.info("Se guardo la direcion")

                try:
                    for t in lista_numeros:
                        t.persona = instance.personal.persona
                        t.save()
                    logger.debug("Se guardaron los numeros de telefono")
                    logger.info("Se guardaron los numeros de telefono")
                except:
                    logger.debug("Error")
                    logger.error("Error a la hora de guardar los telefonos")
                    pass

                # Crear la relación del personal con el colegio logueado
                personal_colegio = PersonalColegio()
                personal_colegio.personal = instance.empleado
                personal_colegio.colegio = colegio
                personal_colegio.save()
                logger.debug(
                    "Se creó la relación del personal: " + str(instance.personal) + " en el Colegio: " + str(colegio))
                logger.info("Se creó la relación del personal: " + str(instance.personal) + " en el Colegio: " + str(colegio))

                logger.debug("Se creó un nuevo personal")
                return instance


def copiarVal(form, parent: Profile):
    parent.nombre = form.cleaned_data["nombre"]
    logger.debug("se modificó nombre: " + form.cleaned_data["nombre"])

    parent.segundo_nombre = form.cleaned_data["segundo_nombre"]
    logger.debug("Se modificó el segundo_nombre: " + form.cleaned_data["segundo_nombre"])

    parent.apellido_pa = form.cleaned_data["apellido_pa"]
    logger.debug("Se modificó el apellido_pa: " + form.cleaned_data["apellido_pa"])

    parent.apellido_ma = form.cleaned_data["apellido_ma"]
    logger.debug("Se modificó apellido_pa: " + form.cleaned_data["apellido_ma"])

    parent.correo = form.cleaned_data["correo"]
    logger.debug("Se modificó correo: " + form.cleaned_data["correo"])

    parent.save()
    logger.debug("actualizado los campos del profile")
