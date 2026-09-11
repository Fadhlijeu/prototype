/**
 * AI Model Selector Logic with Dynamic Shuffle
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const modelPool = [
        { name: "Nexus Core 4.0", tag: "Flagship", desc: "Penalaran kognitif otonom & sintesis multi-modal" },
        { name: "Hyperion Synthetix", tag: "Deep Math", desc: "Penyelesaian logika tingkat lanjut & verifikasi kode" },
        { name: "Chronos Flash", tag: "Fast Edge", desc: "Inferensi ultra-cepat sub-detik untuk chat real-time" },
        { name: "Vortex Swarm", tag: "Multi-Agent", desc: "Koordinasi paralel agen terdistribusi & pencarian masif" },
        { name: "Aether Quantum", tag: "Reflection", desc: "Sistem penalaran berbobot dengan loop koreksi mandiri" },
        { name: "Pulse Neural", tag: "Streaming", desc: "Arsitektur hemat daya dengan latensi nol untuk perangkat lokal" }
    ];

    function attachSelectHandlers() {
        document.querySelectorAll('.model-item').forEach(item => {
            item.onclick = function() {
                document.querySelectorAll('.model-item').forEach(i => i.classList.remove('active'));
                this.classList.add('active');
            };
        });
    }

    attachSelectHandlers();

    const shuffleBtn = document.getElementById('btnShuffle');
    const container = document.getElementById('modelList');

    if (shuffleBtn && container) {
        shuffleBtn.addEventListener('click', () => {
            const shuffled = [...modelPool].sort(() => 0.5 - Math.random()).slice(0, 4);
            container.innerHTML = '';

            shuffled.forEach((m, idx) => {
                const item = document.createElement('div');
                item.className = `model-item ${idx === 0 ? 'active' : ''}`;
                item.innerHTML = `
                    <div class="model-info">
                        <div class="model-title-row">
                            <span class="model-title">${m.name}</span>
                            <span class="model-tag">${m.tag}</span>
                        </div>
                        <span class="model-subtitle">${m.desc}</span>
                    </div>
                    <i data-lucide="check" class="checkmark"></i>
                `;
                container.appendChild(item);
            });

            if (window.lucide) window.lucide.createIcons();
            attachSelectHandlers();
        });
    }
});