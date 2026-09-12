const canvas = document.getElementById('colorCanvas');
const ctx = canvas.getContext('2d');
const thumb = document.getElementById('pickerThumb');
const hueSlider = document.getElementById('hueSlider');
const swatch = document.getElementById('swatchPreview');
const hexInput = document.getElementById('hexInput');
const btnCopy = document.getElementById('btnCopyHex');

let currentHue = 199;

function drawCanvas() {
    const w = canvas.width;
    const h = canvas.height;

    ctx.fillStyle = `hsl(${currentHue}, 100%, 50%)`;
    ctx.fillRect(0, 0, w, h);

    // White gradient horizontal
    const whiteGrad = ctx.createLinearGradient(0, 0, w, 0);
    whiteGrad.addColorStop(0, 'rgba(255,255,255,1)');
    whiteGrad.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = whiteGrad;
    ctx.fillRect(0, 0, w, h);

    // Black gradient vertical
    const blackGrad = ctx.createLinearGradient(0, 0, 0, h);
    blackGrad.addColorStop(0, 'rgba(0,0,0,0)');
    blackGrad.addColorStop(1, 'rgba(0,0,0,1)');
    ctx.fillStyle = blackGrad;
    ctx.fillRect(0, 0, w, h);
}

function updateColorAt(x, y) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const px = Math.max(0, Math.min(canvas.width - 1, x * scaleX));
    const py = Math.max(0, Math.min(canvas.height - 1, y * scaleY));

    const pixel = ctx.getImageData(px, py, 1, 1).data;
    const hex = '#' + [pixel[0], pixel[1], pixel[2]].map(x => x.toString(16).padStart(2, '0')).join('').toUpperCase();

    swatch.style.backgroundColor = hex;
    hexInput.value = hex;

    thumb.style.left = `${(px / canvas.width) * 100}%`;
    thumb.style.top = `${(py / canvas.height) * 100}%`;
}

drawCanvas();

hueSlider.addEventListener('input', (e) => {
    currentHue = e.target.value;
    drawCanvas();
    const rect = canvas.getBoundingClientRect();
    const curX = (parseFloat(thumb.style.left) / 100) * rect.width || rect.width * 0.7;
    const curY = (parseFloat(thumb.style.top) / 100) * rect.height || rect.height * 0.3;
    updateColorAt(curX, curY);
});

canvas.parentElement.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    function move(evt) {
        const x = evt.clientX - rect.left;
        const y = evt.clientY - rect.top;
        updateColorAt(x, y);
    }
    move(e);
    function up() {
        window.removeEventListener('mousemove', move);
        window.removeEventListener('mouseup', up);
    }
    window.addEventListener('mousemove', move);
    window.addEventListener('mouseup', up);
});

btnCopy.addEventListener('click', () => {
    navigator.clipboard.writeText(hexInput.value);
    const icon = document.getElementById('copyIcon');
    icon.setAttribute('data-lucide', 'check');
    if (window.lucide) lucide.createIcons();
    setTimeout(() => {
        icon.setAttribute('data-lucide', 'copy');
        if (window.lucide) lucide.createIcons();
    }, 1500);
});

// Presets
document.querySelectorAll('.preset-dot').forEach(dot => {
    dot.addEventListener('click', () => {
        document.querySelectorAll('.preset-dot').forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
        const hex = dot.dataset.hex;
        swatch.style.backgroundColor = hex;
        hexInput.value = hex;
    });
});