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
 * - Step-by-step beginner friendly interactive tour with crystal clear spotlight
 * - Contextual conversations on page navigation (Gateway, Glass, Web Apps, Raw)
 * - Casual banter / "Basa-Basi" conversation engine with witty trivia
 * - Fully responsive & ergonomic on mobile screens (<=680px)
 * - Procedural Web Audio API sound effects (pop, chime, squish)
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
                osc.type = 'sine';
                osc.frequency.setValueAtTime(480, now);
                osc.frequency.exponentialRampToValueAtTime(780, now + 0.08);
                gain.gain.setValueAtTime(0.14, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
                osc.start(now);
                osc.stop(now + 0.1);
            } else if (type === 'chime') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(523.25, now);
                osc.frequency.setValueAtTime(659.25, now + 0.07);
                osc.frequency.setValueAtTime(783.99, now + 0.14);
                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
                osc.start(now);
                osc.stop(now + 0.3);
            } else if (type === 'squish') {
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
       2. PAGE IDENTIFICATION & CONTEXTUAL GREETINGS
       -------------------------------------------------------------------------- */
    const path = window.location.pathname.toLowerCase();
    const isGlassShowcase = path.includes('glass/showcase.html') || (path.includes('showcase.html') && !path.includes('raw'));
    const isRawShowcase = path.includes('raw/showcase.html') || path.includes('raw');
    const isWebApps = path.includes('apps.html') || path.includes('web-apps');
    const isGateway = !isGlassShowcase && !isRawShowcase && !isWebApps;

    let currentPageKey = 'gateway';
    if (isGlassShowcase) currentPageKey = 'glass';
    else if (isWebApps) currentPageKey = 'webapps';
    else if (isRawShowcase) currentPageKey = 'raw';

    const pageGreetings = {
        gateway: {
            title: "Halo di Master Gateway! 🏛️",
            message: "Ini beranda utama <strong>Prototype</strong>! Dari sini kamu bisa meluncur ke <strong>Glass Showcase</strong> (44 komponen kaca), <strong>Web Apps Studio</strong> (aplikasi web utuh), atau <strong>Raw HTML</strong> (komponen murni). Mau mulai eksplorasi?",
            badge: "Gateway Portal"
        },
        glass: {
            title: "Showroom Glass Dark! ✨",
            message: "Wah, kamu sampai di <strong>Glass Showroom</strong>! Di sini ada 44 komponen dark glass mandiri. Mau coba acak susunan pakai tombol <strong>Randomize</strong>, atau mau kuantar keliling melihat seluruh grid dan kodenya?",
            badge: "Glass Showroom"
        },
        webapps: {
            title: "Web Applications Studio! 🚀",
            message: "Ini dia <strong>Web Applications Studio</strong>! Di sini bukan cuma potongan komponen terpisah, tapi aplikasi web utuh yang jalan beneran (Cloud File Manager & AI Studio). Coba ganti ke simulator <strong>Mobile</strong> atau <strong>Desktop</strong>!",
            badge: "Web Apps Studio"
        },
        raw: {
            title: "Raw HTML5 Showcase! 📐",
            message: "Selamat datang di <strong>Raw Showcase</strong>! Komponen di sini murni HTML5 semantik tanpa sentuhan CSS, pas banget buat referensi anatomi baku dan peran ARIA sebelum dihias.",
            badge: "Raw Semantic"
        }
    };

    /* --------------------------------------------------------------------------
       3. CONVERSATIONS BASA-BASI (Casual Banter & Fun Trivia)
       -------------------------------------------------------------------------- */
    const casualBanterList = [
        {
            title: "Kenapa Desain Kaca? 💎",
            message: "Pernah kepikiran kenapa efek glassmorphism disukai? Pantulan blur dan border halusnya bikin mata kita reflek fokus ke konten inti tanpa ngerasa terdistraksi!"
        },
        {
            title: "Bebas dari NPM & Build Tool! 🚀",
            message: "Semua komponen di web ini 100% mandiri lho! Kamu nggak perlu pusing install paket npm atau bundler berat, cukup copas dan jalan langsung di browser."
        },
        {
            title: "Sensasi Acak Grid 🎲",
            message: "Ngaku deh, kamu tadi sempat klik tombol Randomize di atas kan? Seru banget ya ngeliat 44 kartu komponennya saling bertukar posisi secara dinamis!"
        },
        {
            title: "Rahasia Background Switcher 🎨",
            message: "Di samping tombol Salin tiap kartu ada switch dot hitam dan gradien. Itu berguna banget buat ngetes apakah komponen kaca terbaca jelas di berbagai jenis wallpaper!"
        },
        {
            title: "Dark Mode Ramah Mata 🌙",
            message: "Tema Obsidian Dark di sini didesain dengan saturasi seimbang. Mau coding sampai larut malam pun mata tetap adem dan nggak gampang lelah."
        },
        {
            title: "Responsif di Semua Layar 📱",
            message: "Kalau kamu buka Prototype di layar HP atau tablet, tampilanku otomatis menyesuaikan diri biar jempolmu tetap leluasa berselancar tanpa terhalang!"
        },
        {
            title: "Component Studio Tersembunyi 🔍",
            message: "Klik tombol 'Full' di pojok kartu mana pun! Di situ kamu bisa tarik resizer layarnya buat simulasi ukuran HP, tablet, maupun layar desktop."
        },
        {
            title: "Fisika Kenyal FeralUI 🐾",
            message: "Fisika tubuhku ini terinspirasi dari FeralUI Blob lho. Coba gerak-gerakin kursor mepet ke aku atau klik sekali, kenyal banget kan?"
        },
        {
            title: "AI Model Selector Card 🧠",
            message: "Sekarang kartu arsitektur AI sudah bersih dari tombol acak dummy. Tampilannya jauh lebih rapi, terstruktur, dan siap dipakai produksi!"
        },
        {
            title: "Jelajahi Web Apps Studio 📦",
            message: "Udah mampir ke Web Applications Studio belum? Di sana ada Cloud File Manager dan AI Agent Studio yang jalan beneran layaknya aplikasi utuh!"
        },
        {
            title: "Selalu Siap Membantu ✨",
            message: "Aku bakal tetap standby di pojokan sini ya. Kalau kamu butuh panduan, petunjuk fitur, atau sekadar pengen disapa, klik aku kapan pun!"
        }
    ];

    let banterIndex = 0;

    /* --------------------------------------------------------------------------
       4. STEP-BY-STEP TOUR CONFIGURATIONS
       -------------------------------------------------------------------------- */
    const showcaseTour = [
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
            title: "3. Grid Showroom Komponen (44 Kartu)",
            message: "Ini dia <strong>grid utama showroom</strong> yang memuat seluruh 44 komponen interaktif mandiri! Setiap kartu dapat langsung kamu coba dan interaksikan.",
            selector: "#componentsGrid, .components-grid",
            pointerText: "👉 Grid 44 Komponen Kaca",
            btnText: "Lanjut"
        },
        {
            title: "4. Ganti Latar Kaca (Obsidian / Mesh)",
            message: "Ganti latar halaman antara <strong>Obsidian Dark</strong> pekat atau <strong>Mesh Gradient</strong> untuk melihat efek refraksi kaca secara dramatis!",
            selector: ".grid-bg-selector",
            pointerText: "👉 Ganti Latar Belakang",
            btnText: "Lanjut"
        },
        {
            title: "5. Salin Kode All-in-One Instant",
            message: "Setiap komponen bersifat <strong>mandiri (all-in-one)</strong>. Cukup klik tombol <strong>Salin</strong> untuk copy seluruh kode HTML+CSS+JS tanpa perlu install library!",
            selector: ".card-actions-tools, .component-card:first-of-type .card-actions-tools",
            pointerText: "👉 Salin Kode Sekali Klik",
            btnText: "Lanjut"
        },
        {
            title: "6. Component Studio Fullscreen",
            message: "Klik tombol <strong>Full</strong> pada kartu mana pun untuk membuka playground interaktif dengan pengatur ukuran layar dan tab editor kode multi-file.",
            selector: ".btn-card-full, .component-card:first-of-type .btn-card-full",
            pointerText: "👉 Buka Playground Studio",
            btnText: "Selesai ✦"
        }
    ];

    const gatewayTour = [
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

    const webappsTour = [
        {
            title: "1. Panggung Simulator Aplikasi",
            message: "Area ini menampilkan aplikasi web aktif secara live di dalam simulator interaktif.",
            selector: "#stageSection, .app-showcase-box",
            pointerText: "👉 Panggung Simulator",
            btnText: "Lanjut"
        },
        {
            title: "2. Pengatur Ukuran Layar Multi-Device",
            message: "Uji coba responsivitas aplikasi dengan tombol switch ke ukuran <strong>Mobile</strong>, <strong>Tablet</strong>, atau <strong>Desktop</strong>!",
            selector: ".viewport-buttons, .mode-toggle-cluster",
            pointerText: "👉 Switch Ukuran Layar",
            btnText: "Lanjut"
        },
        {
            title: "3. Pilihan Proyek Aplikasi",
            message: "Ganti proyek aplikasi yang ingin kamu buka (Cloud File Manager, AI Studio) menggunakan tab ini.",
            selector: ".project-tabs-cluster, .projects-selection-bar",
            pointerText: "👉 Pilih Proyek Web",
            btnText: "Selesai ✦"
        }
    ];

    const rawTour = [
        {
            title: "1. Koleksi Komponen Murni HTML5",
            message: "Katalog seluruh elemen form baku, tabel, progress meter, dan modal bawaan peramban tanpa gaya CSS.",
            selector: ".raw-grid, .components-grid",
            pointerText: "👉 Komponen Murni",
            btnText: "Lanjut"
        },
        {
            title: "2. Navigasi & Master Gateway",
            message: "Gunakan navigasi atas untuk kembali ke Master Gateway atau beralih ke Glass Dark Showcase.",
            selector: ".header-actions",
            pointerText: "👉 Navigasi Kembali",
            btnText: "Selesai ✦"
        }
    ];

    let activeTourSteps = showcaseTour;
    if (isWebApps) activeTourSteps = webappsTour;
    else if (isRawShowcase) activeTourSteps = rawTour;
    else if (isGateway) activeTourSteps = gatewayTour;

    let currentStepIndex = 0;
    let isBanterMode = false;

    /* --------------------------------------------------------------------------
       5. INJECT DOM ELEMENTS
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
        canvas.title = "Hai! Klik aku untuk membuka panduan atau ngobrol.";

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
                        <span id="gellyBadgeText">${pageGreetings[currentPageKey].badge}</span>
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
                    <h4 class="gelly-title" id="gellyTitle">${pageGreetings[currentPageKey].title}</h4>
                    <p class="gelly-message" id="gellyMessage">${pageGreetings[currentPageKey].message}</p>
                </div>

                <!-- Quick Topic Selector Row -->
                <div class="gelly-topics-row">
                    <button type="button" class="gelly-topic-pill" data-topic="tour">
                        <i data-lucide="compass"></i> Tur Cepat
                    </button>
                    <button type="button" class="gelly-topic-pill" data-topic="chat">
                        <i data-lucide="message-circle"></i> Basa-Basi
                    </button>
                    ${isGlassShowcase ? `
                    <button type="button" class="gelly-topic-pill" data-topic="grid">
                        <i data-lucide="layout-grid"></i> Lihat Grid
                    </button>
                    <button type="button" class="gelly-topic-pill" data-topic="copy">
                        <i data-lucide="copy"></i> Salin Kode
                    </button>
                    <button type="button" class="gelly-topic-pill" data-topic="bg">
                        <i data-lucide="palette"></i> Ganti Latar
                    </button>
                    ` : `
                    <button type="button" class="gelly-topic-pill" data-topic="apps">
                        <i data-lucide="folder-kanban"></i> Web Apps
                    </button>
                    <button type="button" class="gelly-topic-pill" data-topic="glass">
                        <i data-lucide="gem"></i> Glass Showroom
                    </button>
                    `}
                </div>

                <div class="gelly-actions-footer">
                    <button type="button" class="gelly-btn-action secondary" id="gellyPrevBtn" style="display: none;">
                        <i data-lucide="arrow-left"></i> Kembali
                    </button>
                    <button type="button" class="gelly-btn-action highlight" id="gellyHighlightBtn" style="display: none;">
                        <i data-lucide="crosshair"></i> Tunjukkan
                    </button>
                    <button type="button" class="gelly-btn-action primary" id="gellyNextBtn">
                        Mulai Tur 🧭
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
       6. SPOTLIGHT HIGHLIGHTING ENGINE (Zero Blur, Zoom-Aware)
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

        // Smooth scroll into center view
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });

        setTimeout(() => {
            updateSpotlightRect(el, pointerText);
        }, 260);
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
        const pad = 10;
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
            badge.style.top = `${top - 44}px`;
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
       7. SPEECH BUBBLE CONTROLS & CONVERSATIONS
       -------------------------------------------------------------------------- */
    let isBubbleOpen = false;

    function showBubble() {
        const bubble = document.getElementById('gellyBubbleWrapper');
        const container = document.getElementById('gellyCompanionContainer');
        if (bubble) bubble.classList.add('active');
        if (container) container.classList.remove('minimized', 'has-unread');
        isBubbleOpen = true;
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
        isBanterMode = false;
        if (index < 0) index = 0;
        if (index >= activeTourSteps.length) {
            hideSpotlight();
            playSound('chime');
            currentStepIndex = 0;
            document.getElementById('gellyBadgeText').innerText = "Selesai";
            document.getElementById('gellyTitle').innerText = "Kamu Siap Bereksplorasi! 🎉";
            document.getElementById('gellyMessage').innerHTML = "Semua fitur utama sudah kamu kenali. Klik tombol <strong>Basa-Basi</strong> kalau mau ngobrol santai, atau panggil aku kapan pun!";
            document.getElementById('gellyStepCounter').innerText = "";
            document.getElementById('gellyPrevBtn').style.display = 'none';
            document.getElementById('gellyHighlightBtn').style.display = 'none';
            document.getElementById('gellyNextBtn').innerHTML = `Tutup <i data-lucide="check"></i>`;
            if (window.lucide) window.lucide.createIcons();
            return;
        }

        currentStepIndex = index;
        const step = activeTourSteps[currentStepIndex];

        document.getElementById('gellyBadgeText').innerText = "Tur Interaktif";
        document.getElementById('gellyTitle').innerText = step.title;
        document.getElementById('gellyMessage').innerHTML = step.message;
        document.getElementById('gellyStepCounter').innerText = `(${currentStepIndex + 1}/${activeTourSteps.length})`;

        const prevBtn = document.getElementById('gellyPrevBtn');
        const nextBtn = document.getElementById('gellyNextBtn');
        const hlBtn = document.getElementById('gellyHighlightBtn');

        prevBtn.style.display = currentStepIndex > 0 ? 'inline-flex' : 'none';
        
        if (step.selector && document.querySelector(step.selector)) {
            hlBtn.style.display = 'inline-flex';
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

    function renderCasualBanter() {
        isBanterMode = true;
        hideSpotlight();
        const banter = casualBanterList[banterIndex % casualBanterList.length];
        banterIndex++;

        document.getElementById('gellyBadgeText').innerText = "Basa-Basi 💬";
        document.getElementById('gellyStepCounter').innerText = "";
        document.getElementById('gellyTitle').innerText = banter.title;
        document.getElementById('gellyMessage').innerHTML = banter.message;

        document.getElementById('gellyPrevBtn').style.display = 'none';
        document.getElementById('gellyHighlightBtn').style.display = 'none';
        document.getElementById('gellyNextBtn').innerHTML = `Obrolan Lain 🎲`;

        if (window.lucide) window.lucide.createIcons();
        playSound('chime');
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
                if (isBanterMode) {
                    renderCasualBanter();
                } else if (nextBtn.innerText.includes('Mulai Tur')) {
                    renderTourStep(0);
                } else if (currentStepIndex >= activeTourSteps.length - 1 && nextBtn.innerText.includes('Tutup')) {
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
                } else if (topic === 'chat') {
                    renderCasualBanter();
                } else if (topic === 'grid') {
                    isBanterMode = false;
                    document.getElementById('gellyBadgeText').innerText = "Showroom Grid";
                    document.getElementById('gellyTitle').innerText = "Grid 44 Komponen Kaca";
                    document.getElementById('gellyMessage').innerHTML = "Ini dia grid showroom lengkap yang menampung 44 komponen interaktif! Kamu bisa mencoba langsung setiap komponen di dalam kartunya.";
                    highlightElement("#componentsGrid, .components-grid", "👉 Grid 44 Komponen Kaca");
                    document.getElementById('gellyNextBtn').innerHTML = `Lanjut <i data-lucide="arrow-right"></i>`;
                    playSound('pop');
                } else if (topic === 'copy') {
                    isBanterMode = false;
                    document.getElementById('gellyBadgeText').innerText = "Salin Kode";
                    document.getElementById('gellyTitle').innerText = "Cara Salin Kode Mandiri";
                    document.getElementById('gellyMessage').innerHTML = "Setiap kartu memiliki tombol <strong>Salin</strong>. Begitu diklik, seluruh HTML, CSS variabel, dan JavaScript interaktif langsung tersalin ke clipboard tanpa perlu install dependency.";
                    highlightElement('.card-actions-tools, .component-card:first-of-type .card-actions-tools', "👉 Tombol Salin Instan");
                    document.getElementById('gellyNextBtn').innerHTML = `Lanjut <i data-lucide="arrow-right"></i>`;
                    playSound('pop');
                } else if (topic === 'bg') {
                    isBanterMode = false;
                    document.getElementById('gellyBadgeText').innerText = "Tema Latar";
                    document.getElementById('gellyTitle').innerText = "Ganti Tema Latar Kaca";
                    document.getElementById('gellyMessage').innerHTML = "Pilih tombol <strong>Mesh Gradient</strong> pada header untuk mengaktifkan wallpaper dinamis, atau gunakan switch per kartu untuk menguji kontras.";
                    highlightElement('.grid-bg-selector', "👉 Switcher Tema Latar");
                    document.getElementById('gellyNextBtn').innerHTML = `Lanjut <i data-lucide="arrow-right"></i>`;
                    playSound('pop');
                } else if (topic === 'apps') {
                    window.location.href = isGlassShowcase ? '../../apps.html' : 'ui/web/apps.html';
                } else if (topic === 'glass') {
                    window.location.href = isWebApps ? 'components/glass/showcase.html' : 'ui/web/components/glass/showcase.html';
                }
            };
        });
    }

    /* --------------------------------------------------------------------------
       8. FERALUI-INSPIRED SOFT-BODY SPRING PHYSICS JELLY BLOB (Canvas 2D)
       -------------------------------------------------------------------------- */
    function initGellyPhysicsCanvas() {
        const canvas = document.getElementById('gellyCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const width = 280;
        const height = 280;
        const cx = 180; // Offset towards bottom-right so blob peeks out diagonally
        const cy = 180;
        const baseRadius = 100;

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

        let squashX = 1;
        let squashY = 1;
        let squashVx = 0;
        let squashVy = 0;

        let mouseScreenX = window.innerWidth / 2;
        let mouseScreenY = window.innerHeight / 2;
        let isHovered = false;
        let blinkProgress = 0;
        let isBlinking = false;
        let nextBlinkTime = Date.now() + 3000;

        window.addEventListener('mousemove', (e) => {
            mouseScreenX = e.clientX;
            mouseScreenY = e.clientY;

            const rect = canvas.getBoundingClientRect();
            const canvasX = e.clientX - rect.left;
            const canvasY = e.clientY - rect.top;

            if (canvasX >= 0 && canvasX <= rect.width && canvasY >= 0 && canvasY <= rect.height) {
                isHovered = true;
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

        // Touch support on mobile
        window.addEventListener('touchmove', (e) => {
            if (e.touches && e.touches[0]) {
                mouseScreenX = e.touches[0].clientX;
                mouseScreenY = e.touches[0].clientY;
            }
        }, { passive: true });

        canvas.addEventListener('click', () => {
            squashX = 1.35;
            squashY = 0.72;
            squashVx = -0.2;
            squashVy = 0.2;

            points.forEach((p) => {
                p.vr += (Math.random() - 0.5) * 20;
            });

            playSound('squish');
            toggleBubble();
        });

        let lastTime = performance.now();

        function render(now) {
            const dt = Math.min((now - lastTime) / 1000, 0.1);
            lastTime = now;

            const springK = 75;
            const springDamp = 6.5;

            const fx = (1 - squashX) * springK - squashVx * springDamp;
            squashVx += fx * dt;
            squashX += squashVx * dt;

            const fy = (1 - squashY) * springK - squashVy * springDamp;
            squashVy += fy * dt;
            squashY += squashVy * dt;

            const pSpringK = 80;
            const pDamp = 6;
            const waveTime = now * 0.002;

            points.forEach((p, i) => {
                const idleOffset = Math.sin(waveTime + i * 0.8) * 3.5;
                const target = p.baseRadius + idleOffset;

                const force = (target - p.currentRadius) * pSpringK - p.vr * pDamp;
                p.vr += force * dt;
                p.currentRadius += p.vr * dt;
            });

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

            ctx.clearRect(0, 0, width, height);
            ctx.save();

            ctx.translate(cx, cy);
            ctx.scale(squashX, squashY);
            ctx.translate(-cx, -cy);

            const coords = points.map(p => {
                const x = cx + Math.cos(p.angle) * p.currentRadius;
                const y = cy + Math.sin(p.angle) * p.currentRadius;
                return { x, y };
            });

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

            // Vibrant gradient
            const grad = ctx.createRadialGradient(cx - 35, cy - 35, 15, cx, cy, baseRadius * 1.3);
            grad.addColorStop(0, '#38BDF8');
            grad.addColorStop(0.4, '#0284C7');
            grad.addColorStop(0.8, '#4F46E5');
            grad.addColorStop(1, '#6B21A8');
            ctx.fillStyle = grad;
            ctx.fill();

            // Specular gloss
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

            ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
            ctx.lineWidth = 2.5;
            ctx.stroke();

            // Eyes & Pupil tracking
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

            const blinkFactor = isBlinking ? (1 - Math.sin(blinkProgress * Math.PI) * 0.92) : 1;

            function drawEye(center, pupil, radius) {
                ctx.save();
                ctx.translate(center.x, center.y);
                ctx.scale(1, blinkFactor);
                ctx.translate(-center.x, -center.y);

                ctx.fillStyle = '#FFFFFF';
                ctx.beginPath();
                ctx.arc(center.x, center.y, radius, 0, Math.PI * 2);
                ctx.fill();

                if (blinkFactor > 0.3) {
                    ctx.fillStyle = '#0F172A';
                    ctx.beginPath();
                    ctx.arc(pupil.x, pupil.y, radius * 0.52, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.fillStyle = '#FFFFFF';
                    ctx.beginPath();
                    ctx.arc(pupil.x - 2.5, pupil.y - 2.5, radius * 0.2, 0, Math.PI * 2);
                    ctx.fill();
                }

                ctx.restore();
            }

            drawEye(eye1Center, pupil1, 15);
            drawEye(eye2Center, pupil2, 14);

            // Cute smiling mouth
            ctx.save();
            ctx.strokeStyle = '#0F172A';
            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            ctx.beginPath();
            const mouthCenter = { x: cx - 22, y: cy - 14 };
            if (isHovered || isBubbleOpen || isBanterMode) {
                ctx.arc(mouthCenter.x, mouthCenter.y, 8, 0.15 * Math.PI, 0.85 * Math.PI, false);
            } else {
                ctx.arc(mouthCenter.x, mouthCenter.y, 6, 0.2 * Math.PI, 0.8 * Math.PI, false);
            }
            ctx.stroke();
            ctx.restore();

            // Blush
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
       9. INITIALIZE ON PAGE LOAD WITH CONTEXTUAL NAVIGATION SPEECH
       -------------------------------------------------------------------------- */
    function init() {
        injectCompanionUI();
        setupBubbleEvents();
        initGellyPhysicsCanvas();

        // Check if page switched
        const lastPage = sessionStorage.getItem('gelly_last_page');
        const isPageSwitch = lastPage && lastPage !== currentPageKey;
        sessionStorage.setItem('gelly_last_page', currentPageKey);

        // If newly switched to a page or first visit: greet user with contextual intro!
        if (isPageSwitch || !sessionStorage.getItem('gelly_welcomed')) {
            sessionStorage.setItem('gelly_welcomed', 'true');
            setTimeout(() => {
                showBubble();
            }, 600);
        } else {
            // Subtle ping dot
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
