/**
 * ==========================================================================
 * GELLY — Interactive Physics-Driven Blob Companion & Guidance System
 * Inspired by FeralUI playful physics elements (https://feralui.dev/blob)
 * 
 * Features:
 * - Realtime soft-body spring physics jelly blob on Canvas 2D
 * - Eye tracking with pupils following mouse cursor across the entire screen
 * - Natural blinking intervals & expressive mouth expressions
 * - Frosted glass chat speech bubble peeking diagonally from bottom-right
 * - Step-by-step beginner friendly interactive tour
 * - Dynamic spotlight overlay highlighting page elements with floating badges
 * - Procedural Web Audio API sound effects (no external audio assets)
 * ==========================================================================
 */

(function () {
    'use strict';

    // Prevent duplicate initialization
    if (window.__GELLY_COMPANION_INITIALIZED__) return;
    window.__GELLY_COMPANION_INITIALIZED__ = true;

    /* --------------------------------------------------------------------------
       1. SOUND EFFECTS (Web Audio API)
       -------------------------------------------------------------------------- */
    let audioCtx = null;
    let isMuted = localStorage.getItem('gelly_sound_muted') === 'true';

    function initAudio() {
        if (!audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) audioCtx = new AudioContext();
        }
    }

    function playSound(type = 'pop') {
        if (isMuted) return;
        try {
            initAudio();
            if (!audioCtx) return;
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }

            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            if (type === 'pop') {
                // Friendly soft bubble pop
                osc.type = 'sine';
                osc.frequency.setValueAtTime(460, now);
                osc.frequency.exponentialRampToValueAtTime(780, now + 0.08);
                gain.gain.setValueAtTime(0.14, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
                osc.start(now);
                osc.stop(now + 0.1);
            } else if (type === 'chime') {
                // Success chime arpeggio
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(523.25, now); // C5
                osc.frequency.setValueAtTime(659.25, now + 0.07); // E5
                osc.frequency.setValueAtTime(783.99, now + 0.14); // G5
                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
                osc.start(now);
                osc.stop(now + 0.3);
            } else if (type === 'squish') {
                // Jelly squish sound
                osc.type = 'sine';
                osc.frequency.setValueAtTime(320, now);
                osc.frequency.exponentialRampToValueAtTime(180, now + 0.12);
                gain.gain.setValueAtTime(0.15, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.13);
                osc.start(now);
                osc.stop(now + 0.14);
            }
        } catch (e) {
            // Audio policy or unsupported fallback
        }
    }

    /* --------------------------------------------------------------------------
       2. TOUR SCRIPTS CONFIGURATION (Tailored per page)
       -------------------------------------------------------------------------- */
    const isShowcase = window.location.pathname.includes('showcase.html');
    const isWebApps = window.location.pathname.includes('apps.html');

    const showcaseTour = [
        {
            title: "Halo! Aku Gelly 👋",
            message: "Aku pemandumu di <strong>Prototype Glass Showroom</strong>. Mau tahu cara menjelajahi dan menyalin komponen ini dengan cepat?",
            selector: null,
            pointerText: null,
            btnText: "Mulai Tur 🧭"
        },
        {
            title: "1. Filter Kategori Komponen",
            message: "Gunakan bilah filter ini untuk menyaring komponen berdasarkan tipe: <strong>Buttons</strong>, <strong>Cards</strong>, <strong>Inputs</strong>, hingga <strong>UI Kits</strong> lengkap.",
            selector: "#filterTabs, .filter-tabs",
            pointerText: "👉 Pilih Kategori di Sini",
            btnText: "Lanjut"
        },
        {
            title: "2. Selektor Kolom Tata Letak",
            message: "Kamu bisa menyesuaikan tampilan grid menjadi <strong>1, 2, 3, 4, atau Auto kolom</strong> agar nyaman dilihat di layar monitor maupun laptop.",
            selector: ".layout-selector, .controls-right",
            pointerText: "👉 Atur Kolom Layar",
            btnText: "Lanjut"
        },
        {
            title: "3. Ganti Latar Kaca (Obsidian / Mesh)",
            message: "Ganti latar halaman antara <strong>Obsidian Dark</strong> pekat atau <strong>Mesh Gradient</strong> untuk melihat efek refraksi kaca secara dramatis!",
            selector: ".grid-bg-selector",
            pointerText: "👉 Ganti Latar Belakang",
            btnText: "Lanjut"
        },
        {
            title: "4. Salin Kode All-in-One Instant",
            message: "Setiap komponen bersifat <strong>mandiri (all-in-one)</strong>. Cukup klik tombol <strong>Salin</strong> untuk copy seluruh kode HTML+CSS+JS tanpa perlu install library!",
            selector: ".card-actions-tools, .component-card:first-of-type .card-actions-tools",
            pointerText: "👉 Salin Kode Sekali Klik",
            btnText: "Lanjut"
        },
        {
            title: "5. Component Studio Fullscreen",
            message: "Klik tombol <strong>Full</strong> pada kartu mana pun untuk membuka playground interaktif dengan pengatur ukuran layar dan tab editor kode multi-file.",
            selector: ".btn-card-full, .component-card:first-of-type .btn-card-full",
            pointerText: "👉 Buka Playground Studio",
            btnText: "Selesai ✦"
        }
    ];

    const gatewayTour = [
        {
            title: "Halo! Aku Gelly 👋",
            message: "Selamat datang di <strong>Master Gateway Prototype</strong>! Ini adalah pusat eksplorasi komponen web modern dan aplikasi utuh.",
            selector: null,
            pointerText: null,
            btnText: "Jelajahi Workspace"
        },
        {
            title: "1. Web Applications Studio",
            message: "Jelajahi proyek aplikasi web siap pakai seperti <strong>Cloud File Manager</strong> dan <strong>AI Agent Studio</strong> lengkap dengan simulator multi-perangkat.",
            selector: ".hub-card[href*='apps.html'], .hub-grid a:first-child",
            pointerText: "👉 Proyek Web Utuh",
            btnText: "Lanjut"
        },
        {
            title: "2. Glass Style Showcase",
            message: "Katalog <strong>44 komponen Glass Dark Premium</strong> mandiri bebas dependensi dengan live preview dan editor kode interaktif.",
            selector: ".hub-card[href*='showcase.html'], .hub-grid a:nth-child(2)",
            pointerText: "👉 Koleksi Komponen Glass",
            btnText: "Lanjut"
        },
        {
            title: "3. Raw Semantic HTML & Taksonomi",
            message: "Koleksi komponen murni tanpa styling CSS dan kamus audit 120+ elemen web baku untuk referensi struktur semantik standar.",
            selector: ".hub-card[href*='raw/showcase.html'], .hub-grid a:nth-child(3)",
            pointerText: "👉 Struktur Semantik Baku",
            btnText: "Selesai ✦"
        }
    ];

    const activeTourSteps = isShowcase ? showcaseTour : gatewayTour;
    let currentStepIndex = 0;

    /* --------------------------------------------------------------------------
       3. INJECT DOM ELEMENTS
       -------------------------------------------------------------------------- */
    function injectCompanionUI() {
        // Spotlight elements
        const overlay = document.createElement('div');
        overlay.id = 'gellySpotlightOverlay';
        overlay.className = 'gelly-spotlight-overlay';
        overlay.onclick = () => hideSpotlight();

        const box = document.createElement('div');
        box.id = 'gellySpotlightBox';
        box.className = 'gelly-spotlight-box';
        box.style.display = 'none';

        const badge = document.createElement('div');
        badge.id = 'gellyPointerBadge';
        badge.className = 'gelly-pointer-badge';
        badge.style.display = 'none';
        badge.innerHTML = `<i data-lucide="sparkles"></i> <span id="gellyPointerText">Panduan</span>`;

        // Blob Mascot Container
        const companion = document.createElement('div');
        companion.id = 'gellyCompanionContainer';
        companion.className = 'gelly-companion-container';

        const canvas = document.createElement('canvas');
        canvas.id = 'gellyCanvas';
        canvas.className = 'gelly-canvas';
        canvas.width = 280;
        canvas.height = 280;
        canvas.title = "Hai! Klik aku untuk membuka panduan.";

        const pingDot = document.createElement('div');
        pingDot.className = 'gelly-ping-dot';
        pingDot.title = "Tips baru tersedia!";

        companion.appendChild(canvas);
        companion.appendChild(pingDot);

        // Speech Bubble Wrapper
        const bubbleWrapper = document.createElement('div');
        bubbleWrapper.id = 'gellyBubbleWrapper';
        bubbleWrapper.className = 'gelly-bubble-wrapper';

        bubbleWrapper.innerHTML = `
            <div class="gelly-bubble">
                <div class="gelly-bubble-header">
                    <div class="gelly-badge">
                        <span class="gelly-badge-dot"></span>
                        <span>Panduan</span>
                        <span class="gelly-step-counter" id="gellyStepCounter"></span>
                    </div>
                    <div class="gelly-header-tools">
                        <button type="button" class="gelly-tool-btn" id="gellySoundBtn" title="Aktifkan/Matikan Suara">
                            <i data-lucide="${isMuted ? 'volume-x' : 'volume-2'}"></i>
                        </button>
                        <button type="button" class="gelly-tool-btn" id="gellyMinimizeBtn" title="Kecilkan Pemandu">
                            <i data-lucide="minus"></i>
                        </button>
                        <button type="button" class="gelly-tool-btn" id="gellyCloseBtn" title="Tutup Balon Chat">
                            <i data-lucide="x"></i>
                        </button>
                    </div>
                </div>

                <div class="gelly-bubble-content">
                    <h4 class="gelly-title" id="gellyTitle">Pemandu Prototype</h4>
                    <p class="gelly-message" id="gellyMessage">Memuat panduan interaktif...</p>
                </div>

                <!-- Quick Topic Selector -->
                <div class="gelly-topics-row">
                    <button type="button" class="gelly-topic-pill" data-topic="tour">
                        <i data-lucide="compass"></i> Tur Cepat
                    </button>
                    <button type="button" class="gelly-topic-pill" data-topic="copy">
                        <i data-lucide="copy"></i> Salin Kode
                    </button>
                    <button type="button" class="gelly-topic-pill" data-topic="bg">
                        <i data-lucide="palette"></i> Ganti Latar
                    </button>
                    <button type="button" class="gelly-topic-pill" data-topic="apps">
                        <i data-lucide="folder-kanban"></i> Web Apps
                    </button>
                </div>

                <div class="gelly-actions-footer">
                    <button type="button" class="gelly-btn-action secondary" id="gellyPrevBtn" style="display: none;">
                        <i data-lucide="arrow-left"></i> Kembali
                    </button>
                    <button type="button" class="gelly-btn-action highlight" id="gellyHighlightBtn" style="display: none;">
                        <i data-lucide="crosshair"></i> Tunjukkan
                    </button>
                    <button type="button" class="gelly-btn-action primary" id="gellyNextBtn">
                        Lanjut <i data-lucide="arrow-right"></i>
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);
        document.body.appendChild(box);
        document.body.appendChild(badge);
        document.body.appendChild(companion);
        document.body.appendChild(bubbleWrapper);

        if (window.lucide && typeof window.lucide.createIcons === 'function') {
            window.lucide.createIcons();
        }
    }

    /* --------------------------------------------------------------------------
       4. SPOTLIGHT HIGHLIGHTING ENGINE
       -------------------------------------------------------------------------- */
    let currentHighlightedElement = null;

    function highlightElement(selector, pointerText = "👉 Di Sini!") {
        if (!selector) {
            hideSpotlight();
            return;
        }

        const el = document.querySelector(selector);
        if (!el) {
            hideSpotlight();
            return;
        }

        currentHighlightedElement = el;

        // Smooth scroll to target element
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });

        setTimeout(() => {
            updateSpotlightRect(el, pointerText);
        }, 250);
    }

    function updateSpotlightRect(el, pointerText) {
        if (!el) return;
        const rect = el.getBoundingClientRect();
        const overlay = document.getElementById('gellySpotlightOverlay');
        const box = document.getElementById('gellySpotlightBox');
        const badge = document.getElementById('gellyPointerBadge');
        const badgeText = document.getElementById('gellyPointerText');

        if (!overlay || !box || !badge) return;

        const zoom = parseFloat(getComputedStyle(document.documentElement).zoom) || 1;
        const pad = 8;
        const top = (rect.top / zoom) - pad;
        const left = (rect.left / zoom) - pad;
        const width = (rect.width / zoom) + (pad * 2);
        const height = (rect.height / zoom) + (pad * 2);

        box.style.display = 'block';
        box.style.top = `${Math.max(4, top)}px`;
        box.style.left = `${Math.max(4, left)}px`;
        box.style.width = `${width}px`;
        box.style.height = `${height}px`;

        if (badgeText && pointerText) {
            badgeText.innerText = pointerText;
        }

        badge.style.display = 'flex';
        // Position badge above or below depending on available space
        if (top > 60) {
            badge.style.top = `${top - 42}px`;
            badge.style.left = `${Math.min((window.innerWidth / zoom) - 180, Math.max(12, left))}px`;
        } else {
            badge.style.top = `${top + height + 14}px`;
            badge.style.left = `${Math.min((window.innerWidth / zoom) - 180, Math.max(12, left))}px`;
        }

        overlay.classList.add('active');
        if (window.lucide) window.lucide.createIcons();
    }

    function hideSpotlight() {
        const overlay = document.getElementById('gellySpotlightOverlay');
        const box = document.getElementById('gellySpotlightBox');
        const badge = document.getElementById('gellyPointerBadge');
        if (overlay) overlay.classList.remove('active');
        if (box) box.style.display = 'none';
        if (badge) badge.style.display = 'none';
        currentHighlightedElement = null;
    }

    // Keep spotlight aligned during scroll/resize
    window.addEventListener('scroll', () => {
        if (currentHighlightedElement) {
            const badge = document.getElementById('gellyPointerBadge');
            const pointerText = badge ? document.getElementById('gellyPointerText').innerText : "Panduan";
            updateSpotlightRect(currentHighlightedElement, pointerText);
        }
    }, { passive: true });

    window.addEventListener('resize', () => {
        if (currentHighlightedElement) {
            const badge = document.getElementById('gellyPointerBadge');
            const pointerText = badge ? document.getElementById('gellyPointerText').innerText : "Panduan";
            updateSpotlightRect(currentHighlightedElement, pointerText);
        }
    });

    /* --------------------------------------------------------------------------
       5. SPEECH BUBBLE CONTROLS
       -------------------------------------------------------------------------- */
    let isBubbleOpen = false;

    function showBubble() {
        const bubble = document.getElementById('gellyBubbleWrapper');
        const container = document.getElementById('gellyCompanionContainer');
        if (bubble) bubble.classList.add('active');
        if (container) container.classList.remove('minimized', 'has-unread');
        isBubbleOpen = true;
        renderTourStep(currentStepIndex);
        playSound('pop');
    }

    function hideBubble() {
        const bubble = document.getElementById('gellyBubbleWrapper');
        if (bubble) bubble.classList.remove('active');
        isBubbleOpen = false;
        hideSpotlight();
    }

    function toggleBubble() {
        if (isBubbleOpen) {
            hideBubble();
        } else {
            showBubble();
        }
    }

    function renderTourStep(index) {
        if (index < 0) index = 0;
        if (index >= activeTourSteps.length) {
            // Tour finished!
            hideSpotlight();
            playSound('chime');
            currentStepIndex = 0;
            document.getElementById('gellyTitle').innerText = "Kamu Siap Bereksplorasi! 🎉";
            document.getElementById('gellyMessage').innerHTML = "Semua fitur utama sudah kamu kenali. Klik aku lagi kapan pun kamu butuh tips atau panduan.";
            document.getElementById('gellyStepCounter').innerText = "Selesai";
            document.getElementById('gellyPrevBtn').style.display = 'none';
            document.getElementById('gellyHighlightBtn').style.display = 'none';
            document.getElementById('gellyNextBtn').innerHTML = `Tutup <i data-lucide="check"></i>`;
            if (window.lucide) window.lucide.createIcons();
            return;
        }

        currentStepIndex = index;
        const step = activeTourSteps[currentStepIndex];

        document.getElementById('gellyTitle').innerText = step.title;
        document.getElementById('gellyMessage').innerHTML = step.message;
        document.getElementById('gellyStepCounter').innerText = `(${currentStepIndex + 1}/${activeTourSteps.length})`;

        const prevBtn = document.getElementById('gellyPrevBtn');
        const nextBtn = document.getElementById('gellyNextBtn');
        const hlBtn = document.getElementById('gellyHighlightBtn');

        prevBtn.style.display = currentStepIndex > 0 ? 'inline-flex' : 'none';
        
        if (step.selector && document.querySelector(step.selector)) {
            hlBtn.style.display = 'inline-flex';
            // Auto highlight step element
            highlightElement(step.selector, step.pointerText);
        } else {
            hlBtn.style.display = 'none';
            hideSpotlight();
        }

        const isLast = currentStepIndex === activeTourSteps.length - 1;
        nextBtn.innerHTML = isLast ? `Selesai <i data-lucide="check"></i>` : `${step.btnText || 'Lanjut'} <i data-lucide="arrow-right"></i>`;

        if (window.lucide) window.lucide.createIcons();
        playSound('pop');
    }

    function setupBubbleEvents() {
        const closeBtn = document.getElementById('gellyCloseBtn');
        const minBtn = document.getElementById('gellyMinimizeBtn');
        const soundBtn = document.getElementById('gellySoundBtn');
        const nextBtn = document.getElementById('gellyNextBtn');
        const prevBtn = document.getElementById('gellyPrevBtn');
        const hlBtn = document.getElementById('gellyHighlightBtn');

        if (closeBtn) closeBtn.onclick = () => hideBubble();
        
        if (minBtn) {
            minBtn.onclick = () => {
                hideBubble();
                const container = document.getElementById('gellyCompanionContainer');
                if (container) container.classList.add('minimized');
                playSound('squish');
            };
        }

        if (soundBtn) {
            soundBtn.onclick = () => {
                isMuted = !isMuted;
                localStorage.setItem('gelly_sound_muted', isMuted ? 'true' : 'false');
                soundBtn.innerHTML = `<i data-lucide="${isMuted ? 'volume-x' : 'volume-2'}"></i>`;
                if (window.lucide) window.lucide.createIcons();
                if (!isMuted) playSound('pop');
            };
        }

        if (nextBtn) {
            nextBtn.onclick = () => {
                if (currentStepIndex >= activeTourSteps.length - 1 && nextBtn.innerText.includes('Tutup')) {
                    hideBubble();
                } else {
                    renderTourStep(currentStepIndex + 1);
                }
            };
        }

        if (prevBtn) {
            prevBtn.onclick = () => {
                renderTourStep(currentStepIndex - 1);
            };
        }

        if (hlBtn) {
            hlBtn.onclick = () => {
                const step = activeTourSteps[currentStepIndex];
                if (step && step.selector) {
                    highlightElement(step.selector, step.pointerText);
                    playSound('chime');
                }
            };
        }

        // Quick topic pills
        document.querySelectorAll('.gelly-topic-pill').forEach(pill => {
            pill.onclick = function () {
                const topic = this.getAttribute('data-topic');
                if (topic === 'tour') {
                    renderTourStep(0);
                } else if (topic === 'copy') {
                    document.getElementById('gellyTitle').innerText = "Cara Salin Kode Mandiri";
                    document.getElementById('gellyMessage').innerHTML = "Setiap kartu memiliki tombol <strong>Salin</strong>. Begitu diklik, seluruh HTML, CSS variabel, dan JavaScript interaktif langsung tersalin ke clipboard tanpa perlu install dependency.";
                    highlightElement('.card-actions-tools, .component-card:first-of-type .card-actions-tools', "👉 Tombol Salin Instan");
                    playSound('pop');
                } else if (topic === 'bg') {
                    document.getElementById('gellyTitle').innerText = "Ganti Tema Latar Kaca";
                    document.getElementById('gellyMessage').innerHTML = "Pilih tombol <strong>Mesh Gradient</strong> pada header untuk mengaktifkan wallpaper dinamis, atau gunakan switch per kartu untuk menguji kontras.";
                    highlightElement('.grid-bg-selector', "👉 Switcher Tema Latar");
                    playSound('pop');
                } else if (topic === 'apps') {
                    document.getElementById('gellyTitle').innerText = "Web Applications Studio";
                    document.getElementById('gellyMessage').innerHTML = "Mau melihat aplikasi skala penuh? Kunjungi <strong>Web Applications Studio</strong> untuk simulator multi-perangkat (Mobile & Desktop).";
                    highlightElement("a[href*='apps.html']", "👉 Buka Web Applications");
                    playSound('pop');
                }
            };
        });
    }

    /* --------------------------------------------------------------------------
       6. FERALUI-INSPIRED SOFT-BODY SPRING PHYSICS JELLY BLOB
       -------------------------------------------------------------------------- */
    function initGellyPhysicsCanvas() {
        const canvas = document.getElementById('gellyCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const width = 280;
        const height = 280;
        const cx = 180; // Center offset towards bottom-right so blob peeks out diagonally
        const cy = 180;
        const baseRadius = 100;

        // Create 18 spring points on the perimeter
        const numPoints = 18;
        const points = [];
        for (let i = 0; i < numPoints; i++) {
            const angle = (i / numPoints) * (Math.PI * 2);
            points.push({
                baseAngle: angle,
                angle: angle,
                baseRadius: baseRadius,
                currentRadius: baseRadius,
                targetRadius: baseRadius,
                vx: 0,
                vy: 0,
                vr: 0
            });
        }

        // Global squish impulse variables
        let squashX = 1;
        let squashY = 1;
        let squashVx = 0;
        let squashVy = 0;

        // Eye tracking & blinking
        let mouseScreenX = window.innerWidth / 2;
        let mouseScreenY = window.innerHeight / 2;
        let isHovered = false;
        let blinkProgress = 0;
        let isBlinking = false;
        let nextBlinkTime = Date.now() + 3000;
        let talkBounce = 0;

        window.addEventListener('mousemove', (e) => {
            mouseScreenX = e.clientX;
            mouseScreenY = e.clientY;

            // Check if cursor is near Gelly's bottom-right corner
            const rect = canvas.getBoundingClientRect();
            const canvasX = e.clientX - rect.left;
            const canvasY = e.clientY - rect.top;

            if (canvasX >= 0 && canvasX <= rect.width && canvasY >= 0 && canvasY <= rect.height) {
                isHovered = true;
                // Deform closest vertex slightly
                const mouseAngle = Math.atan2(canvasY * 2 - cy, canvasX * 2 - cx);
                points.forEach(p => {
                    const diff = Math.abs(p.angle - mouseAngle);
                    if (diff < 0.6 || Math.abs(diff - Math.PI * 2) < 0.6) {
                        p.vr += 3.5;
                    }
                });
            } else {
                isHovered = false;
            }
        });

        // Click / Squish interaction
        canvas.addEventListener('click', () => {
            // Elastic squish impulse
            squashX = 1.35;
            squashY = 0.72;
            squashVx = -0.2;
            squashVy = 0.2;

            // Perturb points randomly for organic jiggle
            points.forEach((p, idx) => {
                p.vr += (Math.random() - 0.5) * 20;
            });

            playSound('squish');
            toggleBubble();
        });

        // Animation Loop
        let lastTime = performance.now();

        function render(now) {
            const dt = Math.min((now - lastTime) / 1000, 0.1);
            lastTime = now;

            // 1. Spring physics simulation for overall squish
            const springK = 75;
            const springDamp = 6.5;

            const fx = (1 - squashX) * springK - squashVx * springDamp;
            squashVx += fx * dt;
            squashX += squashVx * dt;

            const fy = (1 - squashY) * springK - squashVy * springDamp;
            squashVy += fy * dt;
            squashY += squashVy * dt;

            // 2. Point vertices radial spring simulation
            const pSpringK = 80;
            const pDamp = 6;
            const waveTime = now * 0.002;

            points.forEach((p, i) => {
                // Subtle organic idle breathing wave
                const idleOffset = Math.sin(waveTime + i * 0.8) * 3.5;
                const target = p.baseRadius + idleOffset;

                const force = (target - p.currentRadius) * pSpringK - p.vr * pDamp;
                p.vr += force * dt;
                p.currentRadius += p.vr * dt;
            });

            // 3. Eye blinking logic
            if (now > nextBlinkTime && !isBlinking) {
                isBlinking = true;
                blinkProgress = 0;
            }

            if (isBlinking) {
                blinkProgress += dt * 9;
                if (blinkProgress >= 1) {
                    isBlinking = false;
                    blinkProgress = 0;
                    nextBlinkTime = now + (2500 + Math.random() * 4000);
                }
            }

            // 4. Render Blob
            ctx.clearRect(0, 0, width, height);
            ctx.save();

            // Apply squish centered on (cx, cy)
            ctx.translate(cx, cy);
            ctx.scale(squashX, squashY);
            ctx.translate(-cx, -cy);

            // Compute polygon points
            const coords = points.map(p => {
                const x = cx + Math.cos(p.angle) * p.currentRadius;
                const y = cy + Math.sin(p.angle) * p.currentRadius;
                return { x, y };
            });

            // Draw jelly shape using smooth curves
            ctx.beginPath();
            ctx.moveTo((coords[0].x + coords[coords.length - 1].x) / 2, (coords[0].y + coords[coords.length - 1].y) / 2);

            for (let i = 0; i < coords.length; i++) {
                const p1 = coords[i];
                const p2 = coords[(i + 1) % coords.length];
                const midX = (p1.x + p2.x) / 2;
                const midY = (p1.y + p2.y) / 2;
                ctx.quadraticCurveTo(p1.x, p1.y, midX, midY);
            }
            ctx.closePath();

            // Gradient fill (Cyber cyan -> Deep Indigo -> Purple glow)
            const grad = ctx.createRadialGradient(cx - 35, cy - 35, 15, cx, cy, baseRadius * 1.3);
            grad.addColorStop(0, '#38BDF8');
            grad.addColorStop(0.4, '#0284C7');
            grad.addColorStop(0.8, '#4F46E5');
            grad.addColorStop(1, '#6B21A8');
            ctx.fillStyle = grad;
            ctx.fill();

            // Caustic Specular Gloss Highlight (top-left inner shine)
            ctx.save();
            ctx.clip();
            const specGrad = ctx.createRadialGradient(cx - 50, cy - 50, 5, cx - 35, cy - 35, 60);
            specGrad.addColorStop(0, 'rgba(255, 255, 255, 0.65)');
            specGrad.addColorStop(0.5, 'rgba(56, 189, 248, 0.25)');
            specGrad.addColorStop(1, 'transparent');
            ctx.fillStyle = specGrad;
            ctx.beginPath();
            ctx.arc(cx - 35, cy - 35, 60, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // Specular perimeter stroke
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
            ctx.lineWidth = 2.5;
            ctx.stroke();

            // 5. Draw Cartoon Eyes & Pupils (Pupils follow mouse cursor)
            const rect = canvas.getBoundingClientRect();
            const eye1Center = { x: cx - 42, y: cy - 38 };
            const eye2Center = { x: cx - 6, y: cy - 46 };

            const eyeScreen1 = {
                x: rect.left + (eye1Center.x / 2),
                y: rect.top + (eye1Center.y / 2)
            };
            const eyeScreen2 = {
                x: rect.left + (eye2Center.x / 2),
                y: rect.top + (eye2Center.y / 2)
            };

            const angle1 = Math.atan2(mouseScreenY - eyeScreen1.y, mouseScreenX - eyeScreen1.x);
            const angle2 = Math.atan2(mouseScreenY - eyeScreen2.y, mouseScreenX - eyeScreen2.x);

            const maxPupilOffset = 6;
            const pupil1 = {
                x: eye1Center.x + Math.cos(angle1) * maxPupilOffset,
                y: eye1Center.y + Math.sin(angle1) * maxPupilOffset
            };
            const pupil2 = {
                x: eye2Center.x + Math.cos(angle2) * maxPupilOffset,
                y: eye2Center.y + Math.sin(angle2) * maxPupilOffset
            };

            // Blink factor (1 = open, 0.08 = closed)
            const blinkFactor = isBlinking ? (1 - Math.sin(blinkProgress * Math.PI) * 0.92) : 1;

            function drawEye(center, pupil, radius) {
                ctx.save();
                ctx.translate(center.x, center.y);
                ctx.scale(1, blinkFactor);
                ctx.translate(-center.x, -center.y);

                // White sclera with soft shadow
                ctx.fillStyle = '#FFFFFF';
                ctx.beginPath();
                ctx.arc(center.x, center.y, radius, 0, Math.PI * 2);
                ctx.fill();

                if (blinkFactor > 0.3) {
                    // Dark pupil
                    ctx.fillStyle = '#0F172A';
                    ctx.beginPath();
                    ctx.arc(pupil.x, pupil.y, radius * 0.52, 0, Math.PI * 2);
                    ctx.fill();

                    // White sparkle reflection
                    ctx.fillStyle = '#FFFFFF';
                    ctx.beginPath();
                    ctx.arc(pupil.x - 2.5, pupil.y - 2.5, radius * 0.2, 0, Math.PI * 2);
                    ctx.fill();
                }

                ctx.restore();
            }

            drawEye(eye1Center, pupil1, 15);
            drawEye(eye2Center, pupil2, 14);

            // Cute Happy Mouth
            ctx.save();
            ctx.strokeStyle = '#0F172A';
            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            ctx.beginPath();
            const mouthCenter = { x: cx - 22, y: cy - 14 };
            if (isHovered || isBubbleOpen) {
                // Wide happy smile
                ctx.arc(mouthCenter.x, mouthCenter.y, 8, 0.15 * Math.PI, 0.85 * Math.PI, false);
            } else {
                // Subtle calm curve
                ctx.arc(mouthCenter.x, mouthCenter.y, 6, 0.2 * Math.PI, 0.8 * Math.PI, false);
            }
            ctx.stroke();
            ctx.restore();

            // Cheerful Cheek Blush
            ctx.fillStyle = 'rgba(244, 114, 182, 0.4)';
            ctx.beginPath();
            ctx.arc(cx - 56, cy - 24, 7, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(cx + 8, cy - 32, 6, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();
            requestAnimationFrame(render);
        }

        requestAnimationFrame(render);
    }

    /* --------------------------------------------------------------------------
       7. INITIALIZE WHEN DOM IS READY
       -------------------------------------------------------------------------- */
    function init() {
        injectCompanionUI();
        setupBubbleEvents();
        initGellyPhysicsCanvas();

        // Check if user is first-time visitor on showcase or home
        const hasSeenTour = localStorage.getItem('gelly_tour_seen_v2');
        if (!hasSeenTour) {
            // Friendly automatic introduction after 900ms
            setTimeout(() => {
                showBubble();
                localStorage.setItem('gelly_tour_seen_v2', 'true');
            }, 900);
        } else {
            // Show subtle notification ping dot on Gelly
            const container = document.getElementById('gellyCompanionContainer');
            if (container) container.classList.add('has-unread');
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
