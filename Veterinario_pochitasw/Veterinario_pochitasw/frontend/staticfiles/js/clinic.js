document.addEventListener('DOMContentLoaded', function () {
    const calendarGrid = document.getElementById('calendar-grid');
    if (calendarGrid) {
        initCalendar();
        loadAppointments();
    }
});

let currentView = 'list';

function switchView(view) {
    currentView = view;
    document.getElementById('btn-view-list').classList.toggle('active', view === 'list');
    document.getElementById('btn-view-calendar').classList.toggle('active', view === 'calendar');

    document.getElementById('list-view').style.display = view === 'list' ? 'block' : 'none';
    document.getElementById('calendar-view').style.display = view === 'calendar' ? 'block' : 'none';
}

function initCalendar() {
    const grid = document.getElementById('calendar-grid');
    grid.innerHTML = ''; // Clear

    // Generate Time Slots (Rows)
    // 9:00 to 20:00 (11 hours)
    for (let h = 9; h < 20; h++) {
        // Time Label Column
        const timeLabel = document.createElement('div');
        timeLabel.className = 'time-slot fw-bold bg-light';
        timeLabel.innerText = `${h}:00`;
        grid.appendChild(timeLabel);

        // 6 Day Columns (Mon-Sat)
        for (let d = 0; d < 6; d++) {
            const cell = document.createElement('div');
            cell.className = 'day-column';
            cell.dataset.day = d; // 0=Mon, 5=Sat
            cell.dataset.hour = h;
            cell.style.position = 'relative';
            grid.appendChild(cell);
        }
    }
}

function loadAppointments() {
    fetch('/api/citas/calendario/')
        .then(response => response.json())
        .then(data => {
            renderEvents(data);
        })
        .catch(error => console.error('Error loading calendar:', error));
}

function renderEvents(events) {
    // Clear previous events if needed, but here we just append to the grid structure
    // Actually, we should clear only events, but our initCalendar clears everything.
    // So we just iterate and append to the correct cells.

    // The grid is: TimeCol, Mon, Tue... Sat. Total 7 cols.
    // We need to find the correct cell by day and hour.

    const grid = document.getElementById('calendar-grid');
    const dayColumns = document.querySelectorAll('.day-column');

    events.forEach(event => {
        const date = new Date(event.start);

        // Adjust for timezone offset if necessary, or assume server sends ISO local time
        // JS Date parsing might shift to local. 

        // Get Day of week (0=Sun, 1=Mon...)
        let day = date.getDay();
        if (day === 0) return; // Sunday hidden
        day = day - 1; // 0=Mon, 5=Sat

        const hour = date.getHours();

        if (hour < 9 || hour >= 20) return; // Out of bounds

        // Find the specific cell (Day + Hour)
        // Helper: The grid is flat divs.
        // But we added dataset attributes.
        const targetCell = Array.from(dayColumns).find(c => c.dataset.day == day && c.dataset.hour == hour);

        if (targetCell) {
            const el = document.createElement('div');
            el.className = 'calendar-event';
            el.style.backgroundColor = event.color;
            el.innerText = `${event.start.slice(11, 16)} ${event.mascota}`;
            el.title = `${event.title} - ${event.dueño}`;

            // Calculate top percent based on minutes
            const minutes = date.getMinutes();
            const topPct = (minutes / 60) * 100;
            el.style.top = `${topPct}%`;
            el.style.height = '45px'; // Fixed height 45min roughly

            // Interaction: Open Reschedule Modal
            el.onclick = () => openRescheduleModal(event);

            targetCell.appendChild(el);
        }
    });
}

/**
 * Inicializa el modal de atención veterinaria.
 * Pasa el ID de la cita y el nombre de la mascota al formulario.
 */
function initAtencionModal() {
    const atenderButtons = document.querySelectorAll('.atender-btn');
    const atencionForm = document.getElementById('atencionForm');
    const modalMascotaNombre = document.getElementById('modalMascotaNombre');

    if (!atencionForm) return; // No estamos en el dashboard veterinario

    atenderButtons.forEach(button => {
        button.addEventListener('click', function () {
            const citaId = this.getAttribute('data-cita-id');
            const mascotaNombre = this.getAttribute('data-mascota');

            // Actualizar action del formulario
            atencionForm.action = `/api/dashboard/veterinario/atender/${citaId}/`;

            // Actualizar nombre de mascota en el título
            if (modalMascotaNombre) {
                modalMascotaNombre.textContent = mascotaNombre;
            }
        });
    });
}

// Inicializar modal de atención cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
    initAtencionModal();
});

function openRescheduleModal(eventObj) {
    // Determine if passed object is raw event or custom obj
    let id, start, vetId, mascota;

    if (eventObj.id) {
        // From Calendar
        id = eventObj.id;
        // Format ISO date for input datetime-local: YYYY-MM-DDTHH:mm
        start = eventObj.start.substring(0, 16);
        vetId = eventObj.veterinario_id;
        mascota = eventObj.mascota;
    } else {
        // Fallback or manual trigger
        console.error("Invalid event object");
        return;
    }

    document.getElementById('reagendarCitaId').value = id;
    document.getElementById('reagendarFecha').value = start;
    document.getElementById('reagendarVeterinario').value = vetId || "";
    document.getElementById('reagendarMascota').innerText = mascota;

    // Set Action URL dynamically
    const form = document.getElementById('reagendarForm');
    form.action = `/api/dashboard/reagendar_cita/${id}/`;

    const modal = new bootstrap.Modal(document.getElementById('reagendarModal'));
    modal.show();
}


