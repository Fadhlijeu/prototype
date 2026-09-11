/**
 * Elastic Lockscreen Glass Clock — Interactive Pull-to-Stretch Physics Engine
 * 1:1 Visual Match with Downward Rubber Sag, Wobble Harmonic Oscillation & Sound Synthesis
 */

(function () {
    // Digit Vector Path Definitions (Extra-tall condensed rounded glyphs, matching photo)
    const DIGIT_PATHS = {
        '0': "M 16,54 C 16,24 38,0 52,0 C 66,0 88,24 88,54 V 306 C 88,336 66,360 52,360 C 38,360 16,336 16,306 Z M 38,68 V 292 C 38,312 44,326 52,326 C 60,326 66,312 66,292 V 68 C 66,48 60,34 52,34 C 44,34 38,48 38,68 Z",
        '1': "M 32,46 L 56,22 V 360 H 34 V 42 L 32,46 Z",
        '2': "M 18,52 C 18,22 40,0 54,0 C 68,0 88,22 88,52 C 88,96 50,150 24,204 V 324 H 88 V 360 H 16 V 314 C 40,260 84,200 84,152 C 84,60 62,34 53,34 C 42,34 26,50 26,72 H 18 Z",
        '3': "M 18,50 C 18,22 40,0 53,0 C 67,0 88,22 88,50 C 88,88 64,124 50,146 C 66,168 88,206 88,252 C 88,310 66,360 52,360 C 38,360 16,312 16,270 H 26 C 26,304 40,326 52,326 C 64,326 78,284 78,248 C 78,198 56,166 40,166 H 34 V 136 H 40 C 54,136 78,108 78,64 C 78,42 64,34 53,34 C 42,34 26,44 26,68 H 18 Z",
        '4': "M 70,0 V 240 H 14 V 204 L 68,16 H 70 V 240 H 88 V 276 H 70 V 360 H 48 V 276 H 14 V 230 L 68,0 H 70 Z",
        '5': "M 84,0 V 36 H 26 V 140 C 34,126 50,118 64,118 C 78,118 88,142 88,184 V 286 C 88,332 68,360 52,360 C 36,360 16,328 16,280 H 26 C 26,314 38,326 52,326 C 66,326 78,300 78,272 V 196 C 78,162 66,146 52,146 C 40,146 30,158 24,176 L 16,168 L 18,0 H 84 Z",
        '6': "M 82,34 C 74,12 58,0 48,0 C 32,0 16,26 16,68 V 292 C 16,334 34,360 52,360 C 70,360 88,334 88,292 V 222 C 88,178 70,152 52,152 C 38,152 26,168 20,188 V 72 C 20,44 32,32 48,32 C 58,32 70,42 76,58 L 82,34 Z M 38,228 C 42,204 50,184 54,184 C 64,184 76,204 76,238 V 284 C 76,312 66,326 54,326 C 42,326 38,312 38,284 V 228 Z",
        '7': "M 16,0 H 88 V 36 L 44,360 H 22 L 66,36 H 16 V 0 Z",
        '8': "M 52,0 C 66,0 86,20 86,54 C 86,88 68,124 54,146 C 70,168 88,206 88,256 C 88,314 68,360 52,360 C 36,360 16,314 16,256 C 16,206 34,168 50,146 C 36,124 18,88 18,54 C 18,20 38,0 52,0 Z M 52,34 C 42,34 30,46 30,68 C 30,102 46,134 52,138 C 58,134 74,102 74,68 C 74,46 62,34 52,34 Z M 52,168 C 44,174 28,210 28,262 C 28,308 40,326 52,326 C 64,326 76,308 76,262 C 76,210 60,174 52,168 Z",
        '9': "M 22,326 C 30,348 46,360 56,360 C 72,360 88,334 88,292 V 68 C 88,26 70,0 52,0 C 34,0 16,26 16,68 V 138 C 16,182 34,208 52,208 C 66,208 78,192 84,172 V 288 C 84,316 72,328 56,328 C 46,328 34,318 28,302 L 22,326 Z M 66,132 C 62,156 54,176 50,176 C 40,176 28,156 28,122 V 76 C 28,48 38,34 50,34 C 62,34 66,48 66,76 V 132 Z"
    };

    // Physics Presets
    const ELASTICITY_PRESETS = {
        jelly: { stiffness: 0.085, damping: 0.81, maxStretch: 340, mass: 1.0, boingFreq: 180 },
        rubber: { stiffness: 0.14, damping: 0.88, maxStretch: 280, mass: 0.8, boingFreq: 260 },
        slime: { stiffness: 0.045, damping: 0.76, maxStretch: 420, mass: 1.4, boingFreq: 120 }
    };

    let activePreset = ELASTICITY_PRESETS.jelly;
    let timeMode = 'photo'; // 'photo' = 07:06, 'live' = real system time
    let clockInterval = null;

    // Web Audio Synthesizer
    let audioCtx = null;
    let tensionOsc = null;
    let tensionGain = null;

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

    function startTensionAudio() {
        try {
            initAudio();
            if (!audioCtx) return;

            tensionOsc = audioCtx.createOscillator();
            tensionGain = audioCtx.createGain();

            tensionOsc.type = 'triangle';
            tensionOsc.frequency.setValueAtTime(80, audioCtx.currentTime);

            tensionGain.gain.setValueAtTime(0.01, audioCtx.currentTime);

            tensionOsc.connect(tensionGain);
            tensionGain.connect(audioCtx.destination);
            tensionOsc.start();
        } catch (e) {}
    }

    function updateTensionAudio(stretchRatio) {
        if (!tensionOsc || !tensionGain || !audioCtx) return;
        try {
            const freq = 80 + stretchRatio * 280;
            const vol = Math.min(0.12, stretchRatio * 0.12);
            tensionOsc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            tensionGain.gain.setValueAtTime(vol, audioCtx.currentTime);
        } catch (e) {}
    }

    function stopTensionAudio() {
        if (tensionOsc) {
            try {
                tensionGain.gain.setValueAtTime(0, audioCtx.currentTime);
                tensionOsc.stop(audioCtx.currentTime + 0.05);
            } catch (e) {}
            tensionOsc = null;
            tensionGain = null;
        }
    }

    function playBoingSound(velocity) {
        try {
            initAudio();
            if (!audioCtx) return;

            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();

            const baseFreq = activePreset.boingFreq;
            const now = audioCtx.currentTime;

            osc.type = 'sine';
            osc.frequency.setValueAtTime(baseFreq * 1.5, now);
            osc.frequency.exponentialRampToValueAtTime(baseFreq, now + 0.08);
            osc.frequency.exponentialRampToValueAtTime(baseFreq * 0.7, now + 0.35);

            gain.gain.setValueAtTime(0.24, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

            osc.connect(gain);
            gain.connect(audioCtx.destination);

            osc.start(now);
            osc.stop(now + 0.5);
        } catch (e) {}
    }

    // Time Display Controller
    function renderDigits(timeStr) {
        const d0 = timeStr[0] || '0';
        const d1 = timeStr[1] || '7';
        const d2 = timeStr[3] || '0';
        const d3 = timeStr[4] || '6';

        const p0 = document.getElementById('pathD0');
        const p1 = document.getElementById('pathD1');
        const p2 = document.getElementById('pathD2');
        const p3 = document.getElementById('pathD3');

        if (p0) p0.setAttribute('d', DIGIT_PATHS[d0] || DIGIT_PATHS['0']);
        if (p1) p1.setAttribute('d', DIGIT_PATHS[d1] || DIGIT_PATHS['7']);
        if (p2) p2.setAttribute('d', DIGIT_PATHS[d2] || DIGIT_PATHS['0']);
        if (p3) p3.setAttribute('d', DIGIT_PATHS[d3] || DIGIT_PATHS['6']);
    }

    function updateClock() {
        if (timeMode === 'photo') {
            renderDigits("07:06");
        } else {
            const now = new Date();
            const hh = String(now.getHours()).padStart(2, '0');
            const mm = String(now.getMinutes()).padStart(2, '0');
            renderDigits(`${hh}:${mm}`);
        }
    }

    // Gesture & Pull-to-Stretch Physics Engine
    let isDragging = false;
    let startPointerY = 0;
    let currentStretch = 0; // Current vertical stretch displacement
    let springVelocity = 0;
    let animFrameId = null;

    const clockMesh = document.getElementById('elasticClockMesh');
    const dragArea = document.getElementById('clockDragArea');
    const pullHint = document.getElementById('pullHint');
    const hudStretchVal = document.getElementById('hudStretchVal');
    const hudTensionVal = document.getElementById('hudTensionVal');
    const hudBarFill = document.getElementById('hudBarFill');

    // Digit columns for non-linear parabolic sag
    const col0 = document.getElementById('digitCol0');
    const col1 = document.getElementById('digitCol1');
    const colonCol = document.getElementById('colonCol');
    const col2 = document.getElementById('digitCol2');
    const col3 = document.getElementById('digitCol3');

    function applyStretchDeformation(stretchPx) {
        currentStretch = stretchPx;

        // Ratio of stretch relative to max
        const ratio = Math.max(0, stretchPx / activePreset.maxStretch);

        // Volume-preserving scale: As it elongates vertically, it squashes horizontally
        const scaleY = 1 + (stretchPx / 260);
        const scaleX = 1 / Math.sqrt(Math.max(0.6, scaleY));
        const translateY = stretchPx * 0.45;

        // Apply deformation matrix to clock mesh
        if (clockMesh) {
            clockMesh.style.transform = `translateY(${translateY}px) scale(${scaleX}, ${scaleY})`;

            // Tension classes for glow effects
            clockMesh.classList.toggle('high-tension', ratio > 0.45 && ratio <= 0.8);
            clockMesh.classList.toggle('extreme-tension', ratio > 0.8);
        }

        // Parabolic droop on individual digit columns (sagging more in center and bottom)
        const sagCenter = stretchPx * 0.16;
        const sagEdges = stretchPx * 0.07;
        const colonLag = stretchPx * 0.22;

        if (col0) col0.style.transform = `translate(18px, ${sagEdges}px)`;
        if (col1) col1.style.transform = `translate(142px, ${sagCenter}px)`;
        if (colonCol) colonCol.style.transform = `translate(262px, ${colonLag}px)`;
        if (col2) col2.style.transform = `translate(296px, ${sagCenter}px)`;
        if (col3) col3.style.transform = `translate(420px, ${sagEdges}px)`;

        // Update Telemetry HUD
        const stretchPercent = Math.round(ratio * 100);
        const tensionNewton = (ratio * 4.8).toFixed(1);

        if (hudStretchVal) hudStretchVal.innerText = `+${stretchPercent}%`;
        if (hudTensionVal) hudTensionVal.innerText = `${tensionNewton} N`;
        if (hudBarFill) hudBarFill.style.width = `${Math.min(100, stretchPercent)}%`;

        updateTensionAudio(ratio);
    }

    function onPointerDown(e) {
        isDragging = true;
        startPointerY = e.clientY;
        if (animFrameId) cancelAnimationFrame(animFrameId);

        if (dragArea) dragArea.classList.add('dragging');
        if (pullHint) pullHint.classList.add('hidden');

        startTensionAudio();

        if (dragArea && dragArea.setPointerCapture) {
            dragArea.setPointerCapture(e.pointerId);
        }
    }

    function onPointerMove(e) {
        if (!isDragging) return;

        const rawDeltaY = e.clientY - startPointerY;

        if (rawDeltaY > 0) {
            // Logarithmic progressive resistance curve
            const damped = rawDeltaY / (1 + rawDeltaY * 0.0018);
            const clamped = Math.min(activePreset.maxStretch, damped);
            applyStretchDeformation(clamped);
        } else {
            // Slight compression upward if dragged up
            const compressed = Math.max(-30, rawDeltaY * 0.3);
            applyStretchDeformation(compressed);
        }
    }

    function onPointerUp(e) {
        if (!isDragging) return;
        isDragging = false;

        if (dragArea) dragArea.classList.remove('dragging');
        stopTensionAudio();

        if (dragArea && dragArea.releasePointerCapture) {
            try {
                dragArea.releasePointerCapture(e.pointerId);
            } catch (err) {}
        }

        // Trigger spring snap-back animation
        if (Math.abs(currentStretch) > 20) {
            playBoingSound(springVelocity);
            if (navigator.vibrate) {
                try { navigator.vibrate([20, 30, 40]); } catch(e) {}
            }
        }

        runSpringSnapAnimation();
    }

    // Damped Harmonic Spring Simulation
    function runSpringSnapAnimation() {
        if (animFrameId) cancelAnimationFrame(animFrameId);

        let pos = currentStretch;
        let vel = springVelocity;
        const k = activePreset.stiffness;
        const d = activePreset.damping;

        function springStep() {
            // Hooke's Law with damping: F = -k * x - c * v
            const force = -k * pos;
            vel = (vel + force) * d;
            pos += vel;

            applyStretchDeformation(pos);

            // Check if settled
            if (Math.abs(pos) > 0.4 || Math.abs(vel) > 0.4) {
                animFrameId = requestAnimationFrame(springStep);
            } else {
                applyStretchDeformation(0);
                animFrameId = null;
            }
        }

        animFrameId = requestAnimationFrame(springStep);
    }

    window.triggerSnapBack = function () {
        if (animFrameId) cancelAnimationFrame(animFrameId);
        playBoingSound(1.0);
        applyStretchDeformation(0);
    };

    // Wallpaper Switcher (Black / Blob)
    window.setClockBg = function (bg) {
        const stage = document.getElementById('clockStage');
        if (stage) {
            stage.setAttribute('data-stage-bg', bg);
        }

        const btnBlack = document.getElementById('btnBgBlack');
        const btnBlob = document.getElementById('btnBgBlob');
        if (btnBlack) btnBlack.classList.toggle('active', bg === 'black');
        if (btnBlob) btnBlob.classList.toggle('active', bg === 'blob');

        try {
            localStorage.setItem('elastic-clock-bg', bg);
        } catch (e) {}
    };

    // Time Mode Switcher
    window.setTimeMode = function (mode) {
        timeMode = mode;
        const btnPhoto = document.getElementById('btnTimePhoto');
        const btnLive = document.getElementById('btnTimeLive');

        if (btnPhoto) btnPhoto.classList.toggle('active', mode === 'photo');
        if (btnLive) btnLive.classList.toggle('active', mode === 'live');

        if (clockInterval) clearInterval(clockInterval);
        if (mode === 'live') {
            updateClock();
            clockInterval = setInterval(updateClock, 1000);
        } else {
            updateClock();
        }
    };

    // Elasticity Preset Selector
    window.setElasticity = function (type, btn) {
        if (ELASTICITY_PRESETS[type]) {
            activePreset = ELASTICITY_PRESETS[type];
        }
        document.querySelectorAll('[data-elasticity]').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
    };

    // Attach Pointer Event Listeners
    if (dragArea) {
        dragArea.addEventListener('pointerdown', onPointerDown);
        window.addEventListener('pointermove', onPointerMove);
        window.addEventListener('pointerup', onPointerUp);
        window.addEventListener('pointercancel', onPointerUp);
    }

    // Initialize
    window.addEventListener('DOMContentLoaded', () => {
        updateClock();

        let savedBg = 'black';
        try {
            savedBg = localStorage.getItem('elastic-clock-bg') || 'black';
        } catch (e) {}
        setClockBg(savedBg);
    });
})();
