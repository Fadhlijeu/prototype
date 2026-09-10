lucide.createIcons();
        function activate(el) {
            document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
        }