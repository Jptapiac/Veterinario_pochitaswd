from clinic.models import Mascota, Cliente

print(f'Total Mascotas: {Mascota.objects.count()}')
print(f'Total Clientes: {Cliente.objects.count()}')
print('\nPrimeras 5 mascotas:')
for m in Mascota.objects.all()[:5]:
    print(f'  - {m.nombre} ({m.especie}) - Cliente: {m.cliente.nombre} {m.cliente.apellido} (ID: {m.cliente.id})')

print('\nCliente ID 5:')
try:
    cliente = Cliente.objects.get(id=5)
    print(f'  Nombre: {cliente.nombre} {cliente.apellido}')
    mascotas = Mascota.objects.filter(cliente=cliente)
    print(f'  Mascotas: {mascotas.count()}')
    for m in mascotas:
        print(f'    - {m.nombre} ({m.especie})')
except Cliente.DoesNotExist:
    print('  Cliente ID 5 no existe')
