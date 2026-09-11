/**
 * Phone Lockscreen PIN Keypad — Interactive Logic & Audio Synthesizer
 * 1:1 Reference Replication with Black & Blob (9:16) Wallpaper Support
 */

(function () {
    let pinCode = "";
    const MAX_PIN_LENGTH = 8;
    let audioCtx = null;

    // Web Audio Synthesizer for Touch Haptic Feedback
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

    function playKeyClickSound() {
        try {
            initAudio();
            if (!audioCtx) return;

            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();

            osc.type = 'sine';
            const now = audioCtx.currentTime;
            osc.frequency.setValueAtTime(580, now);
            osc.frequency.exponentialRampToValueAtTime(240, now + 0.045);

            gain.gain.setValueAtTime(0.18, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.045);

            osc.connect(gain);
            gain.connect(audioCtx.destination);

            osc.start(now);
            osc.stop(now + 0.05);
        } catch (e) {}
    }

    function playSuccessChime() {
        try {
            initAudio();
            if (!audioCtx) return;

            const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
            notes.forEach((freq, idx) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                const startTime = audioCtx.currentTime + idx * 0.07;
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq, startTime);

                gain.gain.setValueAtTime(0.2, startTime);
                gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.28);

                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(startTime);
                osc.stop(startTime + 0.3);
            });
        } catch (e) {}
    }

    function playErrorBuzz() {
        try {
            initAudio();
            if (!audioCtx) return;

            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            const now = audioCtx.currentTime;

            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(140, now);
            osc.frequency.setValueAtTime(110, now + 0.08);

            gain.gain.setValueAtTime(0.2, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);

            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(now);
            osc.stop(now + 0.26);
        } catch (e) {}
    }

    function triggerHaptic(duration = 20) {
        if (navigator.vibrate) {
            try {
                navigator.vibrate(duration);
            } catch (e) {}
        }
    }

    // Render PIN dots inside the frosted capsule
    function updateDotsDisplay() {
        const dotsTrack = document.getElementById('dotsTrack');
        if (!dotsTrack) return;

        dotsTrack.innerHTML = '';
        for (let i = 0; i < pinCode.length; i++) {
            const dot = document.createElement('div');
            dot.className = 'pin-dot';
            dotsTrack.appendChild(dot);
        }

        // Hide error toast when user starts typing again
        const errorToast = document.getElementById('errorToast');
        if (errorToast) errorToast.classList.remove('visible');
    }

    // Key Press Handler
    window.handleKeyPress = function (digit) {
        if (pinCode.length >= MAX_PIN_LENGTH) return;

        playKeyClickSound();
        triggerHaptic(15);

        pinCode += digit;
        updateDotsDisplay();

        // Animate button active state
        const btn = document.querySelector(`.key-btn[data-key="${digit}"]`);
        if (btn) {
            btn.classList.add('pressed');
            setTimeout(() => btn.classList.remove('pressed'), 140);
        }
    };

    // Backspace Handler
    window.handleBackspace = function () {
        playKeyClickSound();
        triggerHaptic(18);

        if (pinCode.length > 0) {
            pinCode = pinCode.slice(0, -1);
            updateDotsDisplay();
        }

        const btn = document.getElementById('btnBackspace');
        if (btn) {
            btn.classList.add('pressed');
            setTimeout(() => btn.classList.remove('pressed'), 140);
        }
    };

    // Confirm / Validate Handler
    window.handleConfirm = function () {
        const btn = document.getElementById('btnConfirm');
        if (btn) {
            btn.classList.add('pressed');
            setTimeout(() => btn.classList.remove('pressed'), 140);
        }

        if (pinCode.length === 0) {
            showError("Please enter your password");
            return;
        }

        // Demo PIN validation: accept any 4-8 digit password, or demo "1234"
        if (pinCode.length >= 4) {
            unlockSuccess();
        } else {
            showError("Password too short (min 4 digits)");
        }
    };

    function showError(msg = "Incorrect password, try again") {
        playErrorBuzz();
        triggerHaptic([40, 60, 40]);

        const pill = document.getElementById('passwordPill');
        const toast = document.getElementById('errorToast');

        if (pill) {
            pill.classList.remove('error-shake');
            void pill.offsetWidth; // trigger reflow
            pill.classList.add('error-shake');
        }

        if (toast) {
            toast.textContent = msg;
            toast.classList.add('visible');
        }

        // Clear PIN after brief pause
        setTimeout(() => {
            pinCode = "";
            updateDotsDisplay();
        }, 500);
    }

    function unlockSuccess() {
        playSuccessChime();
        triggerHaptic([30, 40, 60]);

        const overlay = document.getElementById('unlockOverlay');
        if (overlay) {
            overlay.classList.add('active');
        }
    }

    window.resetLockscreen = function () {
        pinCode = "";
        updateDotsDisplay();
        const overlay = document.getElementById('unlockOverlay');
        if (overlay) {
            overlay.classList.remove('active');
        }
    };

    window.handleEmergencyCall = function () {
        playKeyClickSound();
        triggerHaptic(25);
        alert("Emergency Dialler\nDial 112 / 911 / 110 (Simulation mode)");
    };

    // Wallpaper Switcher (Black / Blob)
    window.setPhoneWallpaper = function (bg) {
        const viewport = document.getElementById('phoneViewport');
        if (viewport) {
            viewport.setAttribute('data-phone-bg', bg);
        }

        const btnBlack = document.getElementById('btnWpBlack');
        const btnBlob = document.getElementById('btnWpBlob');
        if (btnBlack) btnBlack.classList.toggle('active', bg === 'black');
        if (btnBlob) btnBlob.classList.toggle('active', bg === 'blob');

        try {
            localStorage.setItem('phone-lockscreen-wp', bg);
        } catch (e) {}
    };

    // Listen for parent window message
    window.addEventListener('message', function (e) {
        if (e.data && e.data.type === 'SET_PHONE_BG') {
            window.setPhoneWallpaper(e.data.bg);
        }
    });

    // Keyboard support (physical numpad and top-row numbers)
    window.addEventListener('keydown', function (e) {
        if (e.key >= '0' && e.key <= '9') {
            handleKeyPress(e.key);
        } else if (e.key === 'Backspace') {
            handleBackspace();
        } else if (e.key === 'Enter') {
            handleConfirm();
        } else if (e.key === 'Escape') {
            pinCode = "";
            updateDotsDisplay();
        }
    });

    // Restore saved wallpaper preference
    window.addEventListener('DOMContentLoaded', function () {
        let savedWp = 'blob';
        try {
            savedWp = localStorage.getItem('phone-lockscreen-wp') || 'blob';
        } catch (e) {}
        setPhoneWallpaper(savedWp);
    });
})();
