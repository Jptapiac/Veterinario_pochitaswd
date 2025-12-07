# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pochita_project.settings')
django.setup()

from clinic.models import Usuario, Veterinario, Cliente, Mascota
from datetime import date

def create_users():
    print("=" * 60)
    print("CREANDO USUARIOS DE PRUEBA - VETERINARIA POCHITA S.A.")
    print("=" * 60)
    
    # 1. ADMIN
    print("\n[1/5] Creando usuario ADMINISTRADOR...")
    admin, created = Usuario.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@pochita.cl',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'rol': Usuario.Roles.ADMIN
        }
    )
    admin.set_password('Admin2025!')
    admin.save()
    print("   [OK] Usuario: admin | Password: Admin2025!")
    
    
    # 2. RECEPCIONISTA
    print("\n[2/5] Creando usuario RECEPCIONISTA...")
    recep_user, created = Usuario.objects.get_or_create(
        username='maria.gonzalez',
        defaults={
            'email': 'recepcion@pochita.cl',
            'first_name': 'Maria',
            'last_name': 'Gonzalez',
            'rol': Usuario.Roles.RECEPCIONISTA
        }
    )
    recep_user.set_password('Recep2025!')
    recep_user.save()
    print("   [OK] Usuario: maria.gonzalez | Password: Recep2025!")
    
    # 3. VETERINARIOS
    print("\n[3/5] Creando usuarios VETERINARIOS...")
    
    # Veterinario 1: Dr. Juan Perez (Cirugia)
    vet1_user, created = Usuario.objects.get_or_create(
        username='juan.perez',
        defaults={
            'email': 'juan.perez@pochita.cl',
            'first_name': 'Juan',
            'last_name': 'Perez',
            'rol': Usuario.Roles.VETERINARIO
        }
    )
    vet1_user.set_password('Vet2025!')
    vet1_user.save()
    
    Veterinario.objects.get_or_create(
        rut='11.111.111-1',
        defaults={
            'usuario': vet1_user,
            'nombre': 'Dr. Juan Perez',
            'especialidad': 'Cirugia y Traumatologia',
            'telefono': '+56911111111'
        }
    )
    print("   [OK] Usuario: juan.perez | Password: Vet2025! | Especialidad: Cirugia")
    
    # Veterinario 2: Dra. Maria Silva (Medicina Interna)
    vet2_user, created = Usuario.objects.get_or_create(
        username='maria.silva',
        defaults={
            'email': 'maria.silva@pochita.cl',
            'first_name': 'Maria',
            'last_name': 'Silva',
            'rol': Usuario.Roles.VETERINARIO
        }
    )
    vet2_user.set_password('Vet2025!')
    vet2_user.save()
    
    Veterinario.objects.get_or_create(
        rut='12.222.222-2',
        defaults={
            'usuario': vet2_user,
            'nombre': 'Dra. Maria Silva',
            'especialidad': 'Medicina Interna',
            'telefono': '+56922222222'
        }
    )
    print("   [OK] Usuario: maria.silva | Password: Vet2025! | Especialidad: Medicina Interna")
    
    # Veterinario 3: Dr. Carlos Ruiz (Urgencias)
    vet3_user, created = Usuario.objects.get_or_create(
        username='carlos.ruiz',
        defaults={
            'email': 'carlos.ruiz@pochita.cl',
            'first_name': 'Carlos',
            'last_name': 'Ruiz',
            'rol': Usuario.Roles.VETERINARIO
        }
    )
    vet3_user.set_password('Vet2025!')
    vet3_user.save()
    
    Veterinario.objects.get_or_create(
        rut='13.333.333-3',
        defaults={
            'usuario': vet3_user,
            'nombre': 'Dr. Carlos Ruiz',
            'especialidad': 'Urgencias 24/7',
            'telefono': '+56933333333'
        }
    )
    print("   [OK] Usuario: carlos.ruiz | Password: Vet2025! | Especialidad: Urgencias")
    
    # 4. CLIENTES
    print("\n[4/5] Creando usuarios CLIENTES...")
    
    # Cliente 1: Pedro Picapiedra
    cli1_user, created = Usuario.objects.get_or_create(
        username='pedro.picapiedra',
        defaults={
            'email': 'pedro@example.com',
            'first_name': 'Pedro',
            'last_name': 'Picapiedra',
            'rol': Usuario.Roles.CLIENTE
        }
    )
    cli1_user.set_password('Cliente2025!')
    cli1_user.save()
    
    cliente1, created = Cliente.objects.get_or_create(
        rut='16.666.666-6',
        defaults={
            'usuario': cli1_user,
            'nombre': 'Pedro',
            'apellido': 'Picapiedra',
            'telefono': '+56966666666',
            'email': 'pedro@example.com',
            'direccion': 'Av. Siempre Viva 123, Santiago'
        }
    )
    
    # Mascotas de Pedro
    Mascota.objects.get_or_create(
        cliente=cliente1,
        nombre='Dino',
        defaults={
            'especie': 'Perro',
            'raza': 'Golden Retriever',
            'fecha_nacimiento': date(2020, 5, 15),
            'observaciones': 'Muy jugueton, le gusta correr'
        }
    )
    print("   [OK] Usuario: pedro.picapiedra | Password: Cliente2025! | Mascota: Dino")
    
    # Cliente 2: Ana Torres
    cli2_user, created = Usuario.objects.get_or_create(
        username='ana.torres',
        defaults={
            'email': 'ana.torres@example.com',
            'first_name': 'Ana',
            'last_name': 'Torres',
            'rol': Usuario.Roles.CLIENTE
        }
    )
    cli2_user.set_password('Cliente2025!')
    cli2_user.save()
    
    cliente2, created = Cliente.objects.get_or_create(
        rut='17.777.777-7',
        defaults={
            'usuario': cli2_user,
            'nombre': 'Ana',
            'apellido': 'Torres',
            'telefono': '+56977777777',
            'email': 'ana.torres@example.com',
            'direccion': 'Los Aromos 456, Providencia'
        }
    )
    
    # Mascotas de Ana
    Mascota.objects.get_or_create(
        cliente=cliente2,
        nombre='Michi',
        defaults={
            'especie': 'Gato',
            'raza': 'Persa',
            'fecha_nacimiento': date(2021, 3, 10),
            'observaciones': 'Tranquilo, le gusta dormir'
        }
    )
    Mascota.objects.get_or_create(
        cliente=cliente2,
        nombre='Luna',
        defaults={
            'especie': 'Gato',
            'raza': 'Siames',
            'fecha_nacimiento': date(2022, 8, 20),
            'observaciones': 'Muy activa y curiosa'
        }
    )
    print("   [OK] Usuario: ana.torres | Password: Cliente2025! | Mascotas: Michi, Luna")
    
    # Cliente 3: Roberto Gomez
    cli3_user, created = Usuario.objects.get_or_create(
        username='roberto.gomez',
        defaults={
            'email': 'roberto@example.com',
            'first_name': 'Roberto',
            'last_name': 'Gomez',
            'rol': Usuario.Roles.CLIENTE
        }
    )
    cli3_user.set_password('Cliente2025!')
    cli3_user.save()
    
    cliente3, created = Cliente.objects.get_or_create(
        rut='18.888.888-8',
        defaults={
            'usuario': cli3_user,
            'nombre': 'Roberto',
            'apellido': 'Gomez',
            'telefono': '+56988888888',
            'email': 'roberto@example.com',
            'direccion': 'Las Condes 789, Las Condes'
        }
    )
    
    # Mascota de Roberto
    Mascota.objects.get_or_create(
        cliente=cliente3,
        nombre='Bobby',
        defaults={
            'especie': 'Perro',
            'raza': 'Labrador',
            'fecha_nacimiento': date(2019, 11, 5),
            'observaciones': 'Necesita ejercicio diario'
        }
    )
    print("   [OK] Usuario: roberto.gomez | Password: Cliente2025! | Mascota: Bobby")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] USUARIOS CREADOS EXITOSAMENTE")
    print("=" * 60)
    print("\nPara acceder al sistema, usa las credenciales mostradas arriba.")
    print("URL de acceso: http://127.0.0.1:8000/api/login/")
    print("\n")

if __name__ == '__main__':
    create_users()
