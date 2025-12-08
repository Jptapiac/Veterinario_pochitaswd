from clinic.models import Usuario
from django.contrib.auth.hashers import make_password

# Nuevas credenciales
credenciales = {
    # Recepcionistas
    'recepcion': 'Recep2024!',
    'maria.gonzalez': 'Maria2024!',
    
    # Veterinarios
    'dr_juan': 'DrJuan2024!',
    'dr_ana': 'DrAna2024!',
    'dr_pedro': 'DrPedro2024!',
    'vet': 'Vet2024!',
    'juan.perez': 'JuanP2024!',
    'maria.silva': 'MariaS2024!',
    'carlos.ruiz': 'CarlosR2024!',
    
    # Clientes
    'carlos': 'Carlos2024!',
    'manolo': 'Manolo2024!',
    'marlen_test_script': 'Marlen2024!',
    '22.987.654-2': 'Cliente2024!',
    'cliente': 'Client2024!',
}

print("=== ACTUALIZANDO CONTRASEÑAS ===\n")

for username, password in credenciales.items():
    try:
        user = Usuario.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✓ {username}: {password}")
    except Usuario.DoesNotExist:
        print(f"✗ {username}: Usuario no encontrado")

print("\n=== ACTUALIZACIÓN COMPLETADA ===")
