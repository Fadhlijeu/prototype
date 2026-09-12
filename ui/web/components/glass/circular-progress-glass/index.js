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

setProgress(84);

// Autonomous organic telemetry pulse
setInterval(() => {
    let delta = (Math.random() * 4 - 2);
    let next = Math.min(96, Math.max(78, Math.round(currentVal + delta)));
    setProgress(next);
}, 2400);