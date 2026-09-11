/**
 * Glass Form Input Fields Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const passInput = document.getElementById('passInput');
    const togglePassBtn = document.getElementById('togglePassBtn');
    const eyeIcon = document.getElementById('eyeIcon');

    if (togglePassBtn && passInput && eyeIcon) {
        togglePassBtn.addEventListener('click', () => {
            if (passInput.type === 'password') {
                passInput.type = 'text';
                eyeIcon.setAttribute('data-lucide', 'eye-off');
            } else {
                passInput.type = 'password';
                eyeIcon.setAttribute('data-lucide', 'eye');
            }
            if (window.lucide) window.lucide.createIcons();
        });
    }
});
