
@login_required
def historial_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    # Verificar permisos: dueño o personal
    if request.user.rol == 'CLIENTE' and mascota.cliente.usuario != request.user:
        messages.error(request, "No tienes permiso para ver esta mascota.")
        return redirect('dashboard_cliente')
        
    atenciones = Atencion.objects.filter(cita__mascota=mascota).select_related('cita', 'cita__veterinario').order_by('-fecha')
    
    return render(request, 'clinic/historial_mascota.html', {
        'mascota': mascota,
        'atenciones': atenciones
    })
