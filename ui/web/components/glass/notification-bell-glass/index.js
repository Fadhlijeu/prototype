const btnClear = document.getElementById('btnClearAll');
const badge = document.getElementById('bellBadge');
const items = document.querySelectorAll('.notif-item');

btnClear.addEventListener('click', () => {
    items.forEach(item => {
        item.classList.remove('unread');
        item.classList.add('read');
    });
    badge.style.display = 'none';
});