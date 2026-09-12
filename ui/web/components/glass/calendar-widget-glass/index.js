const daysGrid = document.getElementById('daysGrid');
const agendaTitle = document.getElementById('agendaTitle');
const agendaMeta = document.getElementById('agendaMeta');

const eventsMap = {
    12: { title: 'Agent Architecture Review', meta: 'Enclave cluster synchronization demo' },
    15: { title: 'Model Quantization Sprint', meta: 'FlashAttention-3 FP8 benchmark' },
    24: { title: 'Mainnet Security Audit', meta: 'Zero-Knowledge verification check' }
};

let selectedDay = 12;

function renderDays() {
    daysGrid.innerHTML = '';
    // Sep 2026 starts on Tuesday (1 offset)
    // Prev month padding (31st of Aug)
    const prevCell = document.createElement('div');
    prevCell.className = 'cal-day-cell other-month';
    prevCell.textContent = '31';
    daysGrid.appendChild(prevCell);

    for (let day = 1; day <= 30; day++) {
        const cell = document.createElement('div');
        cell.className = 'cal-day-cell';
        if (day === 12) cell.classList.add('today');
        if (day === selectedDay) cell.classList.add('selected');
        cell.textContent = day;

        if (eventsMap[day]) {
            const dot = document.createElement('span');
            dot.className = 'event-dot';
            cell.appendChild(dot);
        }

        cell.addEventListener('click', () => {
            document.querySelectorAll('.cal-day-cell').forEach(c => c.classList.remove('selected'));
            cell.classList.add('selected');
            selectedDay = day;
            if (eventsMap[day]) {
                agendaTitle.textContent = eventsMap[day].title;
                agendaMeta.textContent = eventsMap[day].meta;
            } else {
                agendaTitle.textContent = `Schedule for Sep ${day}`;
                agendaMeta.textContent = 'No critical incidents scheduled';
            }
        });

        daysGrid.appendChild(cell);
    }
}
renderDays();