/**
 * Prompt Pills Row Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const pills = document.querySelectorAll('.pill');
    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            const action = pill.querySelector('span')?.innerText || 'Pill';
            alert('Action: ' + action);
        });
    });
});
