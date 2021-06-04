from django import forms
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from .models import Usuario

class FormularioLogin(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(FormularioLogin,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class FormularioUsuario(forms.ModelForm):
    """ Formulario de Registro de un Usuario en la base de datos
        Variables:
            -password1: Contraseña
            -password2: Verificación de la contraseña
    """
    password1 = forms.CharField(label= 'Contraseña', widget= forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required': 'required'
        }
    ))

    password2 = forms.CharField(label= 'Contraseña de Confirmación', widget= forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required'
        }
    ))

    class Meta:
        model = Usuario
        fields = ('username','email','fecha_nacimiento','peso','altura')
        widgets = {
            'username': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre'
                }
            ),
            'email': forms.EmailInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Correo Electrónico'
                }
            ),
            'fecha_nacimiento': forms.DateTimeInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Fecha de Nacimiento'
                }
            ),
            'peso': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Peso'
                }
            ), 
            'altura': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Altura'
                }
            ),                     
        }
    def clean_password2(self):
        """ Validación de contraseña
        Método que valida que ambas contraseñas sean iguales antes de la encriptación. 
        
        Excepciones:
        - ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error
        """

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('¡Las contraseñas no coinciden!')
        return password2

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user