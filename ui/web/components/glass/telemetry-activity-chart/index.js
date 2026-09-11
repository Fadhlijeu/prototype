const container = document.getElementById('bars');
const toast = document.getElementById('chartToast');
const heights = [45, 62, 50, 78, 58, 88, 68, 94, 72, 60, 80, 92];

if (container) {
    heights.forEach((h, i) => {
        const b = document.createElement('div');
        b.className = 'bar-col';
        b.style.height = h + '%';
        b.title = `Hour ${i + 1}: ${h}% activity load`;
        b.onclick = () => {
            document.querySelectorAll('.bar-col').forEach(c => c.style.filter = '');
            b.style.filter = 'brightness(1.4) drop-shadow(0 0 10px #38BDF8)';
            if (toast) {
                toast.textContent = `Jam ke-${i + 1}: Beban ${h}% • Telemetri Stabil`;
            }
        };
        container.appendChild(b);
    });
}