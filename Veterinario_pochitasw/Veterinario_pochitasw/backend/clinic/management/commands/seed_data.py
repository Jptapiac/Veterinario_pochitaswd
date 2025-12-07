from django.core.management.base import BaseCommand
from django.utils import timezone
from clinic.models import Usuario, Cliente, Veterinario, Mascota, Cita, Producto, ListaEspera
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Poblar base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write('Eliminando datos antiguos...')
        Cita.objects.all().delete()
        Mascota.objects.all().delete()
        Cliente.objects.all().delete()
        Veterinario.objects.all().delete()
        Usuario.objects.all().delete()
        Producto.objects.all().delete()

        self.stdout.write('Creando usuarios y roles...')
        
        # Admin
        Usuario.objects.create_superuser('admin', 'admin@pochita.cl', 'admin123', rol=Usuario.Roles.ADMIN)
        
        # Recepcionista
        recep = Usuario.objects.create_user('recepcion', 'recep@pochita.cl', 'recep123', rol=Usuario.Roles.RECEPCIONISTA)
        recep.first_name = "María"
        recep.last_name = "Pérez"
        recep.save()

        # Veterinarios
        vets_data = [
            ('Juan', 'Soto', '11.111.111-1', 'Cirujano'),
            ('Ana', 'Gómez', '12.222.222-2', 'Dermatóloga'),
            ('Pedro', 'Lira', '13.333.333-3', 'General'),
        ]
        
        vets_objs = []
        for nombre, apellido, rut, esp in vets_data:
            u = Usuario.objects.create_user(f'dr_{nombre.lower()}', f'{nombre}@pochita.cl', 'vet123', rol=Usuario.Roles.VETERINARIO)
            v = Veterinario.objects.create(
                usuario=u,
                rut=rut,
                nombre=f"{nombre} {apellido}",
                especialidad=esp,
                telefono='+56911111111'
            )
            vets_objs.append(v)

        # Clientes y Mascotas
        clientes_data = [
            ('Carlos', 'Díaz', '14.444.444-4', ['Bobby']),
        ]

        mascotas_objs = []
        for nombre, apellido, rut, mascotas in clientes_data:
            u = Usuario.objects.create_user(f'{nombre.lower()}', f'{nombre}@gmail.com', 'client123', rol=Usuario.Roles.CLIENTE)
            c = Cliente.objects.create(
                usuario=u,
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                telefono='+56922222222',
                email=u.email,
                direccion='Av. Siempre Viva 123'
            )
            
            for m_nombre in mascotas:
                m = Mascota.objects.create(
                    cliente=c,
                    nombre=m_nombre,
                    especie=Mascota.Especie.GATO if 'i' in m_nombre else Mascota.Especie.PERRO,
                    raza='Mestizo',
                    fecha_nacimiento=timezone.now().date() - timedelta(days=365*random.randint(1, 10))
                )
                mascotas_objs.append(m)

        # Citas
        self.stdout.write('Agendando citas...')
        # Citas pasadas
        for _ in range(5):
            Cita.objects.create(
                veterinario=random.choice(vets_objs),
                mascota=random.choice(mascotas_objs),
                fecha_hora=timezone.now() - timedelta(days=random.randint(1, 10), hours=random.randint(1, 5)),
                motivo='Control rutinario',
                estado=Cita.Estado.REALIZADA,
                tipo=Cita.Tipo.CONTROL
            )

        # Citas futuras
        for _ in range(5):
            Cita.objects.create(
                veterinario=random.choice(vets_objs),
                mascota=random.choice(mascotas_objs),
                fecha_hora=timezone.now() + timedelta(days=random.randint(1, 7), hours=random.randint(1, 5)),
                motivo='Consulta general',
                estado=Cita.Estado.AGENDADA,
                tipo=Cita.Tipo.CONSULTA
            )

        # Productos
        p_data = [
            ('Correa Perro', 5000, 10),
            ('Alimento Gato 1kg', 8000, 20),
            ('Juguete Hueso', 3000, 15),
            ('Pipeta Pulgas', 12000, 50),
        ]
        for nom, prec, st in p_data:
            Producto.objects.create(nombre=nom, precio=prec, stock=st)

        self.stdout.write(self.style.SUCCESS('Base de datos poblada exitosamente!'))
