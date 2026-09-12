/**
 * AI Model Selector Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    function attachSelectHandlers() {
        document.querySelectorAll('.model-item').forEach(item => {
            item.onclick = function() {
                document.querySelectorAll('.model-item').forEach(i => i.classList.remove('active'));
                this.classList.add('active');
            };
        });
    }

    attachSelectHandlers();
});