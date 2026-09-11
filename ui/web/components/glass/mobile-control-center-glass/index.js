/**
 * Mobile Control Center — Glass Dark Quick Settings Logic
 * 1:1 Reference Replication with Pure White Typography (NO BLUE)
 */

(function () {
    let currentVolume = 0.32;
    let currentBrightness = 0.58;
    let isAutoBrightness = false;
    let isMuted = false;

    // Web Audio Synthesizer
    let audioCtx = null;

    function initAudio() {
        if (!audioCtx) {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            if (AudioContextClass) {
                audioCtx = new AudioContextClass();
            }
        }
        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
    }

    function playTactileClick() {
        if (isMuted || currentVolume <= 0) return;
        try {
            initAudio();
            if (!audioCtx) return;

            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();

            osc.type = 'sine';
            const now = audioCtx.currentTime;
            osc.frequency.setValueAtTime(620, now);
            osc.frequency.exponentialRampToValueAtTime(300, now + 0.035);

            const masterGain = currentVolume * 0.25;
            gain.gain.setValueAtTime(masterGain, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.035);

            osc.connect(gain);
            gain.connect(audioCtx.destination);

            osc.start(now);
            osc.stop(now + 0.04);
        } catch (e) {}
    }

    function triggerHaptic(ms = 15) {
        if (navigator.vibrate) {
            try { navigator.vibrate(ms); } catch (e) {}
        }
    }

    // Toggle Connect Card (Wi-Fi / Data network)
    window.toggleConnectCard = function (cardId) {
        playTactileClick();
        triggerHaptic(18);

        const el = cardId === 'wifi' ? document.getElementById('cardWifi') : document.getElementById('cardData');
        if (el) {
            el.classList.toggle('active');
        }
    };

    // Toggle Quick Settings Tile
    window.toggleTile = function (tileId, label) {
        playTactileClick();
        triggerHaptic(18);

        const tile = document.getElementById(tileId);
        if (tile) {
            const isActive = tile.classList.toggle('active');

            // Extra dim effect integration
            if (tileId === 'tileExtraDim') {
                applyBrightnessLevel(isActive ? currentBrightness * 0.5 : currentBrightness);
            }

            // Silent mode toggle integration
            if (tileId === 'tileSilent') {
                setMuteState(isActive);
            }
        }
    };

    // Header Tools Action
    window.handleToolAction = function (tool) {
        playTactileClick();
        triggerHaptic(15);
        if (tool === 'edit') {
            alert("Edit Control Center (Simulasi: Atur ulang posisi tile)");
        } else if (tool === 'settings') {
            alert("Settings (Simulasi: Buka Pengaturan Perangkat)");
        } else {
            alert("More Options (Simulasi: Opsi tambahan)");
        }
    };

    // Brightness Control
    const brightnessTrack = document.getElementById('brightnessTrack');
    const brightnessFill = document.getElementById('brightnessFill');
    const phoneViewport = document.getElementById('phoneViewport');

    function applyBrightnessLevel(level) {
        const clamped = Math.max(0.1, Math.min(1.0, level));
        if (brightnessFill) {
            brightnessFill.style.width = `${Math.round(clamped * 100)}%`;
        }
        if (phoneViewport) {
            phoneViewport.style.filter = `brightness(${0.45 + clamped * 0.65})`;
        }
    }

    function setupSliderDragging(trackEl, onUpdate) {
        if (!trackEl) return;

        function updateFromPointer(e) {
            const rect = trackEl.getBoundingClientRect();
            const clientX = e.clientX || (e.touches && e.touches[0] ? e.touches[0].clientX : rect.left);
            const ratio = (clientX - rect.left) / rect.width;
            const clamped = Math.max(0, Math.min(1, ratio));
            onUpdate(clamped);
        }

        let isDragging = false;

        trackEl.addEventListener('pointerdown', (e) => {
            isDragging = true;
            trackEl.setPointerCapture(e.pointerId);
            updateFromPointer(e);
            playTactileClick();
            triggerHaptic(12);
        });

        trackEl.addEventListener('pointermove', (e) => {
            if (isDragging) {
                updateFromPointer(e);
            }
        });

        const stopDrag = (e) => {
            if (isDragging) {
                isDragging = false;
                try { trackEl.releasePointerCapture(e.pointerId); } catch (err) {}
            }
        };

        trackEl.addEventListener('pointerup', stopDrag);
        trackEl.addEventListener('pointercancel', stopDrag);
    }

    setupSliderDragging(brightnessTrack, (val) => {
        currentBrightness = Math.max(0.1, val);
        applyBrightnessLevel(currentBrightness);
    });

    window.toggleAutoBrightness = function () {
        playTactileClick();
        triggerHaptic(15);
        isAutoBrightness = !isAutoBrightness;
        const btn = document.getElementById('btnAutoBrightness');
        if (btn) btn.classList.toggle('active', isAutoBrightness);

        if (isAutoBrightness) {
            currentBrightness = 0.58;
            applyBrightnessLevel(currentBrightness);
        }
    };

    // Volume Control
    const volumeTrack = document.getElementById('volumeTrack');
    const volumeFill = document.getElementById('volumeFill');

    function applyVolumeLevel(level) {
        currentVolume = Math.max(0, Math.min(1.0, level));
        if (volumeFill) {
            volumeFill.style.width = `${Math.round(currentVolume * 100)}%`;
        }
        setMuteState(currentVolume === 0);
    }

    setupSliderDragging(volumeTrack, (val) => {
        applyVolumeLevel(val);
    });

    function setMuteState(mute) {
        isMuted = mute;
        const btnMute = document.getElementById('btnMuteToggle');
        const tileSilent = document.getElementById('tileSilent');

        if (btnMute) {
            btnMute.classList.toggle('alert-active', isMuted);
            const svg = btnMute.querySelector('svg');
            if (svg) {
                svg.setAttribute('stroke', isMuted ? '#EF4444' : '#FFFFFF');
            }
        }
        if (tileSilent) {
            tileSilent.classList.toggle('active', isMuted);
        }
    }

    window.toggleMute = function () {
        playTactileClick();
        triggerHaptic(20);
        setMuteState(!isMuted);
        if (!isMuted && currentVolume === 0) {
            applyVolumeLevel(0.35);
        }
    };

    // Android Navigation Bar
    window.handleNav = function (action) {
        playTactileClick();
        triggerHaptic(15);
    };

    // Wallpaper Switcher (Black / Blob)
    window.setControlCenterBg = function (bg) {
        if (phoneViewport) {
            phoneViewport.setAttribute('data-phone-bg', bg);
        }

        const btnBlack = document.getElementById('btnWpBlack');
        const btnBlob = document.getElementById('btnWpBlob');
        if (btnBlack) btnBlack.classList.toggle('active', bg === 'black');
        if (btnBlob) btnBlob.classList.toggle('active', bg === 'blob');

        try {
            localStorage.setItem('cc-wallpaper', bg);
        } catch (e) {}
    };

    // Live Clock & Date
    function updateClockAndDate() {
        const now = new Date();
        const clockEl = document.getElementById('ccClock');
        const dayEl = document.getElementById('ccDateDay');
        const nameEl = document.getElementById('ccDateName');

        if (clockEl) {
            const hrs = String(now.getHours()).padStart(2, '0');
            const mins = String(now.getMinutes()).padStart(2, '0');
            clockEl.textContent = `${hrs}:${mins}`;
        }
        if (dayEl) {
            const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            dayEl.textContent = `${months[now.getMonth()]} ${now.getDate()}`;
        }
        if (nameEl) {
            const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            nameEl.textContent = days[now.getDay()];
        }
    }

    // Dynamic Randomized Tech Networks
    const WIFI_NETWORKS = ['Quantum-5G', 'Aether-Net', 'HyperLink-Wi-Fi', 'Nexus-Mesh', 'Nova-Fiber'];
    const CARRIERS = ['SkyLink 5G', 'Aether Mobile', 'Quantum 5G', 'Nova Cellular'];

    function initRandomizedContent() {
        const wifiEl = document.getElementById('wifiTitle');
        const carrierEl = document.getElementById('carrierText');
        if (wifiEl) {
            const randWifi = WIFI_NETWORKS[Math.floor(Math.random() * WIFI_NETWORKS.length)];
            wifiEl.textContent = randWifi;
        }
        if (carrierEl) {
            const randCarrier = CARRIERS[Math.floor(Math.random() * CARRIERS.length)];
            carrierEl.textContent = randCarrier;
        }
    }

    // Initialize
    window.addEventListener('DOMContentLoaded', () => {
        applyBrightnessLevel(currentBrightness);
        applyVolumeLevel(currentVolume);
        updateClockAndDate();
        setInterval(updateClockAndDate, 1000);
        initRandomizedContent();

        let savedWp = 'black';
        try {
            savedWp = localStorage.getItem('cc-wallpaper') || 'black';
        } catch (e) {}
        setControlCenterBg(savedWp);
    });
})();
