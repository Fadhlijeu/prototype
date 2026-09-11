/**
 * Glass Glowing Progress Bar Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    let currentPercent = 78;
    const totalGb = 100;
    const counterVal = document.getElementById('counterVal');
    const glassFill = document.getElementById('glassFill');
    const storageDetail = document.getElementById('storageDetail');
    const btnMinus = document.getElementById('btnMinus');
    const btnPlus = document.getElementById('btnPlus');
    const btnAutoSim = document.getElementById('btnAutoSim');

    function updateProgress(val) {
        currentPercent = Math.max(5, Math.min(100, val));
        if (counterVal) counterVal.textContent = currentPercent;
        if (glassFill) glassFill.style.width = `${currentPercent}%`;
        if (storageDetail) storageDetail.textContent = `${((currentPercent / 100) * totalGb).toFixed(1)} / ${totalGb} GB`;
    }

    if (btnMinus) {
        btnMinus.addEventListener('click', () => updateProgress(currentPercent - 10));
    }

    if (btnPlus) {
        btnPlus.addEventListener('click', () => updateProgress(currentPercent + 10));
    }

    let simInterval = null;
    if (btnAutoSim) {
        btnAutoSim.addEventListener('click', () => {
            if (simInterval) {
                clearInterval(simInterval);
                simInterval = null;
                btnAutoSim.innerHTML = `<i data-lucide="play"></i> Auto`;
            } else {
                btnAutoSim.innerHTML = `<i data-lucide="pause"></i> Pause`;
                simInterval = setInterval(() => {
                    let next = currentPercent + 4;
                    if (next > 100) next = 10;
                    updateProgress(next);
                }, 800);
            }
            if (window.lucide) window.lucide.createIcons();
        });
    }
});
