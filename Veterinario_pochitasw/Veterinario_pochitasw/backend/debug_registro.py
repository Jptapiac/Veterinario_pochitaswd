import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pochita_project.settings')
django.setup()

from clinic.forms import RegistroUsuarioForm, RegistroClienteForm
from clinic.models import Usuario, Cliente
from django.db import transaction

def test_create_client():
    print("Iniciando prueba de creación de cliente...")
    
    # Datos simulados de un cliente válido
    data_user = {
        'username': 'marlen_test_script',
        'first_name': 'Marlen',
        'last_name': 'Prueba',
        'email': 'marlen@test.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }
    
    data_cliente = {
        'rut': '99.999.999-9',
        'telefono': '+56912345678',
        'direccion': 'Calle Falsa 123'
    }
    
    user_form = RegistroUsuarioForm(data=data_user)
    cliente_form = RegistroClienteForm(data=data_cliente)
    
    if user_form.is_valid() and cliente_form.is_valid():
        print("Forms válidos. Intentando guardar...")
        try:
            with transaction.atomic():
                user = user_form.save(commit=False)
                user.set_password(data_user['password'])
                user.rol = Usuario.Roles.CLIENTE
                user.save()
                print(f"Usuario creado: {user}")

                cliente = cliente_form.save(commit=False)
                cliente.usuario = user
                cliente.nombre = user.first_name
                cliente.apellido = user.last_name
                cliente.email = user.email
                cliente.save()
                print(f"Cliente creado: {cliente}")
                print("¡ÉXITO! El cliente se guardó correctamente.")
        except Exception as e:
            print(f"Excepción al guardar: {e}")
    else:
        print("Errores de validación:")
        print(f"User Form Errors: {user_form.errors}")
        print(f"Cliente Form Errors: {cliente_form.errors}")

if __name__ == '__main__':
    test_create_client()
