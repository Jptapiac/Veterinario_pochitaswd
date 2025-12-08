
@api_view(['POST'])
@login_required
def guardar_atencion(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)
        
        # Validar que sea el veterinario asignado o admin (opcional)
        # if cita.veterinario and cita.veterinario.usuario != request.user: ...

        data = request.data
        
        # Crear Atención
        atencion = Atencion.objects.create(
            cita=cita,
            diagnostico=data.get('diagnostico'),
            tratamiento=data.get('tratamiento'),
            medicamentos=data.get('medicamentos', ''),
            costo_estimado=data.get('costo_estimado', 0) or 0,
            requiere_operacion=data.get('requiere_operacion', False) == 'on' or data.get('requiere_operacion') is True
        )
        
        # Actualizar estado de la cita
        cita.estado = Cita.Estado.REALIZADA
        cita.save()
        
        return Response({'message': 'Atención guardada correctamente', 'atencion_id': atencion.id}, status=201)
    except Cita.DoesNotExist:
        return Response({'error': 'Cita no encontrada'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
