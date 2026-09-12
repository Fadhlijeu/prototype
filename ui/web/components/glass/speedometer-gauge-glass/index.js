const gauge = document.getElementById('gaugePath');
const valEl = document.getElementById('speedoVal');
const downEl = document.getElementById('downVal');
const btnTest = document.getElementById('btnTestSpeed');

const maxDash = 283;

function setSpeed(mbps) {
    const ratio = Math.min(1000, mbps) / 1000;
    const offset = maxDash - (ratio * maxDash);
    gauge.style.strokeDashoffset = offset;
    valEl.textContent = mbps.toFixed(1);
    downEl.textContent = `${mbps.toFixed(1)} Mbps`;
}

btnTest.addEventListener('click', () => {
    btnTest.disabled = true;
    let step = 0;
    const interval = setInterval(() => {
        step++;
        const target = Math.sin(step * 0.4) * 300 + 600 + Math.random() * 80;
        setSpeed(target);
        if (step > 15) {
            clearInterval(interval);
            setSpeed(942.8);
            btnTest.disabled = false;
        }
    }, 120);
});