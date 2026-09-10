lucide.createIcons();
        function select(el) {
            document.querySelectorAll('.model-item').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
        }