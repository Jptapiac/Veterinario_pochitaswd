import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pochita_project.settings')
django.setup()

from clinic.models import Cita

def clean_bobby():
    # Filter appointments for 'Bobby' that are just 'AGENDADA' (not realized, etc)
    citas_bobby = Cita.objects.filter(mascota__nombre__iexact='Bobby', estado='AGENDADA')
    count = citas_bobby.count()
    
    print(f"Encontradas {count} citas AGENDADAS para Bobby.")
    
    if count > 0:
        citas_bobby.delete()
        print("Se han eliminado las citas agendadas de Bobby.")
    else:
        print("No hay citas pendientes para eliminar.")

if __name__ == '__main__':
    clean_bobby()
