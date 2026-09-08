/**
 * Chat Input Bar Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const form = document.querySelector('.chat-input-bar');
    const input = document.getElementById('chatInput');

    if (form && input) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const val = input.value.trim();
            if (!val) return;
            alert('Prompt sent: ' + val);
            input.value = '';
        });
    }
});
