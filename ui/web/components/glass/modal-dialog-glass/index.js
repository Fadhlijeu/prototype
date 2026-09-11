if (window.lucide) window.lucide.createIcons();

let modalFbTimer = null;
function handleModalAction(type, msg) {
    const fb = document.getElementById('modalFeedback');
    if (!fb) return;
    fb.className = `modal-status-feedback ${type}`;
    fb.innerHTML = type === 'confirm' ? `<i data-lucide="check-circle-2"></i> ${msg}` :
                   type === 'cancel' ? `<i data-lucide="x-circle"></i> ${msg}` :
                   `<i data-lucide="info"></i> ${msg}`;
    if (window.lucide) lucide.createIcons();
    clearTimeout(modalFbTimer);
    modalFbTimer = setTimeout(() => {
        fb.className = 'modal-status-feedback';
    }, 2600);
}
