"""
Utilidades y funciones helper para la aplicación de clínica veterinaria.
"""


def formatear_rut(rut_input):
    """
    Formatea un RUT chileno al formato estándar XX.XXX.XXX-Y.
    
    Args:
        rut_input (str): RUT sin formato o con formato parcial
        
    Returns:
        str: RUT formateado como XX.XXX.XXX-Y, o el input original si falla
        
    Examples:
        >>> formatear_rut("123456789")
        "12.345.678-9"
        >>> formatear_rut("12345678-9")
        "12.345.678-9"
    """
    if not rut_input:
        return rut_input
    
    # Limpiar RUT: quitar puntos, guiones y espacios
    rut_clean = rut_input.replace('.', '').replace('-', '').replace(' ', '').strip()
    
    if len(rut_clean) < 2:
        return rut_input
    
    try:
        # Separar cuerpo y dígito verificador
        body, dv = rut_clean[:-1], rut_clean[-1].upper()
        
        # Agregar puntos cada 3 dígitos desde la derecha
        reversed_body = body[::-1]
        chunks = [reversed_body[i:i+3] for i in range(0, len(reversed_body), 3)]
        dotted = '.'.join(chunks)[::-1]
        
        return f"{dotted}-{dv}"
    except Exception:
        # Si falla el formateo, intentar formato simple
        try:
            body, dv = rut_clean[:-1], rut_clean[-1].upper()
            return f"{body}-{dv}"
        except Exception:
            return rut_input


def formatear_telefono(telefono_input):
    """
    Formatea un número de teléfono chileno al formato +56XXXXXXXXX.
    
    Args:
        telefono_input (str): Número de teléfono sin formato o con formato parcial
        
    Returns:
        str: Teléfono formateado como +56XXXXXXXXX
        
    Examples:
        >>> formatear_telefono("912345678")
        "+56912345678"
        >>> formatear_telefono("+56912345678")
        "+56912345678"
        >>> formatear_telefono("56912345678")
        "+56912345678"
    """
    if not telefono_input:
        return telefono_input
    
    # Limpiar: solo dígitos y el símbolo +
    tel_clean = ''.join(c for c in telefono_input if c.isdigit() or c == '+').strip()
    
    # Si ya tiene +56, dejarlo así
    if tel_clean.startswith('+56'):
        return tel_clean
    
    # Si empieza con 56, agregar +
    if tel_clean.startswith('56'):
        return f"+{tel_clean}"
    
    # Si es un número de 7-9 dígitos, agregar +56
    if len(tel_clean) >= 7:
        # Si empieza con 9, agregar +56
        if tel_clean.startswith('9'):
            return f"+56{tel_clean}"
        # Si no, agregar +569
        else:
            return f"+569{tel_clean}"
    
    # Dejar el original si no cumple ningún patrón
    return tel_clean if tel_clean else telefono_input


def validar_conflicto_horario(veterinario_id, fecha_hora, cita_id=None):
    """
    Valida si existe un conflicto de horario para un veterinario.
    Asume citas de 30 minutos de duración.
    
    Args:
        veterinario_id (int): ID del veterinario
        fecha_hora (datetime|str): Fecha y hora de la cita
        cita_id (int, optional): ID de la cita actual (para excluir al reagendar)
    
    Returns:
        tuple: (tiene_conflicto: bool, mensaje: str)
        
    Examples:
        >>> validar_conflicto_horario(1, "2025-12-07 10:00:00")
        (False, "")
        >>> validar_conflicto_horario(1, "2025-12-07 10:00:00")  # Si ya existe cita
        (True, "Conflicto: El veterinario ya tiene una cita a las 10:00")
    """
    from datetime import timedelta
    from django.utils.dateparse import parse_datetime
    from .models import Cita
    
    if not veterinario_id or not fecha_hora:
        return False, ""
    
    # Convertir string a datetime si es necesario
    if isinstance(fecha_hora, str):
        fecha_hora = parse_datetime(fecha_hora)
    
    # Rango de 30 minutos antes y después
    inicio_ventana = fecha_hora - timedelta(minutes=30)
    fin_ventana = fecha_hora + timedelta(minutes=30)
    
    # Buscar citas del mismo veterinario en ese rango
    # Usamos gt y lt para permitir citas contiguas (que terminan justo cuando empieza la otra)
    # Rango de conflicto: (fecha_hora - 30min) < cita_existente < (fecha_hora + 30min)
    citas_conflicto = Cita.objects.filter(
        veterinario_id=veterinario_id,
        fecha_hora__gt=inicio_ventana,
        fecha_hora__lt=fin_ventana,
        estado__in=['AGENDADA', 'CONFIRMADA']
    )
    
    # Excluir la cita actual si estamos reagendando
    if cita_id:
        citas_conflicto = citas_conflicto.exclude(id=cita_id)
    
    if citas_conflicto.exists():
        cita = citas_conflicto.first()
        return True, f"Conflicto: El veterinario ya tiene una cita a las {cita.fecha_hora.strftime('%H:%M')}"
    
    return False, ""


def es_feriado_o_domingo(fecha):
    """
    Verifica si una fecha es domingo o feriado en Chile (2024-2025).
    
    Args:
        fecha (date/datetime): Fecha a verificar
        
    Returns:
        tuple: (es_especial: bool, razon: str)
    """
    # Si es datetime, obtener date
    if hasattr(fecha, 'date'):
        fecha = fecha.date()
        
    # Verificar Domingo (weekday 6)
    if fecha.weekday() == 6:
        return True, "Es Domingo"
        
    # Lista de feriados Chile 2024-2025 (Hardcoded por simplicidad)
    feriados = [
        # 2024
        '2024-01-01', '2024-03-29', '2024-03-30', '2024-05-01', '2024-05-21',
        '2024-06-09', '2024-06-20', '2024-07-16', '2024-08-15', '2024-09-18',
        '2024-09-19', '2024-09-20', '2024-10-12', '2024-10-27', '2024-10-31',
        '2024-11-01', '2024-12-08', '2024-12-25',
        # 2025
        '2025-01-01', '2025-04-18', '2025-04-19', '2025-05-01', '2025-05-21',
        '2025-06-20', '2025-06-29', '2025-07-16', '2025-08-15', '2025-09-18',
        '2025-09-19', '2025-10-12', '2025-10-31', '2025-11-01', '2025-12-08',
        '2025-12-25'
    ]
    
    fecha_str = fecha.strftime('%Y-%m-%d')
    if fecha_str in feriados:
        return True, "Es Feriado"
        
    return False, ""
