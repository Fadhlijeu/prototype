document.addEventListener('DOMContentLoaded', () => {
            if (window.lucide) window.lucide.createIcons();
            const btn = document.getElementById('btn-action');
            if (btn) {
                btn.addEventListener('click', () => {
                    btn.classList.toggle('active');
                });
            }
        });