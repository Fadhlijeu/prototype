/**
 * ==========================================================================
 * TATA — Interactive Physics-Driven Blob Companion & Guidance System
 * Inspired by FeralUI playful physics elements (https://feralui.dev/blob)
 * 
 * New Features:
 * - Mascot official name: "TATA" with grand introduction blur overlay
 * - Fullscreen website backdrop blur on first visit for Tata's introduction
 * - Active mobile touch tracking (touchstart/touchmove follows finger)
 * - Page-adaptive theme colors (Glass, Web Apps, Raw Semantic, Gateway)
 * - Natural automatic banter & jokes without manual buttons
 * - Animated facial expressions (laughing, winking, surprised, pondering)
 * - Random wander & jiggle walking upwards along screen edge
 * - Instant playful return slide when tapped during walking ("Balik ke pos!")
 * - Non-disappearing peek minimize (eyes keep watching and blinking)
 * - Ultra-translucent glass speech popup to prevent accidental misclicks
 * ==========================================================================
 */

(function () {
    'use strict';

    // Prevent duplicate initialization
    if (window.__TATA_COMPANION_INITIALIZED__) return;
    window.__TATA_COMPANION_INITIALIZED__ = true;

    /* --------------------------------------------------------------------------
       1. SOUND EFFECTS (Web Audio API)
       -------------------------------------------------------------------------- */
    let audioCtx = null;
    let isMuted = localStorage.getItem('tata_sound_muted') === 'true';

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
                osc.frequency.exponentialRampToValueAtTime(820, now + 0.08);
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
                osc.frequency.setValueAtTime(340, now);
                osc.frequency.exponentialRampToValueAtTime(160, now + 0.12);
                gain.gain.setValueAtTime(0.16, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.13);
                osc.start(now);
                osc.stop(now + 0.14);
            } else if (type === 'slide') {
                // Cartoon slide whistle return sound
                osc.type = 'sine';
                osc.frequency.setValueAtTime(650, now);
                osc.frequency.exponentialRampToValueAtTime(220, now + 0.25);
                gain.gain.setValueAtTime(0.15, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
                osc.start(now);
                osc.stop(now + 0.3);
            }
        } catch (e) {
            // Audio policy or unsupported fallback
        }
    }

    /* --------------------------------------------------------------------------
       2. PAGE IDENTIFICATION & THEME ADAPTATION
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

    // Apply theme class to body
    document.body.classList.add(`page-theme-${currentPageKey}`);

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
       3. SPONTANEOUS BANTER & JOKES (Without buttons! Natural banter)
       -------------------------------------------------------------------------- */
    const banterJokes = [
        {
            title: "Bebas AI Slop! 😎",
            message: "Pernah mikir nggak, kenapa komponen di sini nggak ada tombol dummy? Karena Tata benci AI slop yang nggak jelas!",
            expression: 'laugh'
        },
        {
            title: "Gombalan Kaca 🙈",
            message: "Kamu tahu bedanya kamu sama CSS Glass? Kalau CSS Glass mantulin cahaya, kalau kamu mantulin pesona... aseek!",
            expression: 'wink'
        },
        {
            title: "Adem di Mata ✨",
            message: "Kata siapa ngoding malem-malem bikin pusing? Asal pake dark mode sama liat aku senyum, dijamin langsung adem!",
            expression: 'happy'
        },
        {
            title: "Rahasia Perosotan 💨",
            message: "Psst... coba diemin aku bentar sampai aku jalan ke atas layar. Nanti kalau kamu klik aku pas lagi jalan, aku bakal meluncur balik kayak perosotan!",
            expression: 'wink'
        },
        {
            title: "AI Model Selector Rapi! 🧠",
            message: "Tadi aku ngintip kartu AI Model Selector, tombol acak dummy-nya udah hilang beneran, sekarang kelihatan profesional banget!",
            expression: 'happy'
        },
        {
            title: "Rebahan Dulu ☕",
            message: "Kalau kamu capek scroll 44 komponen, santai aja... rebahan bentar sambil ngopi, Tata yang jagain kodenya di sini.",
            expression: 'ponder'
        },
        {
            title: "Tombol Salin Gercep 📋",
            message: "Tombol Salin di kartu ini gercep banget lho. Sekali klik langsung nempel di clipboard tanpa perlu install dependency apa pun!",
            expression: 'laugh'
        },
        {
            title: "Jempol Lincah 👍",
            message: "Eh, jempolmu lincah banget scrolling-nya! Jangan lupa peregangan jari ya biar nggak kram.",
            expression: 'happy'
        },
        {
            title: "Cloud File Manager Keren ☁️",
            message: "Di Web Apps Studio ada Cloud File Manager beneran lho! Bisa buka folder, dengerin synthesizer suara, dan ganti view mobile.",
            expression: 'surprised'
        },
        {
            title: "Geli-Geli Empuk 🤭",
            message: "Aku tuh kalau kena kursor atau jari sentuh geli-geli empuk gimanaaa gitu... coba colek aku lagi deh!",
            expression: 'laugh'
        },
        {
            title: "Pengen Tinggi 🐾",
            message: "Kadang aku suka jalan-jalan ke atas layar biar kelihatan lebih tinggi... tapi ya tetep bulet kenyal sih.",
            expression: 'wink'
        },
        {
            title: "Kemewahan Wallpaper Mesh 🎨",
            message: "Coba aktifkan tombol Mesh Gradient di atas! Efek refraksi kaca di wallpaper ambient mewahnya ngalahin restoran bintang lima!",
            expression: 'surprised'
        },
        {
            title: "Tombol Acak Favorit 🎲",
            message: "Tombol Randomize di atas seru banget kan? Sekali klik, 44 komponen langsung joget tukar posisi secara acak!",
            expression: 'laugh'
        },
        {
            title: "Hemat Baterai 🔋",
            message: "Tenang aja, aku nggak bakal ngabisin baterai HP kamu kok. Kodingan fisika pegasku murni Canvas 2D super ringan!",
            expression: 'happy'
        },
        {
            title: "Ingat Minum Air 💧",
            message: "Jangan lupa minum air putih ya! Ngoding boleh fokus, tapi kesehatan tetap prioritas nomor satu!",
            expression: 'happy'
        },
        {
            title: "Studio Interaktif 🔍",
            message: "Klik tombol 'Full' di kartu mana pun! Di situ kamu bisa tarik-tarik ukuran layarnya kayak karet buat tes simulator mobile!",
            expression: 'surprised'
        }
    ];

    let banterIdx = 0;
    let currentExpression = 'happy'; // 'happy', 'laugh', 'wink', 'surprised', 'ponder', 'sleepy'

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
    let isTourActive = false;

    /* --------------------------------------------------------------------------
       5. INJECT DOM ELEMENTS & GRAND INTRO OVERLAY
       -------------------------------------------------------------------------- */
    function injectCompanionUI() {
        // 1. Fullscreen First-Time Intro Overlay (Blurs entire website!)
        const introOverlay = document.createElement('div');
        introOverlay.id = 'tataIntroOverlay';
        introOverlay.className = 'tata-intro-overlay';
        introOverlay.innerHTML = `
            <div class="tata-intro-card">
                <div class="tata-intro-avatar">🐾</div>
                <div class="tata-intro-tag">✨ Kenalan Yuk!</div>
                <h3 class="tata-intro-title">Halo! Aku Tata 👋</h3>
                <p class="tata-intro-desc">
                    Mascot jelly kenyal pemandumu di <strong>Prototype</strong>! Aku bakal nemenin kamu menjelajahi 44 komponen web mandiri, ngasih tips praktis, atau sesekali jalan-jalan di layarmu. Siap eksplorasi bareng Tata?
                </p>
                <div class="tata-intro-actions">
                    <button type="button" class="btn-intro-secondary" id="btnIntroSkip">Eksplorasi Sendiri</button>
                    <button type="button" class="btn-intro-primary" id="btnIntroStart">Halo Tata, Siap! 🚀</button>
                </div>
            </div>
        `;

        // 2. Spotlight elements (Crystal clear cutout)
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

        // 3. Blob Mascot Container
        const companion = document.createElement('div');
        companion.id = 'gellyCompanionContainer';
        companion.className = 'gelly-companion-container';

        const canvas = document.createElement('canvas');
        canvas.id = 'gellyCanvas';
        canvas.className = 'gelly-canvas';
        canvas.width = 280;
        canvas.height = 280;
        canvas.title = "Hai, aku Tata! Klik aku untuk panduan atau ngobrol seru.";

        const pingDot = document.createElement('div');
        pingDot.className = 'gelly-ping-dot';
        pingDot.title = "Tips baru dari Tata!";

        companion.appendChild(canvas);
        companion.appendChild(pingDot);

        // 4. Speech Bubble Wrapper (Ultra-translucent frosted glass)
        const bubbleWrapper = document.createElement('div');
        bubbleWrapper.id = 'gellyBubbleWrapper';
        bubbleWrapper.className = 'gelly-bubble-wrapper';

        bubbleWrapper.innerHTML = `
            <div class="gelly-bubble">
                <div class="gelly-bubble-header">
                    <div class="gelly-badge">
                        <span class="gelly-badge-dot"></span>
                        <span id="gellyBadgeText">Tata ✦</span>
                        <span class="gelly-step-counter" id="gellyStepCounter"></span>
                    </div>
                    <div class="gelly-header-tools">
                        <button type="button" class="gelly-tool-btn" id="gellySoundBtn" title="Aktifkan/Matikan Suara">
                            <i data-lucide="${isMuted ? 'volume-x' : 'volume-2'}"></i>
                        </button>
                        <button type="button" class="gelly-tool-btn" id="gellyMinimizeBtn" title="Kecilkan Tata">
                            <i data-lucide="minus"></i>
                        </button>
                        <button type="button" class="gelly-tool-btn" id="gellyCloseBtn" title="Tutup">
                            <i data-lucide="x"></i>
                        </button>
                    </div>
                </div>

                <div class="gelly-bubble-content">
                    <h4 class="gelly-title" id="gellyTitle">${pageGreetings[currentPageKey].title}</h4>
                    <p class="gelly-message" id="gellyMessage">${pageGreetings[currentPageKey].message}</p>
                </div>

                <!-- Quick Topic Selector Row (Direct Action, NO redundant Basa-Basi buttons) -->
                <div class="gelly-topics-row">
                    <button type="button" class="gelly-topic-pill" data-topic="tour">
                        <i data-lucide="compass"></i> Panduan
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
                    <button type="button" class="gelly-topic-pill" data-topic="walk" title="Ajak Tata jalan-jalan">
                        <i data-lucide="footprints"></i> Ajak Jalan
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
                        Mulai Panduan 🧭
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(introOverlay);
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
       7. SPEECH BUBBLE CONTROLS & SPONTANEOUS DIALOGUES
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
        isTourActive = true;
        if (index < 0) index = 0;
        if (index >= activeTourSteps.length) {
            hideSpotlight();
            playSound('chime');
            currentStepIndex = 0;
            isTourActive = false;
            currentExpression = 'laugh';
            document.getElementById('gellyBadgeText').innerText = "Tata ✦";
            document.getElementById('gellyTitle').innerText = "Kamu Siap Bereksplorasi! 🎉";
            document.getElementById('gellyMessage').innerHTML = "Semua fitur utama sudah kamu kenali. Sentuh atau klik aku kapan saja kalau mau disapa atau ditemani jalan!";
            document.getElementById('gellyStepCounter').innerText = "";
            document.getElementById('gellyPrevBtn').style.display = 'none';
            document.getElementById('gellyHighlightBtn').style.display = 'none';
            document.getElementById('gellyNextBtn').innerHTML = `Tutup <i data-lucide="check"></i>`;
            if (window.lucide) window.lucide.createIcons();
            return;
        }

        currentStepIndex = index;
        const step = activeTourSteps[currentStepIndex];

        currentExpression = (index % 2 === 0) ? 'happy' : 'wink';
        document.getElementById('gellyBadgeText').innerText = "Panduan Tata";
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

    // Spontaneous natural banter / joke triggered by clicking Tata or idle
    function triggerSpontaneousBanter() {
        isTourActive = false;
        hideSpotlight();
        const joke = banterJokes[banterIdx % banterJokes.length];
        banterIdx++;

        currentExpression = joke.expression || 'happy';
        document.getElementById('gellyBadgeText').innerText = "Tata ✦";
        document.getElementById('gellyStepCounter').innerText = "";
        document.getElementById('gellyTitle').innerText = joke.title;
        document.getElementById('gellyMessage').innerHTML = joke.message;

        document.getElementById('gellyPrevBtn').style.display = 'none';
        document.getElementById('gellyHighlightBtn').style.display = 'none';
        document.getElementById('gellyNextBtn').innerHTML = `Mulai Panduan 🧭`;

        showBubble();
        playSound('chime');
    }

    /* --------------------------------------------------------------------------
       8. RANDOM WANDERING & JIGGLE WALKING ALONG SCREEN EDGE
       -------------------------------------------------------------------------- */
    let companionState = 'idle'; // 'idle', 'walking', 'returning'
    let walkInterval = null;
    let idleTimer = null;

    function startWanderWalk() {
        if (companionState !== 'idle' || isBubbleOpen) return;

        const container = document.getElementById('gellyCompanionContainer');
        if (!container) return;

        companionState = 'walking';
        currentExpression = 'surprised';
        container.classList.add('walking');

        // Pick random height on the right side of the screen (between 180px and 60vh)
        const randomBottom = Math.floor(180 + Math.random() * (window.innerHeight * 0.45));
        container.style.bottom = `${randomBottom}px`;
        container.style.right = `-5px`;

        playSound('squish');

        // Auto return after 14 seconds if user doesn't touch her
        clearTimeout(walkInterval);
        walkInterval = setTimeout(() => {
            if (companionState === 'walking') {
                returnToHomeCorner(false);
            }
        }, 14000);
    }

    // When clicked/tapped during walking, Tata glides back to home with playful reaction!
    function returnToHomeCorner(byClick = true) {
        const container = document.getElementById('gellyCompanionContainer');
        if (!container) return;

        clearTimeout(walkInterval);
        companionState = 'returning';
        container.classList.remove('walking');
        container.classList.add('returning');

        container.style.bottom = '-15px';
        container.style.right = '-15px';

        if (byClick) {
            currentExpression = 'wink';
            playSound('slide');
            // Friendly caught-red-handed quip!
            document.getElementById('gellyBadgeText').innerText = "Tata ✦";
            document.getElementById('gellyTitle').innerText = "Eep! Ketahuan dehh 💨";
            document.getElementById('gellyMessage').innerHTML = "Tata lagi asyik jalan-jalan ke atas layar, eh kamu pencet... langsung meluncur balik ke pos deh!";
            showBubble();
        } else {
            currentExpression = 'happy';
        }

        setTimeout(() => {
            container.classList.remove('returning');
            companionState = 'idle';
        }, 700);
    }

    function resetIdleTimer() {
        clearTimeout(idleTimer);
        // Start wandering after 24 seconds of quiet idle
        idleTimer = setTimeout(() => {
            if (companionState === 'idle' && !isBubbleOpen) {
                startWanderWalk();
            }
        }, 24000);
    }

    window.addEventListener('mousemove', resetIdleTimer, { passive: true });
    window.addEventListener('touchstart', resetIdleTimer, { passive: true });
    window.addEventListener('scroll', resetIdleTimer, { passive: true });

    function setupBubbleEvents() {
        const closeBtn = document.getElementById('gellyCloseBtn');
        const minBtn = document.getElementById('gellyMinimizeBtn');
        const soundBtn = document.getElementById('gellySoundBtn');
        const nextBtn = document.getElementById('gellyNextBtn');
        const prevBtn = document.getElementById('gellyPrevBtn');
        const hlBtn = document.getElementById('gellyHighlightBtn');

        // Intro modal buttons
        const introStart = document.getElementById('btnIntroStart');
        const introSkip = document.getElementById('btnIntroSkip');
        const introOverlay = document.getElementById('tataIntroOverlay');

        function dismissIntro() {
            if (introOverlay) {
                introOverlay.classList.remove('active');
                localStorage.setItem('tata_intro_seen_v3', 'true');
                playSound('chime');
                // Tata greets at home base
                setTimeout(() => {
                    showBubble();
                }, 400);
            }
        }

        if (introStart) introStart.onclick = dismissIntro;
        if (introSkip) introSkip.onclick = dismissIntro;

        if (closeBtn) closeBtn.onclick = () => hideBubble();
        
        // Minimize: Tata doesn't disappear! Eyes keep peeking gently
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
                localStorage.setItem('tata_sound_muted', isMuted ? 'true' : 'false');
                soundBtn.innerHTML = `<i data-lucide="${isMuted ? 'volume-x' : 'volume-2'}"></i>`;
                if (window.lucide) window.lucide.createIcons();
                if (!isMuted) playSound('pop');
            };
        }

        if (nextBtn) {
            nextBtn.onclick = () => {
                if (nextBtn.innerText.includes('Mulai Panduan')) {
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
                } else if (topic === 'grid') {
                    isTourActive = false;
                    document.getElementById('gellyBadgeText').innerText = "Tata ✦ Grid";
                    document.getElementById('gellyTitle').innerText = "Grid 44 Komponen Kaca";
                    document.getElementById('gellyMessage').innerHTML = "Ini dia grid showroom lengkap yang menampung 44 komponen interaktif! Kamu bisa mencoba langsung setiap komponen di dalam kartunya.";
                    highlightElement("#componentsGrid, .components-grid", "👉 Grid 44 Komponen Kaca");
                    document.getElementById('gellyNextBtn').innerHTML = `Lanjut <i data-lucide="arrow-right"></i>`;
                    playSound('pop');
                } else if (topic === 'copy') {
                    isTourActive = false;
                    document.getElementById('gellyBadgeText').innerText = "Tata ✦ Salin";
                    document.getElementById('gellyTitle').innerText = "Cara Salin Kode Mandiri";
                    document.getElementById('gellyMessage').innerHTML = "Setiap kartu memiliki tombol <strong>Salin</strong>. Begitu diklik, seluruh HTML, CSS variabel, dan JavaScript interaktif langsung tersalin ke clipboard tanpa perlu install dependency.";
                    highlightElement('.card-actions-tools, .component-card:first-of-type .card-actions-tools', "👉 Tombol Salin Instan");
                    document.getElementById('gellyNextBtn').innerHTML = `Lanjut <i data-lucide="arrow-right"></i>`;
                    playSound('pop');
                } else if (topic === 'bg') {
                    isTourActive = false;
                    document.getElementById('gellyBadgeText').innerText = "Tata ✦ Tema";
                    document.getElementById('gellyTitle').innerText = "Ganti Tema Latar Kaca";
                    document.getElementById('gellyMessage').innerHTML = "Pilih tombol <strong>Mesh Gradient</strong> pada header untuk mengaktifkan wallpaper dinamis, atau gunakan switch per kartu untuk menguji kontras.";
                    highlightElement('.grid-bg-selector', "👉 Switcher Tema Latar");
                    document.getElementById('gellyNextBtn').innerHTML = `Lanjut <i data-lucide="arrow-right"></i>`;
                    playSound('pop');
                } else if (topic === 'walk') {
                    hideBubble();
                    startWanderWalk();
                } else if (topic === 'apps') {
                    window.location.href = isGlassShowcase ? '../../apps.html' : 'ui/web/apps.html';
                } else if (topic === 'glass') {
                    window.location.href = isWebApps ? 'components/glass/showcase.html' : 'ui/web/components/glass/showcase.html';
                }
            };
        });
    }

    /* --------------------------------------------------------------------------
       9. FERALUI-INSPIRED SOFT-BODY SPRING PHYSICS JELLY BLOB (Canvas 2D)
       -------------------------------------------------------------------------- */
    function initGellyPhysicsCanvas() {
        const canvas = document.getElementById('gellyCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const width = 280;
        const height = 280;
        const cx = 180;
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

        // Desktop Mouse Tracking
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

        // Mobile Touch Tracking (Finger tracking on touch devices!)
        function handleTouchTracking(e) {
            if (e.touches && e.touches[0]) {
                mouseScreenX = e.touches[0].clientX;
                mouseScreenY = e.touches[0].clientY;

                const rect = canvas.getBoundingClientRect();
                const canvasX = e.touches[0].clientX - rect.left;
                const canvasY = e.touches[0].clientY - rect.top;

                if (canvasX >= 0 && canvasX <= rect.width && canvasY >= 0 && canvasY <= rect.height) {
                    const touchAngle = Math.atan2(canvasY * 2 - cy, canvasX * 2 - cx);
                    points.forEach(p => {
                        const diff = Math.abs(p.angle - touchAngle);
                        if (diff < 0.7 || Math.abs(diff - Math.PI * 2) < 0.7) {
                            p.vr += 4;
                        }
                    });
                }
            }
        }

        window.addEventListener('touchstart', handleTouchTracking, { passive: true });
        window.addEventListener('touchmove', handleTouchTracking, { passive: true });

        // Click / Touch on Tata Mascot
        canvas.addEventListener('click', (e) => {
            e.stopPropagation();

            // IF TATA IS WANDERING: Play slide return back to home corner!
            if (companionState === 'walking') {
                returnToHomeCorner(true);
                return;
            }

            // Normal click reaction: Squish and spontaneous banter!
            squashX = 1.35;
            squashY = 0.72;
            squashVx = -0.2;
            squashVy = 0.2;

            points.forEach((p) => {
                p.vr += (Math.random() - 0.5) * 20;
            });

            playSound('squish');

            const container = document.getElementById('gellyCompanionContainer');
            if (container && container.classList.contains('minimized')) {
                container.classList.remove('minimized');
                showBubble();
            } else if (!isBubbleOpen) {
                // Spontaneous funny remark when clicked!
                triggerSpontaneousBanter();
            } else {
                toggleBubble();
            }
        });

        let lastTime = performance.now();

        function render(now) {
            const dt = Math.min((now - lastTime) / 1000, 0.1);
            lastTime = now;

            // Walk hop oscillation if walking
            if (companionState === 'walking') {
                squashY = 1 + Math.sin(now * 0.009) * 0.18;
                squashX = 1 - Math.sin(now * 0.009) * 0.12;
            } else {
                // Spring physics simulation for overall squish
                const springK = 75;
                const springDamp = 6.5;

                const fx = (1 - squashX) * springK - squashVx * springDamp;
                squashVx += fx * dt;
                squashX += squashVx * dt;

                const fy = (1 - squashY) * springK - squashVy * springDamp;
                squashVy += fy * dt;
                squashY += squashVy * dt;
            }

            // Point vertices radial spring simulation
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

            // Eye blinking
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

            // Page-Adaptive Gradient Colors for Tata
            const grad = ctx.createRadialGradient(cx - 35, cy - 35, 15, cx, cy, baseRadius * 1.3);
            if (isWebApps) {
                // Electric Cyan & High-tech Blue for Web Apps
                grad.addColorStop(0, '#22D3EE');
                grad.addColorStop(0.4, '#0284C7');
                grad.addColorStop(0.8, '#2563EB');
                grad.addColorStop(1, '#0F172A');
            } else if (isRawShowcase) {
                // Minimal Slate & Cool Cobalt for Raw
                grad.addColorStop(0, '#93C5FD');
                grad.addColorStop(0.4, '#3B82F6');
                grad.addColorStop(0.8, '#475569');
                grad.addColorStop(1, '#1E293B');
            } else {
                // Vibrant Cyan + Indigo + Neon Purple for Glass & Gateway
                grad.addColorStop(0, '#38BDF8');
                grad.addColorStop(0.4, '#0284C7');
                grad.addColorStop(0.8, '#4F46E5');
                grad.addColorStop(1, '#6B21A8');
            }
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

            // Eyes & Pupil tracking (Follows mouse or touch coordinates!)
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

            const maxPupilOffset = 6.5;
            const pupil1 = {
                x: eye1Center.x + Math.cos(angle1) * maxPupilOffset,
                y: eye1Center.y + Math.sin(angle1) * maxPupilOffset
            };
            const pupil2 = {
                x: eye2Center.x + Math.cos(angle2) * maxPupilOffset,
                y: eye2Center.y + Math.sin(angle2) * maxPupilOffset
            };

            const blinkFactor = isBlinking ? (1 - Math.sin(blinkProgress * Math.PI) * 0.92) : 1;

            function drawEye(center, pupil, radius, isWinkEye = false) {
                ctx.save();
                ctx.translate(center.x, center.y);
                
                // Wink expression
                if (currentExpression === 'wink' && isWinkEye) {
                    ctx.scale(1, 0.15);
                } else if (currentExpression === 'laugh') {
                    // Squinting happy eyes > <
                    ctx.scale(1, 0.25);
                } else {
                    ctx.scale(1, blinkFactor);
                }
                ctx.translate(-center.x, -center.y);

                ctx.fillStyle = '#FFFFFF';
                ctx.beginPath();
                ctx.arc(center.x, center.y, radius, 0, Math.PI * 2);
                ctx.fill();

                if (blinkFactor > 0.3 && currentExpression !== 'laugh' && !(currentExpression === 'wink' && isWinkEye)) {
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

            drawEye(eye1Center, pupil1, 15, false);
            drawEye(eye2Center, pupil2, 14, true);

            // Rich Facial Expressions (Mouth)
            ctx.save();
            ctx.strokeStyle = '#0F172A';
            ctx.fillStyle = '#0F172A';
            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            const mouthCenter = { x: cx - 22, y: cy - 14 };

            if (currentExpression === 'laugh') {
                // Wide open laughing mouth
                ctx.beginPath();
                ctx.arc(mouthCenter.x, mouthCenter.y - 2, 9, 0, Math.PI, false);
                ctx.fill();
            } else if (currentExpression === 'surprised' || companionState === 'walking') {
                // Surprised cute round mouth O
                ctx.beginPath();
                ctx.arc(mouthCenter.x, mouthCenter.y, 5, 0, Math.PI * 2);
                ctx.stroke();
            } else if (currentExpression === 'ponder') {
                // Wavy pondering mouth
                ctx.beginPath();
                ctx.moveTo(mouthCenter.x - 7, mouthCenter.y);
                ctx.quadraticCurveTo(mouthCenter.x - 3, mouthCenter.y - 3, mouthCenter.x, mouthCenter.y);
                ctx.quadraticCurveTo(mouthCenter.x + 3, mouthCenter.y + 3, mouthCenter.x + 7, mouthCenter.y);
                ctx.stroke();
            } else if (isHovered || isBubbleOpen || currentExpression === 'wink') {
                // Warm wide smile
                ctx.beginPath();
                ctx.arc(mouthCenter.x, mouthCenter.y, 8, 0.15 * Math.PI, 0.85 * Math.PI, false);
                ctx.stroke();
            } else {
                // Gentle calm smile
                ctx.beginPath();
                ctx.arc(mouthCenter.x, mouthCenter.y, 6, 0.2 * Math.PI, 0.8 * Math.PI, false);
                ctx.stroke();
            }
            ctx.restore();

            // Cheek Blush
            ctx.fillStyle = 'rgba(244, 114, 182, 0.42)';
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
       10. INITIALIZE ON PAGE LOAD WITH FIRST-TIME INTRO BLUR
       -------------------------------------------------------------------------- */
    function init() {
        injectCompanionUI();
        setupBubbleEvents();
        initGellyPhysicsCanvas();
        resetIdleTimer();

        // 1. Check if first-time visitor needs the grand introduction with website blur!
        const hasSeenIntro = localStorage.getItem('tata_intro_seen_v3');
        if (!hasSeenIntro) {
            const intro = document.getElementById('tataIntroOverlay');
            if (intro) {
                setTimeout(() => {
                    intro.classList.add('active');
                    playSound('chime');
                }, 350);
            }
        } else {
            // Check if page switched for contextual greeting
            const lastPage = sessionStorage.getItem('tata_last_page');
            const isPageSwitch = lastPage && lastPage !== currentPageKey;
            sessionStorage.setItem('tata_last_page', currentPageKey);

            if (isPageSwitch || !sessionStorage.getItem('tata_welcomed')) {
                sessionStorage.setItem('tata_welcomed', 'true');
                setTimeout(() => {
                    showBubble();
                }, 600);
            } else {
                const container = document.getElementById('gellyCompanionContainer');
                if (container) container.classList.add('has-unread');
            }
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
