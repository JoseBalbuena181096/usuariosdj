from django import forms
from .models import User
from django.contrib.auth import authenticate


class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required= True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña',
        required= True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repetir contraseña'
            }
        )
    )

    class Meta:
        # EL modelo del formulario
        model = User
        # fields = ('__all__' )
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
            )
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas son diferentes')
    
    # def clean_password1(self):
    #     if len(self.cleaned_data['password1']) < 5:
    #         self.add_error('password1', 'Las contraseñas son muy cortas')

class LoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        required= True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'nombre usuario',
                'style': '{margin : 10px}'
            }
        )
    )

    password = forms.CharField(
        label='Contraseña',
        required= True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña'
            }
        )
    )
    # Validación si existe el usuario y su contraseña
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        # recuperamos la data del formulario
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username = username, password = password):
            raise forms.ValidationError('El usuario o el password no son correctos ')
        return cleaned_data
    
class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Ingrese contraseña actual ',
        required= True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña Actual'
            }
        )
    )

    password2 = forms.CharField(
        label='Ingrese contraseña Nueva ',
        required= True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña Nueva'
            }
        )
    )

class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True,
                                  label='Ingrese código de verificación')

    # recivo el pk desde la vista
    def __init__(self,pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            # verificamos si el codigo e id del usuario son validos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('el código es incorrecto')    
        else:
            raise forms.ValidationError('el código es incorrecto') 