/**
 * Thinking Effort Selector Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const wrapper = document.getElementById('thinkingWrapper');
    const trigger = document.getElementById('thinkingTrigger');
    const badge = document.getElementById('activeLevelBadge');
    const items = document.querySelectorAll('.level-item');

    if (trigger && wrapper) {
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            wrapper.classList.toggle('open');
        });
    }

    items.forEach(item => {
        item.addEventListener('click', (e) => {
            e.stopPropagation();
            items.forEach(el => el.classList.remove('active'));
            item.classList.add('active');

            const level = item.getAttribute('data-level');
            if (badge) badge.textContent = level;

            wrapper.classList.remove('open');
        });
    });

    document.addEventListener('click', (e) => {
        if (wrapper && !wrapper.contains(e.target)) {
            wrapper.classList.remove('open');
        }
    });
});