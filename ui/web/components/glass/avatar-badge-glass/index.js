/**
 * Glass Avatar with Status Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const buttons = document.querySelectorAll('.btn-status-pill');
    const dot = document.getElementById('mainStatusDot');
    const dotText = document.getElementById('liveDotText');
    const label = document.getElementById('statusLabel');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const mode = btn.getAttribute('data-mode');
            if (mode === 'online') {
                if (dot) {
                    dot.style.background = '#10B981';
                    dot.style.boxShadow = '0 0 12px #10B981';
                }
                if (dotText) dotText.style.background = '#10B981';
                if (label) label.textContent = 'Online — Aktif Mensintesis Data';
            } else if (mode === 'busy') {
                if (dot) {
                    dot.style.background = '#F59E0B';
                    dot.style.boxShadow = '0 0 12px #F59E0B';
                }
                if (dotText) dotText.style.background = '#F59E0B';
                if (label) label.textContent = 'Berpikir — Proses Penalaran Mendalam';
            } else if (mode === 'dnd') {
                if (dot) {
                    dot.style.background = '#EF4444';
                    dot.style.boxShadow = '0 0 12px #EF4444';
                }
                if (dotText) dotText.style.background = '#EF4444';
                if (label) label.textContent = 'DND — Jangan Ganggu (Silent)';
            }
        });
    });
});
