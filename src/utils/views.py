import logging

from profiles.models import Profile
from register.models import Personal, Colegio, PersonalColegio, Direccion
from utils.middleware import get_current_colegio

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
        if not request.user.is_authenticated() or not request.session.get('colegio'):
            # return HttpResponseRedirect('/login/')
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


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
        direccion.provincia = form.cleaned_data["provincia"]
        direccion.distrito = form.cleaned_data["distrito"]

        # obtener los telefonos que vienen en el formulario

        if padre is Profile:

            if persona_registrada is not None:
                copiarVal(form=form, parent=persona_registrada)
                rpta = hijo().saveFromPersona(per=persona_registrada, parentesco=form.cleaned_data["parentesco"])
                logger.debug("Se guardó un registró a partir de la persona existente")

                direccion.persona = rpta.persona
                direccion.save()
                logger.debug("Se creo la direccion")

                return rpta
            else:
                instance = form.save()

                direccion.persona = instance.persona
                direccion.save()
                logger.debug("Se guardó la direccion")

                instance.save()
                logger.debug("Se creó un nuevo registro")

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

                #agregar la dirección
                direccion.persona = rpta.personal.persona
                direccion.save()
                
                # Verificar que no exista la relación del personal con el colegio previamente
                try:
                    per_col = PersonalColegio.objects.get(personal=rpta)
                    per_col.activo = True
                    per_col.save()
                    logger.debug("Se actualiza la relación colegio y personal a activo")
                except PersonalColegio.DoesNotExist:
                    per_col = PersonalColegio()
                    per_col.personal = rpta
                    per_col.colegio = colegio
                    per_col.save()
                    logger.debug("Se creó la relación personal colegio")
                return rpta

            else:  # Si la persona no existe

                instance = form.save()
                logger.debug("Instancia guardada: " + str(instance))

                instance.save()
                logger.debug("Se creó el registro")

                direccion.persona = instance.personal.persona
                direccion.save()
                logger.debug("se guardo la direccion")

                # Crear la relación del personal con el colegio logueado
                personal_colegio = PersonalColegio()
                personal_colegio.personal = instance.empleado
                personal_colegio.colegio = colegio
                personal_colegio.save()
                logger.debug(
                    "Se creó la relación del personal: " + str(instance.personal) + " en el Colegio: " + str(colegio))

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
