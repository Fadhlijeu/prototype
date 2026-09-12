const fab = document.getElementById('btnRadialCenter');
const container = document.querySelector('.radial-orbit-container');
const toast = document.getElementById('radialToast');
const satellites = document.querySelectorAll('.radial-satellite');

let isOpen = false;
const radius = 95; // px distance from center

function toggleRadial() {
    isOpen = !isOpen;
    container.classList.toggle('open', isOpen);

    satellites.forEach((sat, idx) => {
        if (isOpen) {
            const angle = parseInt(sat.dataset.angle) * (Math.PI / 180);
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;
            
            setTimeout(() => {
                sat.style.opacity = '1';
                sat.style.pointerEvents = 'auto';
                sat.style.transform = `translate(${x}px, ${y}px) scale(1)`;
            }, idx * 40);
        } else {
            sat.style.opacity = '0';
            sat.style.pointerEvents = 'none';
            sat.style.transform = 'translate(0, 0) scale(0.4)';
        }
    });
}

fab.addEventListener('click', toggleRadial);

satellites.forEach(sat => {
    sat.addEventListener('click', () => {
        const label = sat.dataset.label;
        toast.innerHTML = `Action: <strong>${label}</strong> triggered`;
        toast.classList.add('visible');
        setTimeout(() => toast.classList.remove('visible'), 2400);
        toggleRadial();
    });
});