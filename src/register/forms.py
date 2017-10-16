from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.forms import ModelForm

from profiles.models import Profile
from register.models import Alumno, Apoderado, Personal, Promotor, Director, Cajero, Tesorero, Proveedor, Colegio, Sistemas, Administrativo, \
    Direccion, Docente
from utils.forms import ValidProfileFormMixin
from utils.models import TipoDocumento, TipoSexo, Departamento, Provincia, Distrito


class PersonaForm(ModelForm):

    direccion = forms.CharField(widget=forms.TextInput(attrs={'tabindex': '13', 'class': 'form-control'}), label="Direccion")
    referencia = forms.CharField(widget=forms.TextInput(attrs={'tabindex': '14', 'class': 'form-control'}), label="Referencia")
    departamento = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Departamento")
    provincia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Provincia", required=False)
    distrito = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Distrito", required=False)
    tipo_cel = forms.ChoiceField(widget=forms.Select(attrs={'tabindex': '15', 'class': 'form-control'}), label="Tipo Movil",
                                 required=False)
    celular = forms.CharField(widget=forms.NumberInput(attrs={'tabindex': '16', 'class': 'form-control'}), label="Celular",
                              required=False)
    celulares = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'tabindex': '17', 'class': 'form-control'}), label="Números",
                                          required=False)

    @property
    def ChoiceTipoDocumento(self):
        choices = [(tipo.id_tipo, tipo.descripcion) for tipo in TipoDocumento.objects.all()]
        return choices

    @property
    def ChoiceTipoSexo(self):
        choices = [(sex.id_sexo, sex.descripcion) for sex in TipoSexo.objects.all()]
        return choices

    @property
    def ChoiceDepartamento(self):

        choices = []

        choices.append(('-1', 'Seleccione'))

        for d in Departamento.objects.all():
            choices.append((d.id_departamento, d.descripcion))

        return choices

    # @property
    def ChoiceProvincia(self):
        # choices = [(p.id_provincia, p.descripcion) for p in Provincia.objects.filter(departamento__id_departamento=dpto)]
        choices = [(p.id_provincia, p.descripcion) for p in
                   Provincia.objects.all()]
        return choices

    # @property
    def ChoiceDistrito(self):
        # choices = [(d.id_distrito, d.descripcion) for d in Distrito.objects.filter(provincia__id_provincia=prov)]
        choices = [(d.id_distrito, d.descripcion) for d in Distrito.objects.all()]
        return choices

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_documento'] = forms.ChoiceField(choices=self.ChoiceTipoDocumento,
                                                          widget=forms.Select(attrs={'tabindex': '5', 'class': 'form-control'}))
        self.fields['sexo'] = forms.ChoiceField(choices=self.ChoiceTipoSexo,
                                                widget=forms.Select(attrs={'tabindex': '7', 'class': 'form-control'}))
        self.fields['departamento'] = forms.ChoiceField(choices = self.ChoiceDepartamento, initial='-1',
                                                        widget=forms.Select(attrs={'tabindex': '10', 'class': 'form-control'}))
        self.fields['nombre'].widget.attrs = {'tabindex': '1', 'class': 'form-control', 'maxlength': '50'}
        self.fields['segundo_nombre'].widget.attrs = {'tabindex': '2', 'class': 'form-control', 'maxlength': '200'}
        self.fields['apellido_pa'].widget.attrs = {'tabindex': '3', 'class': 'form-control', 'maxlength': '50'}
        self.fields['apellido_ma'].widget.attrs = {'tabindex': '4', 'class': 'form-control', 'maxlength': '50'}
        self.fields['numero_documento'].widget.attrs = {'tabindex': '6', 'class': 'form-control', 'maxlength': '15'}
        self.fields['correo'].widget.attrs = {'tabindex': '9', 'class': 'form-control'}
        self.fields['fecha_nac'] = forms.DateField(widget=forms.DateInput, input_formats=['%Y-%m-%d'])
        self.fields['fecha_nac'].widget.attrs = {'tabindex': '8', 'class': 'form-control', 'onChange': 'validarFecNac()'}

        try:
            #cargar los valores guardados en la dirección
            if kwargs['instance'].pk is not None:
                direc = Direccion.objects.get(persona__id_persona=kwargs['instance'].pk)
                self.fields['departamento'].initial = direc.dpto

                opciones_provincias = self.ChoiceProvincia()
                opciones_distritos = self.ChoiceDistrito()

                self.fields['provincia'] = forms.ChoiceField(choices=opciones_provincias,
                    widget=forms.Select(attrs={'tabindex': '11', 'class': 'form-control'}))
                self.fields['distrito'] = forms.ChoiceField(choices=opciones_distritos,
                    widget=forms.Select(attrs={'tabindex': '12', 'class': 'form-control'}))

                self.fields['provincia'].initial = direc.provincia
                self.fields['distrito'].initial = direc.distrito
                self.fields['direccion'].initial = direc.calle
                self.fields['referencia'].initial = direc.referencia
        except:
            self.fields['provincia'] = forms.ChoiceField(choices=self.ChoiceProvincia, initial='-1',
                                                            widget=forms.Select(
                                                                attrs={'tabindex': '10', 'class': 'form-control'}))
            self.fields['distrito'] = forms.ChoiceField(choices=self.ChoiceDistrito, initial='-1',
                                                            widget=forms.Select(
                                                                attrs={'tabindex': '10', 'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class AlumnoForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Alumno", required=False)

    class Meta:
        model = Alumno
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class ApoderadoForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Apoderado", required=False)

    #alu = forms.CharField(widget=forms.TextInput(attrs={'tabindex': '23', 'class': 'form-control'}), label="Direccion")

    alumno = forms.ModelMultipleChoiceField(queryset=Alumno.objects.all(),required= False,
                                 widget=autocomplete.ModelSelect2Multiple(url='registers:alumno_autocomplete',attrs={'tabindex': '27', 'class': 'form-control'}))

    #parentesco = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    def ChoiceParentesco(self):
        MY_CHOICES = (
            ('Padre', 'Padre'),
            ('Madre', 'Madre'),
            ('Tio', 'Tio'),
            ('Hermano', 'Hermano'),
            ('Apoderado', 'Apoderado')
        )
        return MY_CHOICES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parentesco'] = forms.ChoiceField(choices=self.ChoiceParentesco())
        self.fields['parentesco'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Apoderado
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento',
                  'numero_documento', 'sexo', 'correo', 'fecha_nac']


class PersonalForm(ValidProfileFormMixin, PersonaForm):

    class Meta:
        model = Personal
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class SistemasForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Sistemas", required=False)

    class Meta:
        model = Sistemas
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class DocenteForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Docente", required=False)

    class Meta:
        model = Docente
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class PromotorForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Promotor", required=False)

    class Meta:
        model = Promotor
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class DirectorForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Director", required=False)

    class Meta:
        model = Director
        fields = [ 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class CajeroForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Cajero", required=False)

    class Meta:
        model = Cajero
        fields = [ 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']


class TesoreroForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Tesorero", required=False)

    class Meta:
        model = Tesorero
        fields = [ 'nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']

class AdministrativoForm(ValidProfileFormMixin, PersonaForm):

    title = forms.CharField(label="Registrar Administrativo", required=False)

    class Meta:
        model = Administrativo
        fields = ['nombre', 'segundo_nombre', 'apellido_pa', 'apellido_ma', 'tipo_documento', 'numero_documento',
                  'sexo', 'correo', 'fecha_nac']

class ProveedorForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "idproveedor"
        self.helper.form_method = "post"

        self.helper.add_input(Submit('submit', 'Grabar', css_class="btn btn-primary btn-block btn-flat"))

    class Meta:
        model = Proveedor
        fields = ['razon_social', 'ruc']


class ColegioForm(ModelForm):

    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Direccion")
    referencia = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Referencia")
    departamento = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Departamento")
    provincia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Provincia")
    distrito = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Distrito")
    tipo_cel = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Tipo Movil",
                                 required=False)
    celular = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Celular",
                              required=False)
    celulares = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}), label="Números",
                                          required=False)

    @property
    def ChoiceTipoDocumento(self):
        choices = [(tipo.id_tipo, tipo.descripcion) for tipo in TipoDocumento.objects.all()]
        return choices

    @property
    def ChoiceTipoSexo(self):
        choices = [(sex.id_sexo, sex.descripcion) for sex in TipoSexo.objects.all()]
        return choices

    @property
    def ChoiceDepartamento(self):
        choices = [(d.id_departamento, d.descripcion) for d in Departamento.objects.all()]
        return choices

    @property
    def ChoiceProvincia(self):
        choices = [(p.id_provincia, p.descripcion) for p in Provincia.objects.all()]
        return choices

    @property
    def ChoiceDistrito(self):
        choices = [(d.id_distrito, d.descripcion) for d in Distrito.objects.all()]
        return choices

    class Meta:
        model = Colegio
        fields = [
            'nombre',
            'ruc',
            'ugel',
            'departamento',
            'provincia',
            'distrito',
            'referencia',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['ruc'].widget.attrs.update({'class': 'form-control'})
        self.fields['ugel'].widget.attrs.update({'class': 'form-control'})
        self.fields['departamento'] = forms.ChoiceField(choices=self.ChoiceDepartamento,
                                                        widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['provincia'] = forms.ChoiceField(choices=self.ChoiceProvincia,
                                                     widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['distrito'] = forms.ChoiceField(choices=self.ChoiceDistrito,
                                                    widget=forms.Select(attrs={'class': 'form-control'}))
