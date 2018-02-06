import logging
from django.forms import ModelForm

from profiles.models import Profile

logger = logging.getLogger("project")


class ValidProfileFormMixin():

    def is_valid(self):

        valid = super(ModelForm, self).is_valid()
        logger.debug("Redefiniendo el método Valid")

        try:
            if self.cleaned_data["numero_documento"] != "00000000":
                persona_registrada = Profile.objects.get(numero_documento=self.cleaned_data["numero_documento"],
                                                         tipo_documento=self.cleaned_data["tipo_documento"])
                logger.debug("Se encontró una persona registrada: " + str(persona_registrada.id_persona))

                try:
                    if (persona_registrada.apellido_pa.upper() != self.cleaned_data["apellido_pa"].upper()) \
                            and (persona_registrada.apellido_ma.upper() != self.cleaned_data["apellido_ma"].upper()):

                        self.add_error('numero_documento', 'La persona a ingresar no coincide con el ya existente, '
                                                           'verifique el número de documento ingresado '
                                                           'la persona ya registrada es: ' +
                                       persona_registrada.getNombreCompleto.title())

                        logger.error("Existe una persona igual con el mismo número de documento")

                        valid = False
                except:
                    if (persona_registrada.apellido_pa.upper() != self.cleaned_data["apellido_pa"].upper()):
                        self.add_error('numero_documento', 'La persona a ingresar no coincide con el ya existente, '
                                                           'verifique el número de documento ingresado '
                                                           'la persona ya registrada es: ' +
                                       persona_registrada.getNombreCompleto.title())

                        logger.error("Existe una persona igual con el mismo número de documento")

                        valid = False
        except Profile.DoesNotExist:
            pass

        return valid
