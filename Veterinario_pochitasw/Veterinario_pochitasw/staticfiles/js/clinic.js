document.addEventListener('DOMContentLoaded', function () {
    const citaForm = document.querySelector('#nuevaCitaModal form');
    if (citaForm) {
        // Populate Veterinarios or other dynamic selects if needed
        // For now, handling submit
        const saveBtn = document.querySelector('#nuevaCitaModal .btn-primary');
        saveBtn.addEventListener('click', function () {
            // Simple gathering of values - in a real app use FormData or individual IDs
            // This is a mockup script for the prototype logic
            alert('Funcionalidad de Agendar en Prototipo: Los datos se enviarían a /api/citas/ vía POST.\n\nJSON:\n{\n  "veterinario": ...,\n  "mascota": ...,\n  "fecha_hora": ...\n}');

            // Cerrar modal
            const modalEl = document.getElementById('nuevaCitaModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();

            // Recargar para simular
            location.reload();
        });
    }
});
