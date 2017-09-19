from authtools.models import User
from authtools.forms import UserCreationForm

class RegistroUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'groups',
            'email',
            'name',
            'password1',
            'password2',

        ]

        labels = {
            'groups': 'Grupo',
            'email': 'Correo',
            'name': 'Nombre de Usuario',
            'password1': 'Crea una contraseña',
            'password2': 'Confirma tu contraseña',

        }
