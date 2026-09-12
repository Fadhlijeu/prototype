document.querySelectorAll('.glass-toast').forEach(toast => {
    toast.addEventListener('click', () => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        setTimeout(() => toast.remove(), 250);
    });
});
if (window.lucide) {
    window.lucide.createIcons();
}
