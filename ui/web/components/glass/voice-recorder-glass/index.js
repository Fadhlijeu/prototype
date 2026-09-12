const vCanvas = document.getElementById('voiceCanvas');
const vCtx = vCanvas.getContext('2d');
let isRecording = true;
let animVoice;

function drawSineWave() {
    vCtx.clearRect(0, 0, vCanvas.width, vCanvas.height);
    const w = vCanvas.width;
    const h = vCanvas.height;

    vCtx.beginPath();
    vCtx.strokeStyle = isRecording ? '#38BDF8' : 'rgba(255, 255, 255, 0.2)';
    vCtx.lineWidth = 2;

    const time = Date.now() * 0.005;
    for (let x = 0; x < w; x++) {
        const freq = isRecording ? 0.04 : 0.01;
        const amp = isRecording ? Math.sin(x * 0.02 + time) * 16 : 2;
        const y = h / 2 + Math.sin(x * freq + time) * amp;
        if (x === 0) vCtx.moveTo(x, y);
        else vCtx.lineTo(x, y);
    }
    vCtx.stroke();

    animVoice = requestAnimationFrame(drawSineWave);
}
drawSineWave();

const btnRec = document.getElementById('btnRecordToggle');
const beacon = document.getElementById('beacon');
const statusLabel = document.getElementById('statusLabel');

btnRec.addEventListener('click', () => {
    isRecording = !isRecording;
    beacon.classList.toggle('active', isRecording);
    statusLabel.textContent = isRecording ? 'LIVE AUDIO STREAM' : 'PAUSED';
    statusLabel.style.color = isRecording ? '#EF4444' : '#94A3B8';
});