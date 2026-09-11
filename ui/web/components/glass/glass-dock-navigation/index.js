lucide.createIcons();
        const dock = document.querySelector('.glass-dock');
        const items = document.querySelectorAll('.nav-item');

        function updatePill(el) {
            if (!el) return;
            dock.style.setProperty('--pill-left', `${el.offsetLeft}px`);
            dock.style.setProperty('--pill-top', `${el.offsetTop}px`);
            dock.style.setProperty('--pill-width', `${el.offsetWidth}px`);
            dock.style.setProperty('--pill-height', `${el.offsetHeight}px`);
        }

        function switchNav(el) {
            items.forEach(i => i.classList.remove('active'));
            el.classList.add('active');
            updatePill(el);
        }

        window.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => updatePill(document.querySelector('.nav-item.active')), 50);
        });
        window.addEventListener('resize', () => {
            updatePill(document.querySelector('.nav-item.active'));
        });

        let dockToastTimer = null;
        function handleFabAction() {
            const toast = document.getElementById('dockToast');
            if (!toast) return;
            toast.classList.add('show');
            clearTimeout(dockToastTimer);
            dockToastTimer = setTimeout(() => {
                toast.classList.remove('show');
            }, 2200);
        }