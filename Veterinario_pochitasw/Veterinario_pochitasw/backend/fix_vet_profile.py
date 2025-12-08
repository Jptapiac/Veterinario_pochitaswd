import os
import django
import sys

# Setup Django environment
sys.path.append(r'C:\Users\Josta\Documents\Veterinario_pochitasw\Veterinario_pochitasw\Veterinario_pochitasw\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pochita_project.settings')
django.setup()

from clinic.models import Usuario, Veterinario

usernames = ["juan.perez", "carlos.ruiz", "maria.silva"]

for username in usernames:
    print(f"\nProcessing user: {username}...")
    try:
        user = Usuario.objects.get(username=username)
        print(f"User found: {user.username} (ID: {user.id})")
        print(f"Role: {user.rol}")
        
        if hasattr(user, 'perfil_veterinario'):
            print(f"[OK] Profile exists: {user.perfil_veterinario}")
        else:
            print("[MISSING] User has NO Veterinario profile.")
            
            print("Attempting to fix...")
            
            # Create unique dummy data per user to avoid unique constraint errors
            dummy_rut = f"1{user.id}.111.111-1"
            dummy_phone = f"+569111111{user.id}"
            
            vet, created = Veterinario.objects.get_or_create(
                nombre=user.first_name + " " + user.last_name,
                defaults={
                    'rut': dummy_rut,
                    'especialidad': 'General',
                    'telefono': dummy_phone
                }
            )
            
            if created:
                print("Created new Veterinario profile.")
            else:
                print("Found existing Veterinario profile (unlinked or reused).")
                
            # Link it
            if vet.usuario != user:
                vet.usuario = user
                vet.save()
                print("[SUCCESS] Succesfully linked Veterinario profile to User.")
            else:
                print("Profile was already linked? (Should not happen given the error)")

    except Usuario.DoesNotExist:
        print(f"User {username} not found.")
    except Exception as e:
        print(f"Error processing {username}: {e}")
