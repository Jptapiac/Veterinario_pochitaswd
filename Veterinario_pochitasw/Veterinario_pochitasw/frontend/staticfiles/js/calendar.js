// Calendar functions - Global scope
window.currentDate = new Date();

// Chilean holidays 2024-2025
window.chileanHolidays = {
    '2024-01-01': 'Año Nuevo',
    '2024-03-29': 'Viernes Santo',
    '2024-03-30': 'Sábado Santo',
    '2024-05-01': 'Día del Trabajo',
    '2024-05-21': 'Glorias Navales',
    '2024-06-20': 'Pueblos Indígenas',
    '2024-06-29': 'San Pedro y San Pablo',
    '2024-07-16': 'Virgen del Carmen',
    '2024-08-15': 'Asunción de la Virgen',
    '2024-09-18': 'Independencia',
    '2024-09-19': 'Glorias del Ejército',
    '2024-09-20': 'Fiestas Patrias',
    '2024-10-12': 'Encuentro Dos Mundos',
    '2024-10-31': 'Iglesias Evangélicas',
    '2024-11-01': 'Todos los Santos',
    '2024-12-08': 'Inmaculada Concepción',
    '2024-12-25': 'Navidad',
    '2025-01-01': 'Año Nuevo',
    '2025-04-18': 'Viernes Santo',
    '2025-04-19': 'Sábado Santo',
    '2025-05-01': 'Día del Trabajo',
    '2025-05-21': 'Glorias Navales',
    '2025-06-20': 'Pueblos Indígenas',
    '2025-06-29': 'San Pedro y San Pablo',
    '2025-07-16': 'Virgen del Carmen',
    '2025-08-15': 'Asunción de la Virgen',
    '2025-09-18': 'Independencia',
    '2025-09-19': 'Glorias del Ejército',
    '2025-10-12': 'Encuentro Dos Mundos',
    '2025-10-31': 'Iglesias Evangélicas',
    '2025-11-01': 'Todos los Santos',
    '2025-12-08': 'Inmaculada Concepción',
    '2025-12-25': 'Navidad'
};

window.switchView = function (view) {
    console.log('Switching to view:', view);

    // Update buttons
    var btnList = document.getElementById('btn-view-list');
    var btnWeek = document.getElementById('btn-view-week');
    var btnMonth = document.getElementById('btn-view-month');

    if (btnList) btnList.classList.remove('active');
    if (btnWeek) btnWeek.classList.remove('active');
    if (btnMonth) btnMonth.classList.remove('active');

    if (view === 'list' && btnList) btnList.classList.add('active');
    if (view === 'week' && btnWeek) btnWeek.classList.add('active');
    if (view === 'month' && btnMonth) btnMonth.classList.add('active');

    // Show/hide views
    var listView = document.getElementById('list-view');
    var weekView = document.getElementById('calendar-view');
    var monthView = document.getElementById('month-view');

    if (listView) listView.style.display = view === 'list' ? 'block' : 'none';
    if (weekView) weekView.style.display = view === 'week' ? 'block' : 'none';
    if (monthView) monthView.style.display = view === 'month' ? 'block' : 'none';

    if (view === 'month') {
        window.renderMonthCalendar();
    }

    console.log('View switched successfully');
};

window.navigateMonth = function (direction) {
    window.currentDate.setMonth(window.currentDate.getMonth() + direction);
    window.renderMonthCalendar();
};

window.renderMonthCalendar = function () {
    var year = window.currentDate.getFullYear();
    var month = window.currentDate.getMonth();

    // Update title
    var monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    var titleEl = document.getElementById('current-month-title');
    if (titleEl) {
        titleEl.textContent = monthNames[month] + ' ' + year;
    }

    // Get calendar info
    var firstDay = new Date(year, month, 1);
    var lastDay = new Date(year, month + 1, 0);
    var daysInMonth = lastDay.getDate();
    var startingDayOfWeek = firstDay.getDay();

    // Get grid
    var grid = document.querySelector('.calendar-month-grid');
    if (!grid) return;

    // Remove old cells (keep headers)
    var oldCells = grid.querySelectorAll('.calendar-day-cell');
    for (var i = 0; i < oldCells.length; i++) {
        oldCells[i].remove();
    }

    // Add empty cells for days before month starts
    for (var i = 0; i < startingDayOfWeek; i++) {
        var emptyCell = document.createElement('div');
        emptyCell.className = 'calendar-day-cell other-month';
        grid.appendChild(emptyCell);
    }

    // Add cells for each day of the month
    var today = new Date();
    for (var day = 1; day <= daysInMonth; day++) {
        var dateStr = year + '-' + String(month + 1).padStart(2, '0') + '-' + String(day).padStart(2, '0');
        var cell = document.createElement('div');
        cell.className = 'calendar-day-cell';

        // Check if today
        if (year === today.getFullYear() && month === today.getMonth() && day === today.getDate()) {
            cell.classList.add('today');
        }

        // Check if weekend
        var dayOfWeek = new Date(year, month, day).getDay();
        if (dayOfWeek === 0 || dayOfWeek === 6) {
            cell.classList.add('weekend');
        }

        // Check if holiday
        if (window.chileanHolidays[dateStr]) {
            cell.classList.add('holiday');
        }

        var dayNumber = document.createElement('span');
        dayNumber.className = 'day-number';
        dayNumber.textContent = day;
        cell.appendChild(dayNumber);

        // Add holiday name if exists
        if (window.chileanHolidays[dateStr]) {
            var holidayName = document.createElement('span');
            holidayName.className = 'holiday-name';
            holidayName.textContent = window.chileanHolidays[dateStr];
            cell.appendChild(holidayName);
        }

        grid.appendChild(cell);
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('month-view')) {
        window.renderMonthCalendar();
    }
});
