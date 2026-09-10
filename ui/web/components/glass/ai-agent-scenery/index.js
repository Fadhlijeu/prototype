lucide.createIcons();
        function selectModel(el) {
            document.querySelectorAll('.model-item').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
        }