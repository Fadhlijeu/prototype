const scene = document.getElementById('cardScene');
const flipper = document.getElementById('cardFlipper');
const foil = document.getElementById('cardFoil');

let isFlipped = false;

// 3D Parallax Tilt
scene.addEventListener('mousemove', (e) => {
    if (isFlipped) return;
    const rect = scene.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rotateX = ((y - centerY) / centerY) * -14;
    const rotateY = ((x - centerX) / centerX) * 14;
    
    flipper.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    foil.style.transform = `translate(${x * 0.4}px, ${y * 0.4}px)`;
});

scene.addEventListener('mouseleave', () => {
    if (!isFlipped) {
        flipper.style.transform = 'rotateX(0deg) rotateY(0deg)';
    }
});

// Flip card on click
scene.addEventListener('click', () => {
    isFlipped = !isFlipped;
    flipper.classList.toggle('flipped', isFlipped);
});