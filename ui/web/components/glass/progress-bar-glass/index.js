/**
 * Glass Glowing Progress Bar Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    let currentPercent = 14;
    const totalGb = 100;
    const counterVal = document.getElementById('counterVal');
    const glassFill = document.getElementById('glassFill');
    const storageDetail = document.getElementById('storageDetail');
    const syncSpeedLabel = document.getElementById('syncSpeedLabel');
    const syncStatusLabel = document.getElementById('syncStatusLabel');
    const speeds = ["24.2 MB/s", "29.8 MB/s", "33.5 MB/s", "27.1 MB/s", "38.6 MB/s"];

    function updateProgress(val) {
        currentPercent = Math.max(0, Math.min(100, Math.round(val)));
        if (counterVal) counterVal.textContent = currentPercent;
        if (glassFill) glassFill.style.width = `${currentPercent}%`;
        if (storageDetail) storageDetail.textContent = `${((currentPercent / 100) * totalGb).toFixed(1)} / ${totalGb} GB`;
    }

    // Autonomous auto-advancing progress simulation (Zero dummy buttons!)
    function runAutoSyncLoop() {
        const step = () => {
            if (currentPercent < 100) {
                const inc = Math.floor(Math.random() * 5) + 2;
                currentPercent = Math.min(100, currentPercent + inc);
                updateProgress(currentPercent);

                if (syncSpeedLabel) syncSpeedLabel.textContent = speeds[Math.floor(Math.random() * speeds.length)];

                if (syncStatusLabel) {
                    syncStatusLabel.textContent = currentPercent === 100 ? "Sinkronisasi Selesai" : "Streaming Data Multi-Region";
                }

                const nextDelay = currentPercent === 100 ? 2400 : Math.floor(Math.random() * 300) + 250;
                setTimeout(step, nextDelay);
            } else {
                currentPercent = 5;
                updateProgress(currentPercent);
                if (syncStatusLabel) syncStatusLabel.textContent = "Menginisialisasi Sesi Baru...";
                setTimeout(step, 800);
            }
        };
        setTimeout(step, 400);
    }

    runAutoSyncLoop();
});
