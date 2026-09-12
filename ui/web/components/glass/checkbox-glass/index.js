document.querySelectorAll('.check-item').forEach(item => {
    item.addEventListener('click', () => {
        item.classList.toggle('active');
    });
});
