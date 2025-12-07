from django import forms
from django.contrib.auth import get_user_model
from .models import Cliente, Mascota

Usuario = get_user_model()

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        help_texts = {
            'username': 'Usaremos este nombre para iniciar sesión (puede ser tu RUT).',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

class RegistroClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'telefono', 'direccion']
        widgets = {
            'direccion': forms.TextInput(),
        }
        labels = {
            'rut': 'RUT',
            'telefono': 'Teléfono Celular',
            'direccion': 'Dirección'
        }

class RegistroMascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'genero', 'raza', 'fecha_nacimiento', 'fecha_registro']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'nombre': 'Nombre de tu Mascota',
            'genero': 'Género',
            'fecha_nacimiento': 'Fecha de Nacimiento (Aprox)',
            'fecha_registro': 'Fecha de Ingreso a Clínica'
        }

