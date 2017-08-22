from django.forms import ModelForm

from profiles.models import Profile


class ValidProfileFormMixin():
    def is_valid(self):

        valid = super(ModelForm, self).is_valid()

        try:
            persona_registrada = Profile.objects.get(numero_documento=self.cleaned_data["numero_documento"],
                                                     tipo_documento=self.cleaned_data["tipo_documento"])

            if (persona_registrada.apellido_pa.upper() != self.cleaned_data["apellido_pa"].upper()) \
                    and (persona_registrada.apellido_ma.upper() != self.cleaned_data["apellido_ma"].upper()):
                self.add_error('numero_documento', 'La persona a ingresar no coincide con el ya existente, '
                                                   'verifique el número de documento ingresado '
                                                   'la persona ya registrada es: ' +
                               persona_registrada.getNombreCompleto.title())
                valid = False

        except Profile.DoesNotExist:
            pass

        return valid
