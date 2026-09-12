const circle = document.getElementById('circleProgress');
const pctText = document.getElementById('radialPct');
const speedText = document.getElementById('statSpeed');
const timeText = document.getElementById('statTime');

const circumference = 2 * Math.PI * 76; // ~477.52
let currentVal = 84;
let autoInterval = null;

function setProgress(val) {
    currentVal = Math.max(0, Math.min(100, val));
    const offset = circumference - (currentVal / 100) * circumference;
    circle.style.strokeDashoffset = offset;
    pctText.textContent = currentVal;
    
    // update telemetry
    speedText.textContent = `${Math.floor(250 + currentVal * 2.8)} MB/s`;
    timeText.textContent = currentVal === 100 ? 'Done' : `${((100 - currentVal) * 0.08).toFixed(1)}s`;
}

document.getElementById('btnMinus').addEventListener('click', () => {
    clearInterval(autoInterval);
    setProgress(currentVal - 10);
});

document.getElementById('btnPlus').addEventListener('click', () => {
    clearInterval(autoInterval);
    setProgress(currentVal + 10);
});

document.getElementById('btnAutoSweep').addEventListener('click', () => {
    if (autoInterval) {
        clearInterval(autoInterval);
        autoInterval = null;
        document.getElementById('btnAutoSweep').textContent = 'Auto Pulse';
    } else {
        document.getElementById('btnAutoSweep').textContent = 'Stop Pulse';
        autoInterval = setInterval(() => {
            let next = currentVal + 6;
            if (next > 100) next = 10;
            setProgress(next);
        }, 400);
    }
});

setProgress(84);