
document.querySelectorAll('.btn-glass').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.style.transform = 'scale(0.94)';
        setTimeout(() => btn.style.transform = '', 150);
    });
});
