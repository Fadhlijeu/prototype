/**
 * Glass Floating Dropdown Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const wrap = document.getElementById('dropWrap');
    const trigger = document.getElementById('dropdownTrigger');
    const label = document.getElementById('selectedLabel');
    const triggerIcon = document.getElementById('triggerIcon');
    const items = document.querySelectorAll('.dropdown-item');

    if (trigger && wrap) {
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            wrap.classList.toggle('open');
        });
    }

    items.forEach(item => {
        item.addEventListener('click', (e) => {
            e.stopPropagation();
            items.forEach(i => i.classList.remove('selected'));
            item.classList.add('selected');

            const val = item.getAttribute('data-value');
            const icon = item.getAttribute('data-icon');

            if (label) label.textContent = val;
            if (triggerIcon) {
                triggerIcon.setAttribute('data-lucide', icon);
                if (window.lucide) window.lucide.createIcons();
            }

            wrap.classList.remove('open');
        });
    });

    document.addEventListener('click', (e) => {
        if (wrap && !wrap.contains(e.target)) {
            wrap.classList.remove('open');
        }
    });
});
