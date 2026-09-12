const canvas = document.getElementById('eqCanvas');
const ctx = canvas.getContext('2d');
let isPlaying = true;
let animId;

const numBars = 32;
const barGains = [4, 2, -1, 5, 3];

function drawSpectrum() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const width = canvas.width;
    const height = canvas.height;
    const barWidth = (width / numBars) - 2;

    const time = Date.now() * 0.004;

    for (let i = 0; i < numBars; i++) {
        // synthesize frequency response
        const bandIndex = Math.min(4, Math.floor((i / numBars) * 5));
        const boost = (barGains[bandIndex] + 12) / 24; // normalize 0-1
        
        let barHeight = 10;
        if (isPlaying) {
            const wave = Math.sin(time + i * 0.3) * 0.4 + 0.6;
            const noise = Math.sin(time * 2.3 + i * 1.2) * 0.25;
            barHeight = (wave + noise) * (height * 0.75) * (0.4 + boost * 0.8);
        } else {
            barHeight = 6 + Math.sin(i * 0.5) * 3;
        }

        const x = i * (barWidth + 2) + 2;
        const y = height - barHeight;

        // Gradient
        const grad = ctx.createLinearGradient(0, height, 0, 0);
        grad.addColorStop(0, '#38BDF8');
        grad.addColorStop(0.7, '#818CF8');
        grad.addColorStop(1, '#C084FC');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.roundRect(x, y, barWidth, barHeight, [2, 2, 0, 0]);
        ctx.fill();

        // Peak dot
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(x, Math.max(0, y - 3), barWidth, 1.5);
    }

    animId = requestAnimationFrame(drawSpectrum);
}
drawSpectrum();

// Vertical Range Inputs
document.querySelectorAll('.eq-vertical-range').forEach((slider, idx) => {
    slider.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        barGains[idx] = val;
        const sign = val > 0 ? '+' : '';
        const bandKey = e.target.dataset.band;
        const label = document.getElementById('gain' + bandKey);
        if (label) label.textContent = `${sign}${val} dB`;
        document.getElementById('eqPresetLabel').textContent = 'Custom Profile';
        document.querySelectorAll('.btn-eq-preset').forEach(b => b.classList.remove('active'));
    });
});

// Presets
const presets = {
    master: [4, 2, -1, 5, 3],
    bass: [9, 6, 1, 0, -2],
    vocal: [-2, 1, 5, 4, 1],
    electronic: [7, 3, -2, 6, 8]
};

document.querySelectorAll('.btn-eq-preset').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.btn-eq-preset').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const pKey = btn.dataset.preset;
        const gains = presets[pKey];
        document.getElementById('eqPresetLabel').textContent = btn.textContent;
        
        const bands = ['60', '250', '1k', '4k', '16k'];
        gains.forEach((g, i) => {
            barGains[i] = g;
            const slider = document.querySelector(`.eq-vertical-range[data-band="${bands[i]}"]`);
            if (slider) slider.value = g;
            const label = document.getElementById('gain' + bands[i]);
            const sign = g > 0 ? '+' : '';
            if (label) label.textContent = `${sign}${g} dB`;
        });
    });
});

// Play/Pause
const btnPlay = document.getElementById('btnEqPlay');
const playText = document.getElementById('eqPlayText');
btnPlay.addEventListener('click', () => {
    isPlaying = !isPlaying;
    playText.textContent = isPlaying ? 'Pause Spectrum Stream' : 'Resume Spectrum Stream';
    btnPlay.classList.toggle('playing', isPlaying);
});