from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Usuario, Cliente, Veterinario, Mascota, Cita, Atencion, ListaEspera, Producto
from .serializers import (
    UsuarioSerializer, ClienteSerializer, VeterinarioSerializer, MascotaSerializer, 
    CitaSerializer, AtencionSerializer, ListaEsperaSerializer, ProductoSerializer
)
from .forms import RegistroUsuarioForm, RegistroClienteForm, RegistroMascotaForm
from django.contrib.auth import login
from django.db import transaction
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

from django.contrib import messages
from datetime import timedelta
from .utils import validar_conflicto_horario


# Helper para recepción
def registro_rapido(request):
    """
    Vista para registro rápido de clientes desde el dashboard de recepción.
    
    Permite a recepcionistas y administradores crear nuevos clientes con una
    contraseña temporal predefinida. Incluye auto-formateo de RUT y teléfono.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: Redirect a dashboard_recepcion con mensaje de éxito/error
        
    Permissions:
        - Usuario autenticado
        - Rol: RECEPCIONISTA o ADMIN
        
    POST Parameters:
        - username: RUT del cliente (se usa como username)
        - first_name: Nombre del cliente
        - last_name: Apellido del cliente
        - email: Email del cliente
        - telefono: Teléfono del cliente
        - direccion: Dirección del cliente (opcional)
        - password: Contraseña temporal (predefinida en template)
        - nombre: Nombre de la mascota (opcional)
        - especie: Especie de la mascota (opcional)
        - genero: Género de la mascota (opcional)
        - raza: Raza de la mascota (opcional)
    """
    if not request.user.is_authenticated or request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
        return redirect('index')

    if request.method == 'POST':
        # Importar funciones helper
        from .utils import formatear_rut, formatear_telefono
        
        # Copiamos POST para poder modificarlo
        data = request.POST.copy()
        
        # 1. Auto-formato RUT usando helper
        rut = data.get('username', '').strip()
        if rut:
            rut_formatted = formatear_rut(rut)
            data['username'] = rut_formatted
            data['rut'] = rut_formatted
        
        # 2. Auto-formato Teléfono usando helper
        telefono = data.get('telefono', '').strip()
        if telefono:
            data['telefono'] = formatear_telefono(telefono)
        
        user_form = RegistroUsuarioForm(data)
        cliente_form = RegistroClienteForm(data)
        mascota_form = RegistroMascotaForm(data)

        # RELAX VALIDATION: Remove strict regex validators to avoid UX frustration
        # The auto-formatter attempts to fix it, but if it fails matching strict regex
        # (e.g. foreign ID, short RUT), we generally want to allow it anyway.
        if 'rut' in cliente_form.fields:
            cliente_form.fields['rut'].validators = []
        if 'telefono' in cliente_form.fields:
            cliente_form.fields['telefono'].validators = []

        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if user_form.is_valid() and cliente_form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Crear Usuario
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.rol = Usuario.Roles.CLIENTE
                    user.save()

                    # 2. Crear Perfil Cliente
                    cliente = cliente_form.save(commit=False)
                    cliente.usuario = user
                    cliente.nombre = user.first_name
                    cliente.apellido = user.last_name
                    cliente.email = user.email
                    cliente.save()

                    # 3. Crear Mascota (si se llenaron datos)
                    if mascota_form.is_valid():
                        mascota = mascota_form.save(commit=False)
                        mascota.cliente = cliente
                        mascota.save()

                    if is_ajax:
                        return JsonResponse({'success': True})
                    
                    messages.success(request, f'Cliente {cliente.nombre} registrado exitosamente.')
                    return redirect('dashboard_recepcion')
            except Exception as e:
                if is_ajax:
                    return JsonResponse({'success': False, 'errors': str(e)}, status=400)
                messages.error(request, f"Error al registrar: {e}")
        else:
             # Collect errors
            errors = {} if is_ajax else ""
            
            for field, err in user_form.errors.items():
                msg = [e.message for e in err.as_data()]
                if is_ajax: errors[f"Usuario {field}"] = msg
                else: errors += f"Usuario {field}: {err.as_text()} "
            
            for field, err in cliente_form.errors.items():
                msg = [e.message for e in err.as_data()]
                if is_ajax: errors[f"Cliente {field}"] = msg
                else: errors += f"Cliente {field}: {err.as_text()} "

            for field, err in mascota_form.errors.items():
                msg = [e.message for e in err.as_data()]
                if is_ajax: errors[f"Mascota {field}"] = msg
                else: errors += f"Mascota {field}: {err.as_text()} "
            
            if is_ajax:
                 return JsonResponse({'success': False, 'errors': errors}, status=400)
            
            messages.error(request, f"Formulario inválido. {errors}")
            
    return redirect('dashboard_recepcion')


# --- Standard Views (Frontend) ---

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST'), name='post')
class CustomLoginView(LoginView):
    """
    Vista de login personalizada con rate limiting.
    
    Protección contra fuerza bruta: máximo 5 intentos por minuto por IP.
    """
    template_name = 'clinic/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.rol == 'RECEPCIONISTA' or user.rol == 'ADMIN':
            return reverse_lazy('dashboard_recepcion')
        elif user.rol == 'VETERINARIO':
            return reverse_lazy('dashboard_veterinario')
        else:
            return reverse_lazy('dashboard_cliente')

            return reverse_lazy('dashboard_cliente')

def registro(request):
    """
    Vista de registro público para nuevos clientes.
    
    Permite a usuarios no autenticados crear una cuenta de cliente con su
    primera mascota. Después del registro exitoso, el usuario es autenticado
    automáticamente y redirigido a su dashboard.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: Render del formulario o redirect a dashboard_cliente
        
    Template:
        clinic/registro.html
        
    Context:
        - user_form: RegistroUsuarioForm
        - cliente_form: RegistroClienteForm
        - mascota_form: RegistroMascotaForm
    """
    import logging
    logger = logging.getLogger(__name__)
    
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        logger.info("=== REGISTRO POST REQUEST ===")
        user_form = RegistroUsuarioForm(request.POST)
        cliente_form = RegistroClienteForm(request.POST)
        mascota_form = RegistroMascotaForm(request.POST)

        if user_form.is_valid() and cliente_form.is_valid() and mascota_form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Crear Usuario
                    logger.info("Creating user...")
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.rol = Usuario.Roles.CLIENTE
                    user.save()
                    logger.info(f"User created: {user.username}, ID: {user.id}")

                    # 2. Crear Perfil Cliente
                    logger.info("Creating cliente profile...")
                    cliente = cliente_form.save(commit=False)
                    cliente.usuario = user
                    cliente.nombre = user.first_name
                    cliente.apellido = user.last_name
                    cliente.email = user.email
                    cliente.save()
                    logger.info(f"Cliente created: {cliente}, ID: {cliente.id}")

                    # 3. Crear Mascota
                    logger.info("Creating mascota...")
                    mascota = mascota_form.save(commit=False)
                    mascota.cliente = cliente
                    mascota.save()
                    logger.info(f"Mascota created: {mascota.nombre}, ID: {mascota.id}")

                    # Login y Redirección
                    logger.info("Logging in user...")
                    login(request, user)
                    logger.info(f"User logged in successfully. Redirecting to dashboard_cliente")
                    return redirect('dashboard_cliente')
            except Exception as e:
                # Manejar error de integridad o DB
                logger.error(f"ERROR during registration: {type(e).__name__}: {str(e)}")
                logger.exception("Full traceback:")
                user_form.add_error(None, f"Error al registrar: {e}")
        else:
            logger.warning("Form validation failed")
            if not user_form.is_valid():
                logger.warning(f"User form errors: {user_form.errors}")
            if not cliente_form.is_valid():
                logger.warning(f"Cliente form errors: {cliente_form.errors}")
            if not mascota_form.is_valid():
                logger.warning(f"Mascota form errors: {mascota_form.errors}")

    else:
        user_form = RegistroUsuarioForm()
        cliente_form = RegistroClienteForm()
        mascota_form = RegistroMascotaForm()

    return render(request, 'clinic/registro.html', {
        'user_form': user_form,
        'cliente_form': cliente_form,
        'mascota_form': mascota_form
    })

def index(request):
    return render(request, 'clinic/index.html')

def servicios(request):
    return render(request, 'clinic/servicios.html')

def quienes_somos(request):
    return render(request, 'clinic/quienes_somos.html')

def contacto(request):
    return render(request, 'clinic/contacto.html')

# Dashboards
def dashboard_recepcion(request):
    # Validar rol
    if not request.user.is_authenticated or request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
         return redirect('index')
    
    citas = Cita.objects.all().order_by('fecha_hora')
    vets = Veterinario.objects.all()
    clientes = Cliente.objects.all()
    mascotas = Mascota.objects.all() # Needed for appointment creation dropdown
    espera = ListaEspera.objects.filter(estado='PENDIENTE')
    
    return render(request, 'clinic/dashboard_recepcion.html', {
        'citas': citas, 
        'veterinarios': vets,
        'clientes': clientes,
        'mascotas': mascotas,
        'lista_espera': espera
    })

def dashboard_veterinario(request):
    if not request.user.is_authenticated or request.user.rol != 'VETERINARIO':
         return redirect('index')
    
    try:
        vet = request.user.perfil_veterinario
        citas_hoy = Cita.objects.filter(veterinario=vet).order_by('fecha_hora')
    except:
        citas_hoy = []
    
    return render(request, 'clinic/dashboard_veterinario.html', {'citas': citas_hoy})

def crear_cita_recepcion(request):
    """
    Vista para crear nuevas citas desde el dashboard de recepción.
    
    Valida conflictos de horario antes de crear la cita. Solo accesible
    por recepcionistas y administradores.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: Redirect a dashboard_recepcion con mensaje de éxito/error
        
    Permissions:
        - Usuario autenticado
        - Rol: RECEPCIONISTA o ADMIN
        
    POST Parameters:
        - mascota: ID de la mascota (requerido)
        - veterinario: ID del veterinario (opcional)
        - fecha_hora: Fecha y hora de la cita (requerido)
        - tipo: Tipo de cita (CONSULTA, CONTROL, etc.)
        - motivo: Motivo de la consulta
    """
    if not request.user.is_authenticated or request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
        return redirect('index')
        
    if request.method == 'POST':
        try:
            mascota_id = request.POST.get('mascota')
            veterinario_id = request.POST.get('veterinario')
            fecha_hora = request.POST.get('fecha_hora')
            tipo = request.POST.get('tipo')
            motivo = request.POST.get('motivo', 'Consulta General')
            
            # Basic validation
            if not mascota_id or not fecha_hora:
                messages.error(request, "Faltan datos obligatorios (Mascota o Fecha).")
                return redirect('dashboard_recepcion')
            
            # Validar fecha no pasada
            from django.utils import timezone
            from django.utils.dateparse import parse_datetime
            from .utils import es_feriado_o_domingo
            
            fecha_dt = parse_datetime(fecha_hora)
            if fecha_dt and fecha_dt.date() < timezone.now().date():
                 messages.error(request, "No se pueden agendar citas en fechas pasadas.")
                 return redirect('dashboard_recepcion')

            # Validar urgencia en domingo/feriado
            es_urgencia = request.POST.get('es_urgencia') == 'on'
            es_especial, razon = es_feriado_o_domingo(fecha_dt)
            
            if es_especial and not es_urgencia:
                messages.error(request, f"La fecha seleccionada {razon}. Debe marcar 'Es Urgencia' para continuar.")
                return redirect('dashboard_recepcion')

            # Validar conflicto de horario
            tiene_conflicto, mensaje_conflicto = validar_conflicto_horario(veterinario_id, fecha_hora)
            if tiene_conflicto:
                print(f"DEBUG: Conflicto detectado: {mensaje_conflicto}")
                messages.error(request, mensaje_conflicto)
                return redirect('dashboard_recepcion')

            print(f"DEBUG: Creando cita... Mascota: {mascota_id}, Fecha: {fecha_hora}, Vet: {veterinario_id}, Urgencia: {es_urgencia}")
            cita = Cita.objects.create(
                mascota_id=mascota_id,
                veterinario_id=veterinario_id if veterinario_id else None,
                fecha_hora=fecha_hora,
                tipo=tipo if tipo else 'CONSULTA',
                motivo=motivo,
                estado='AGENDADA',
                es_urgencia=es_urgencia
            )
            print(f"DEBUG: Cita creada con ID: {cita.id}")
            messages.success(request, "Cita agendada correctamente.")
        except Exception as e:
            print(f"DEBUG: EXCEPCIÓN al crear cita: {e}")
            messages.error(request, f"Error al agendar: {e}")
            
    return redirect('dashboard_recepcion')

def cancelar_cita(request, cita_id):
    if not request.user.is_authenticated or request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
        return redirect('index')
    
    try:
        cita = Cita.objects.get(id=cita_id)
        cita.estado = 'CANCELADA'
        cita.save()
        messages.success(request, "Cita cancelada correctamente.")
    except Cita.DoesNotExist:
        messages.error(request, "Cita no encontrada.")
        
    return redirect('dashboard_recepcion')

def reagendar_cita(request, cita_id):
    if not request.user.is_authenticated or request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
        return redirect('index')
    
    if request.method == 'POST':
        try:
            cita = Cita.objects.get(id=cita_id)
            nueva_fecha = request.POST.get('fecha_hora')
            nuevo_vet_id = request.POST.get('veterinario')
            
            # Determinar veterinario y fecha para validación
            vet_id_validar = nuevo_vet_id if nuevo_vet_id else cita.veterinario_id
            fecha_validar = nueva_fecha if nueva_fecha else cita.fecha_hora
            
            # Validar fecha no pasada
            from django.utils import timezone
            from django.utils.dateparse import parse_datetime
            from .utils import es_feriado_o_domingo
            
            if nueva_fecha:
                fecha_dt = parse_datetime(nueva_fecha)
                if fecha_dt and fecha_dt.date() < timezone.now().date():
                     messages.error(request, "No se pueden reagendar citas a fechas pasadas.")
                     return redirect('dashboard_recepcion')
                
                # Validar urgencia en domingo/feriado
                es_urgencia = request.POST.get('es_urgencia') == 'on'
                es_especial, razon = es_feriado_o_domingo(fecha_dt)
                
                if es_especial and not es_urgencia:
                    messages.error(request, f"La fecha seleccionada {razon}. Debe marcar 'Es Urgencia' para continuar.")
                    return redirect('dashboard_recepcion')
                
                cita.es_urgencia = es_urgencia

            # Validar conflicto de horario
            tiene_conflicto, mensaje_conflicto = validar_conflicto_horario(
                vet_id_validar, fecha_validar, cita_id=cita_id
            )
            if tiene_conflicto:
                messages.error(request, mensaje_conflicto)
                return redirect('dashboard_recepcion')
            
            if nueva_fecha:
                cita.fecha_hora = nueva_fecha
                
            if nuevo_vet_id:
                cita.veterinario_id = nuevo_vet_id
            cita.save()
            messages.success(request, f"Cita para {cita.mascota.nombre} reagendada correctamente.")
        except Cita.DoesNotExist:
            messages.error(request, "Error: Cita no encontrada.")
        except Exception as e:
            messages.error(request, f"Error al reagendar: {e}")
            
    return redirect('dashboard_recepcion')

def api_citas_calendario(request):
    """
    Retorna citas en formato JSON para el calendario.
    Opcional: Filtrar por start/end date range si se pasan params.
    """
    if not request.user.is_authenticated or request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
         return JsonResponse({'error': 'Unauthorized'}, status=403)

    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    citas = Cita.objects.filter(estado__in=['AGENDADA', 'CONFIRMADA'])
    
    if start_date and end_date:
        citas = citas.filter(fecha_hora__range=[start_date, end_date])
        
    data = []
    for c in citas:
        # Color coding based on status or type
        color = '#0d6efd' # primary
        if c.estado == 'CONFIRMADA':
            color = '#198754' # success
            
        data.append({
            'id': c.id,
            'title': f"{c.mascota.nombre} ({c.tipo})",
            'start': c.fecha_hora.isoformat(),
            'end': c.fecha_hora.isoformat(), # For point events
            'veterinario': c.veterinario.nombre if c.veterinario else "Sin Asignar",
            'veterinario_id': c.veterinario.id if c.veterinario else "",
            'mascota': c.mascota.nombre,
            'dueño': f"{c.mascota.cliente.nombre} {c.mascota.cliente.apellido}",
            'color': color,
            'tipo': c.tipo,
            'estado': c.estado,
            'motivo': c.motivo
        })
        
    return JsonResponse(data, safe=False)

# Editar Cliente
def editar_cliente(request, cliente_id):
    if not request.user.is_authenticated or request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
        return redirect('index')
    
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        
        if request.method == 'POST':
            cliente.nombre = request.POST.get('nombre', cliente.nombre)
            cliente.apellido = request.POST.get('apellido', cliente.apellido)
            cliente.telefono = request.POST.get('telefono', cliente.telefono)
            cliente.email = request.POST.get('email', cliente.email)
            cliente.direccion = request.POST.get('direccion', cliente.direccion)
            cliente.save()
            messages.success(request, f"Cliente {cliente.nombre} actualizado correctamente.")
        
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente no encontrado.")
    except Exception as e:
        messages.error(request, f"Error al actualizar cliente: {e}")
    
    return redirect('dashboard_recepcion')

# Editar Mascota
def editar_mascota(request, mascota_id):
    if not request.user.is_authenticated:
        return redirect('index')
    
    try:
        mascota = Mascota.objects.get(id=mascota_id)
        
        # Verificar permisos: solo el dueño o recepcionista/admin
        if request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
            if not hasattr(request.user, 'perfil_cliente') or mascota.cliente != request.user.perfil_cliente:
                messages.error(request, "No tienes permiso para editar esta mascota.")
                return redirect('dashboard_cliente')
        
        if request.method == 'POST':
            mascota.nombre = request.POST.get('nombre', mascota.nombre)
            mascota.especie = request.POST.get('especie', mascota.especie)
            mascota.raza = request.POST.get('raza', mascota.raza)
            fecha_nac = request.POST.get('fecha_nacimiento')
            if fecha_nac:
                mascota.fecha_nacimiento = fecha_nac
            mascota.observaciones = request.POST.get('observaciones', mascota.observaciones)
            mascota.save()
            messages.success(request, f"Mascota {mascota.nombre} actualizada correctamente.")
        
    except Mascota.DoesNotExist:
        messages.error(request, "Mascota no encontrada.")
    except Exception as e:
        messages.error(request, f"Error al actualizar mascota: {e}")
    
    # Redirigir según rol
    if request.user.rol in ['RECEPCIONISTA', 'ADMIN']:
        return redirect('dashboard_recepcion')
    return redirect('dashboard_cliente')


def agregar_mascota_cliente(request):
    """
    Vista para que un cliente agregue una nueva mascota desde su dashboard.
    """
    if not request.user.is_authenticated or request.user.rol != 'CLIENTE':
        return redirect('index')
    
    if request.method == 'POST':
        try:
            cliente = request.user.perfil_cliente
            
            # Obtener datos del formulario
            nombre = request.POST.get('nombre', '').strip()
            especie = request.POST.get('especie', 'Perro')
            raza = request.POST.get('raza', '').strip()
            genero = request.POST.get('genero', 'Macho')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            fecha_registro = request.POST.get('fecha_registro')
            observaciones = request.POST.get('observaciones', '').strip()
            
            # Validar campos obligatorios
            if not nombre or not raza:
                messages.error(request, "Nombre y raza son obligatorios.")
                return redirect('dashboard_cliente')
            
            # Crear mascota
            from django.utils import timezone
            mascota = Mascota.objects.create(
                cliente=cliente,
                nombre=nombre,
                especie=especie,
                raza=raza,
                genero=genero,
                fecha_nacimiento=fecha_nacimiento if fecha_nacimiento else None,
                fecha_registro=fecha_registro if fecha_registro else timezone.now().date(),
                observaciones=observaciones
            )
            
            messages.success(request, f"Mascota {mascota.nombre} registrada exitosamente.")
            
        except Exception as e:
            messages.error(request, f"Error al registrar mascota: {e}")
    
    return redirect('dashboard_cliente')


def dashboard_cliente(request):
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"=== DASHBOARD_CLIENTE CALLED ===")
    logger.info(f"User: {request.user}")
    logger.info(f"Is authenticated: {request.user.is_authenticated}")
    logger.info(f"User rol: {getattr(request.user, 'rol', 'NO ROL ATTR')}")
    
    if not request.user.is_authenticated or request.user.rol != 'CLIENTE':
        logger.warning(f"Access denied - redirecting to index")
        return redirect('index')
    
    try:
        logger.info("Attempting to get perfil_cliente...")
        cliente = request.user.perfil_cliente
        logger.info(f"Cliente found: {cliente}")
        
        logger.info("Getting mascotas...")
        mascotas = cliente.mascotas.all()
        logger.info(f"Mascotas count: {mascotas.count()}")
        
        logger.info("Getting citas...")
        citas = Cita.objects.filter(mascota__cliente=cliente).order_by('-fecha_hora')
        logger.info(f"Citas count: {citas.count()}")
    except Exception as e:
        logger.error(f"ERROR getting cliente data: {type(e).__name__}: {str(e)}")
        logger.exception("Full traceback:")
        cliente = None
        mascotas = []
        citas = []

    if request.method == 'POST':
        logger.info("POST request received")
        action = request.POST.get('action')
        logger.info(f"Action: {action}")
        
        if action == 'cancelar':
            cita_id = request.POST.get('cita_id')
            try:
                cita = Cita.objects.get(id=cita_id, mascota__cliente__usuario=request.user)
                if cita.estado != Cita.Estado.CANCELADA:
                    cita.estado = Cita.Estado.CANCELADA
                    cita.save()
                    logger.info(f"Cita {cita_id} cancelled")
            except Cita.DoesNotExist:
                logger.warning(f"Cita {cita_id} not found")
                pass
            return redirect('dashboard_cliente')
            
        # Creación de cita (default behavior if no specific action or implicit creation)
        mascota_id = request.POST.get('mascota')
        vet_id = request.POST.get('veterinario')
        fecha = request.POST.get('fecha_hora')
        motivo = request.POST.get('motivo')
        
        if mascota_id and fecha and motivo:
            Cita.objects.create(
                mascota_id=mascota_id,
                veterinario_id=vet_id if vet_id else None,
                fecha_hora=fecha,
                motivo=motivo,
                estado='AGENDADA'
            )
            messages.success(request, "Cita agendada correctamente.")
            logger.info(f"New cita created for mascota {mascota_id}")
        
        return redirect('dashboard_cliente')
    
    logger.info("Getting veterinarios...")
    veterinarios = Veterinario.objects.all()
    logger.info(f"Veterinarios count: {veterinarios.count()}")
    
    logger.info("Rendering template...")
    return render(request, 'clinic/dashboard_cliente.html', {
        'cliente': cliente,
        'mascotas': mascotas,
        'citas': citas,
        'veterinarios': veterinarios
    })

def historial_mascota(request, mascota_id):
    if not request.user.is_authenticated:
        return redirect('index')
    
    mascota = get_object_or_404(Mascota, id=mascota_id)
    # Historial de atenciones (citas que tienen atención registrada)
    atenciones = Atencion.objects.filter(cita__mascota=mascota).order_by('-fecha')
    # Historial de citas general
    citas = Cita.objects.filter(mascota=mascota).order_by('-fecha_hora')
    
    return render(request, 'clinic/historial_mascota.html', {
        'mascota': mascota,
        'atenciones': atenciones,
        'citas': citas
    })

def registrar_atencion(request, cita_id):
    """
    Vista para registrar atención médica de una cita.
    Solo accesible por veterinarios.
    """
    if not request.user.is_authenticated or request.user.rol != 'VETERINARIO':
        return redirect('index')
    
    if request.method == 'POST':
        try:
            cita = get_object_or_404(Cita, id=cita_id)
            
            # Verificar que el veterinario sea el asignado a la cita
            if cita.veterinario != request.user.perfil_veterinario:
                messages.error(request, "No tienes permiso para atender esta cita.")
                return redirect('dashboard_veterinario')
            
            # Verificar que la cita no haya sido ya atendida
            if hasattr(cita, 'atencion'):
                messages.warning(request, "Esta cita ya tiene una atención registrada.")
                return redirect('dashboard_veterinario')
            
            # Obtener datos del formulario
            diagnostico = request.POST.get('diagnostico', '').strip()
            tratamiento = request.POST.get('tratamiento', '').strip()
            medicamentos = request.POST.get('medicamentos', '').strip()
            costo_estimado = request.POST.get('costo_estimado', 0)
            requiere_operacion = request.POST.get('requiere_operacion') == 'on'
            
            # Validar campos obligatorios
            if not diagnostico or not tratamiento:
                messages.error(request, "Diagnóstico y tratamiento son obligatorios.")
                return redirect('dashboard_veterinario')
            
            # Crear registro de atención
            with transaction.atomic():
                Atencion.objects.create(
                    cita=cita,
                    diagnostico=diagnostico,
                    tratamiento=tratamiento,
                    medicamentos=medicamentos,
                    costo_estimado=costo_estimado if costo_estimado else 0,
                    requiere_operacion=requiere_operacion
                )
                
                # Actualizar estado de la cita
                cita.estado = 'REALIZADA'
                cita.save()
            
            messages.success(request, f"Atención registrada exitosamente para {cita.mascota.nombre}.")
            
        except Exception as e:
            messages.error(request, f"Error al registrar atención: {e}")
    
    return redirect('dashboard_veterinario')


# --- API ViewSets (Backend) ---

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
class VeterinarioViewSet(viewsets.ModelViewSet):
    queryset = Veterinario.objects.all()
    serializer_class = VeterinarioSerializer

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all().order_by('fecha_hora')
    serializer_class = CitaSerializer
    filterset_fields = ['veterinario', 'estado', 'mascota__cliente']

    @action(detail=False, methods=['get'])
    def por_veterinario(self, request):
        vet_id = request.query_params.get('veterinario_id')
        if vet_id:
            citas = Cita.objects.filter(veterinario_id=vet_id)
            serializer = self.get_serializer(citas, many=True)
            return Response(serializer.data)
        return Response([])

class AtencionViewSet(viewsets.ModelViewSet):
    queryset = Atencion.objects.all()
    serializer_class = AtencionSerializer

class ListaEsperaViewSet(viewsets.ModelViewSet):
    queryset = ListaEspera.objects.all()
    serializer_class = ListaEsperaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# --- HU002: API para disponibilidad de horarios ---
def api_disponibilidad_horarios(request):
    """
    API para obtener bloques horarios disponibles para una fecha y veterinario.
    
    Parámetros GET:
        - fecha: Fecha en formato YYYY-MM-DD (requerido)
        - veterinario_id: ID del veterinario (opcional)
    
    Retorna:
        JSON con lista de bloques horarios de 30 minutos (9:00-20:00)
        Cada bloque indica si está disponible u ocupado
    """
    if not request.user.is_authenticated or request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    from datetime import datetime, timedelta
    
    fecha_str = request.GET.get('fecha')
    veterinario_id = request.GET.get('veterinario_id')
    
    if not fecha_str:
        return JsonResponse({'error': 'Fecha requerida'}, status=400)
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}, status=400)
    
    # Generar bloques de 30 minutos de 9:00 a 20:00
    bloques = []
    hora_inicio = 9
    hora_fin = 20
    
    for hora in range(hora_inicio, hora_fin):
        for minuto in [0, 30]:
            inicio = datetime.combine(fecha, datetime.min.time().replace(hour=hora, minute=minuto))
            fin = inicio + timedelta(minutes=30)
            
            # Verificar si hay cita en este bloque
            citas_query = Cita.objects.filter(
                fecha_hora__gte=inicio,
                fecha_hora__lt=fin,
                estado__in=['AGENDADA', 'CONFIRMADA']
            )
            
            if veterinario_id:
                citas_query = citas_query.filter(veterinario_id=veterinario_id)
            
            ocupado = citas_query.exists()
            
            bloques.append({
                'hora': inicio.strftime('%H:%M'),
                'datetime': inicio.isoformat(),
                'disponible': not ocupado
            })
    
    return JsonResponse({'bloques': bloques})


# --- HU006: API para antecedentes de mascota ---
def api_antecedentes_mascota(request, mascota_id):
    """
    API para obtener antecedentes de una mascota.
    
    Retorna:
        JSON con información básica, historial de citas y última atención
    """
    if not request.user.is_authenticated or request.user.rol not in ['RECEPCIONISTA', 'ADMIN']:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        mascota = Mascota.objects.get(id=mascota_id)
        
        # Información básica
        info_basica = {
            'nombre': mascota.nombre,
            'especie': mascota.especie,
            'raza': mascota.raza,
            'genero': mascota.genero,
            'edad': mascota.edad_aprox,
            'observaciones': mascota.observaciones
        }
        
        # Últimas 5 citas
        citas = Cita.objects.filter(mascota=mascota).order_by('-fecha_hora')[:5]
        historial_citas = [{
            'fecha': c.fecha_hora.strftime('%d/%m/%Y %H:%M'),
            'tipo': c.get_tipo_display(),
            'estado': c.get_estado_display(),
            'veterinario': c.veterinario.nombre if c.veterinario else 'Sin asignar',
            'motivo': c.motivo
        } for c in citas]
        
        # Última atención médica
        ultima_atencion = None
        try:
            atencion = Atencion.objects.filter(cita__mascota=mascota).order_by('-fecha').first()
            if atencion:
                ultima_atencion = {
                    'fecha': atencion.fecha.strftime('%d/%m/%Y'),
                    'diagnostico': atencion.diagnostico,
                    'tratamiento': atencion.tratamiento,
                    'medicamentos': atencion.medicamentos,
                    'requiere_operacion': atencion.requiere_operacion
                }
        except:
            pass
        
        return JsonResponse({
            'info_basica': info_basica,
            'historial_citas': historial_citas,
            'ultima_atencion': ultima_atencion
        })
        
    except Mascota.DoesNotExist:
        return JsonResponse({'error': 'Mascota no encontrada'}, status=404)


# --- HU006: Cancelación de cita por veterinario ---
def cancelar_cita_veterinario(request, cita_id):
    """
    Vista para que un veterinario cancele una cita con motivo.
    Registra quién canceló y el motivo.
    """
    if not request.user.is_authenticated or request.user.rol != 'VETERINARIO':
        return redirect('index')
    
    if request.method == 'POST':
        try:
            from django.utils import timezone
            
            cita = Cita.objects.get(id=cita_id)
            
            # Verificar que el veterinario sea el asignado
            if cita.veterinario != request.user.perfil_veterinario:
                messages.error(request, "No tienes permiso para cancelar esta cita.")
                return redirect('dashboard_veterinario')
            
            motivo = request.POST.get('motivo_cancelacion', '').strip()
            
            if not motivo:
                messages.error(request, "Debe proporcionar un motivo de cancelación.")
                return redirect('dashboard_veterinario')
            
            # Actualizar cita
            cita.estado = 'CANCELADA'
            cita.cancelado_por = 'VETERINARIO'
            cita.motivo_cancelacion = motivo
            cita.fecha_cancelacion = timezone.now()
            cita.save()
            
            messages.success(request, f"Cita cancelada. Se notificará al cliente: {cita.mascota.cliente.nombre}")
            
        except Cita.DoesNotExist:
            messages.error(request, "Cita no encontrada.")
        except Exception as e:
            messages.error(request, f"Error al cancelar cita: {e}")
    
    return redirect('dashboard_veterinario')

