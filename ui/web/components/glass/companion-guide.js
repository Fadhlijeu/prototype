/**
 * ============================================================================
 * TATA COMPANION & GLASSOS ORB HELMET RIG ENGINE
 * 
 * High-fidelity visual companion for GlassOS based on:
 * - Dimensional Glass Helmet Visor & Orb Model (SVG Rig with optical refractions)
 * - 3D Dynamic Head Facing ("Nengok-Nengok": Left, Center, Right) + Mouse Follow
 * - Face Fidgets Engine (Tingkah Raut Muka: Manyun, Lirik, Derp, Siul, Wink, Smirk, Alis Joget)
 * - 10 Expressive Moods (Vector Eyelid Clipping, Eyebrows, Mouth Paths, Blush)
 * - Thinking & Yapping Engine ("mikir..." anticipation + mouth flapping sync)
 * - Autonomous Life Engine (Double-blinking, Micro-parallax, Gaze wandering)
 * - Full Project Integration:
 *   * Centered first-time interactive intro
 *   * Slow multi-directional free wandering across edges (no checkpoints)
 *   * Post-guidance quick options menu on click (never auto-restarts tour)
 *   * Multi-page context adaptation (Showcase, Web Apps, Gateway, Raw)
 *   * Continuous 3D Kinematics & Eye Tracking Engine
 * ============================================================================
 */

(function () {
  'use strict';

  if (window.__TATA_COMPANION_INITIALIZED__) return;
  window.__TATA_COMPANION_INITIALIZED__ = true;

  /* --------------------------------------------------------------------------
     1. SOUND SYNTHESIS
     -------------------------------------------------------------------------- */
  let isMuted = localStorage.getItem('tata_sound_muted') === 'true';
  let audioCtx = null;

  function getAudioContext() {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) audioCtx = new AudioContextClass();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  function playSound(type) {
    if (isMuted) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      if (type === 'chime') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(587.33, now); // D5
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.1); // A5
        osc.frequency.exponentialRampToValueAtTime(1174.66, now + 0.22); // D6
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
        osc.start(now);
        osc.stop(now + 0.4);
      } else if (type === 'pop') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.08);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
        osc.start(now);
        osc.stop(now + 0.1);
      } else if (type === 'squish') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(320, now);
        osc.frequency.exponentialRampToValueAtTime(170, now + 0.14);
        gain.gain.setValueAtTime(0.14, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
        osc.start(now);
        osc.stop(now + 0.16);
      } else if (type === 'slide') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(650, now);
        osc.frequency.exponentialRampToValueAtTime(220, now + 0.3);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
        osc.start(now);
        osc.stop(now + 0.35);
      } else if (type === 'sad') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(420, now);
        osc.frequency.exponentialRampToValueAtTime(260, now + 0.28);
        gain.gain.setValueAtTime(0.14, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        osc.start(now);
        osc.stop(now + 0.32);
      }
    } catch (e) {}
  }

  /* --------------------------------------------------------------------------
     2. PAGE IDENTIFICATION & CONTEXTUAL ADAPTATION
     -------------------------------------------------------------------------- */
  const path = window.location.pathname.toLowerCase();
  const isGlassShowcase = path.includes('glass/showcase.html') || (path.includes('showcase.html') && !path.includes('raw'));
  const isRawShowcase = path.includes('raw/showcase.html') || (path.includes('raw') && path.includes('showcase'));
  const isWebApps = path.includes('apps.html') || path.includes('web-apps');
  const isGateway = !isGlassShowcase && !isRawShowcase && !isWebApps;

  let currentPageKey = 'gateway';
  if (isGlassShowcase) currentPageKey = 'glass';
  else if (isWebApps) currentPageKey = 'webapps';
  else if (isRawShowcase) currentPageKey = 'raw';

  document.body.classList.add(`page-theme-${currentPageKey}`);

  /* --------------------------------------------------------------------------
     3. CONTEXTUAL SCRIPTS & YAPPINGS
     -------------------------------------------------------------------------- */
  const COMPANION_SCRIPTS = [
    { expr: 'curious', text: "Hmm... helm kaca ini kedap suara, tapi kok aku tetep bisa denger klik mouse kamu ya?" },
    { expr: 'embarrassed', text: "Ups! Tadi reflek mau bersin... untung kacanya nggak langsung berembun!" },
    { expr: 'happy', text: "Melayang di antarmuka ini rasanya kayak berenang di sirup blueberry kosmik. Cozy!" },
    { expr: 'confused', text: "Kursor kamu lincah amat hari ini. Mau ke mana sih? Ngejar deadline?" },
    { expr: 'sleepy', text: "Hoammm... kalau aku merem 3 detik aja, jangan kira offline ya. Cuma defrag bentar..." },
    { expr: 'excited', text: "Tahukah kamu? Di Neptunus hujannya berlian beneran. Helmku nggak tahan dibentur berlian sih." },
    { expr: 'happy', text: "Gurita punya tiga jantung dan darahnya warna biru. Mirip aku, birunya dapet!" },
    { expr: 'surprised', text: "Satu hari di Venus itu lebih lama daripada satu tahunnya sendiri! Pusing nggak tuh?" },
    ...(isGlassShowcase ? [
      { expr: 'excited', text: "Semua 44 kartu glass di sini 100% standalone—tanpa npm ataupun node_modules!" },
      { expr: 'curious', text: "Coba klik switcher Wallpaper Mesh di bagian atas, refraksi kacanya makin ciamik!" },
      { expr: 'happy', text: "Tombol 'Salin' di tiap kartu langsung ngasih kode HTML + CSS murni siap pakai." }
    ] : []),
    ...(isWebApps ? [
      { expr: 'excited', text: "Ini kumpulan aplikasi web utuh yang jalan live langsung di browsermu!" },
      { expr: 'curious', text: "Kamu bisa uji tampilan Mobile, Tablet, dan Desktop lewat tombol viewport atas!" }
    ] : []),
    ...(isGateway ? [
      { expr: 'happy', text: "Selamat datang di Portal Workbench! Pilih antara Web Apps, Glass UI, atau Raw HTML." },
      { expr: 'curious', text: "Jangan lupa intip Kamus Taksonomi dengan 120+ elemen web universal yang diaudit!" }
    ] : [])
  ];

  const TALK_MOUTH_FRAMES = [
    'M 98 120 Q 104 125 111 121',
    'M 101 118 C 98 118 98 128 101 128 C 107 128 107 118 101 118 Z',
    'M 96 122 Q 104 130 113 122',
    'M 99 123 L 110 123'
  ];

  /* --------------------------------------------------------------------------
     4. CONCISE TOUR CONFIGURATIONS
     -------------------------------------------------------------------------- */
  const isMobileDevice = window.innerWidth <= 680;

  const showcaseTour = [
    {
      title: "Filter Kategori",
      message: "Filter kartu komponen: Buttons, Cards, Inputs, dsb.",
      selector: "#filterTabs, .filter-tabs",
      pointerText: "👉 Kategori"
    },
    ...(!isMobileDevice ? [{
      title: "Kolom Grid",
      message: "Pilih susunan 1, 2, 3, 4 kolom atau tata letak Auto.",
      selector: ".layout-selector, .controls-right",
      pointerText: "👉 Kolom"
    }] : []),
    {
      title: "44 Kartu Glass",
      message: "Seluruh 44 komponen kaca gelap interaktif berada di sini!",
      selector: "#componentsGrid, .components-grid",
      pointerText: "👉 44 Kartu"
    },
    {
      title: "Wallpaper Kaca",
      message: "Ganti antara latar Hitam Pekat dan Mesh Berwarna.",
      selector: ".grid-bg-selector",
      pointerText: "👉 Wallpaper"
    },
    {
      title: "Salin Kode Instan",
      message: "Klik Salin pada kartu mana pun untuk mengambil kodenya!",
      selector: ".card-actions-tools, .component-card:first-of-type .card-actions-tools",
      pointerText: "👉 Salin Kode"
    },
    {
      title: "Sandbox Penuh",
      message: "Klik Full untuk membuka sandbox simulator perangkat.",
      selector: ".btn-card-full, .component-card:first-of-type .btn-card-full",
      pointerText: "👉 Sandbox"
    }
  ];

  const gatewayTour = [
    {
      title: "Aplikasi Web",
      message: "Aplikasi produksi lengkap yang berjalan secara simulasi.",
      selector: ".hub-card[href*='apps.html'], .hub-grid a:first-child",
      pointerText: "👉 Web Apps"
    },
    {
      title: "Glass Showcase",
      message: "44 kartu antarmuka Glass Dark Premium siap salin.",
      selector: ".hub-card[href*='showcase.html'], .hub-grid a:nth-child(2)",
      pointerText: "👉 Glass Cards"
    },
    {
      title: "Raw HTML5",
      message: "Katalog elemen semantik HTML asli tanpa styling bawaan.",
      selector: ".hub-card[href*='raw/showcase.html'], .hub-grid a:nth-child(3)",
      pointerText: "👉 Raw HTML"
    }
  ];

  const webappsTour = [
    {
      title: "Simulator Langsung",
      message: "Jalankan dan uji aplikasi web langsung di viewport ini.",
      selector: "#stageSection, .app-showcase-box",
      pointerText: "👉 Live App"
    },
    {
      title: "Pengalih Layar",
      message: "Uji ukuran layar Mobile, Tablet, dan Desktop secara responsif.",
      selector: ".viewport-buttons, .mode-toggle-cluster",
      pointerText: "👉 Viewport"
    },
    {
      title: "Pilih Aplikasi",
      message: "Beralih antara Cloud Resource Manager dan AI Prompt Studio.",
      selector: ".project-tabs-cluster, .projects-selection-bar",
      pointerText: "👉 Pilih App"
    }
  ];

  const rawTour = [
    {
      title: "Kontrol Asli",
      message: "Elemen semantik browser bawaan untuk referensi struktur.",
      selector: ".raw-grid, .components-grid",
      pointerText: "👉 Kontrol Murni"
    },
    {
      title: "Navigasi",
      message: "Kembali ke Glass Showcase atau Master Workbench.",
      selector: ".header-actions",
      pointerText: "👉 Navigasi"
    }
  ];

  let activeTourSteps = showcaseTour;
  if (isWebApps) activeTourSteps = webappsTour;
  else if (isRawShowcase) activeTourSteps = rawTour;
  else if (isGateway) activeTourSteps = gatewayTour;

  let currentStepIndex = 0;
  let isTourActive = false;
  let isBubbleOpen = false;
  let autoAdvanceTimer = null;
  let typewriterTimer = null;
  let userDismissedBubbleAt = 0;

  /* --------------------------------------------------------------------------
     5. 10-STATE MOOD EXPRESSIONS CONFIGURATION
     -------------------------------------------------------------------------- */
  const EXPRESSIONS = {
    neutral: {
      posture: { y: 0, rot: 0, scaleY: 1 },
      mouth: { d: 'M 97 122 Q 104 128 112 123', stroke: '#0a1128', fill: 'none', width: 4.5 },
      brows: { show: false, l: 'M 68 64 Q 78 61 88 65', r: 'M 118 53 Q 128 50 138 54' },
      eyelids: {
        topL: 'M 52 64 H 106 V 67 Q 79 67 52 67 Z',
        botL: 'M 52 118 H 106 V 115 Q 79 115 52 115 Z',
        topR: 'M 102 52 H 152 V 55 Q 127 55 102 55 Z',
        botR: 'M 102 106 H 152 V 103 Q 127 103 102 103 Z'
      },
      pupils: { baseLX: 84, baseLY: 86, baseRX: 132, baseRY: 74, scale: 1 },
      blush: 0.65
    },
    happy: {
      posture: { y: -5, rot: 2.5, scaleY: 1.02 },
      mouth: { d: 'M 95 119 Q 104 133 115 120', stroke: '#0a1128', fill: 'none', width: 4.8 },
      brows: { show: true, l: 'M 68 60 Q 78 57 88 61', r: 'M 118 49 Q 128 46 138 50' },
      eyelids: {
        topL: 'M 52 64 H 106 V 67 Q 79 67 52 67 Z',
        botL: 'M 52 118 H 106 V 98 Q 79 94 52 98 Z',
        topR: 'M 102 52 H 152 V 55 Q 127 55 102 55 Z',
        botR: 'M 102 106 H 152 V 86 Q 127 82 102 86 Z'
      },
      pupils: { baseLX: 84, baseLY: 84, baseRX: 132, baseRY: 72, scale: 1.05 },
      blush: 0.88
    },
    excited: {
      posture: { y: -8, rot: -1.5, scaleY: 1.04 },
      mouth: { d: 'M 94 117 Q 104 137 116 117 Q 104 121 94 117 Z', stroke: '#0a1128', fill: '#0a1128', width: 2 },
      brows: { show: true, l: 'M 68 56 Q 78 51 88 57', r: 'M 118 45 Q 128 40 138 46' },
      eyelids: {
        topL: 'M 52 64 H 106 V 65 Q 79 65 52 65 Z',
        botL: 'M 52 118 H 106 V 104 Q 79 101 52 104 Z',
        topR: 'M 102 52 H 152 V 53 Q 127 53 102 53 Z',
        botR: 'M 102 106 H 152 V 92 Q 127 89 102 92 Z'
      },
      pupils: { baseLX: 84, baseLY: 83, baseRX: 132, baseRY: 71, scale: 1.15 },
      blush: 0.95
    },
    curious: {
      posture: { y: -3, rot: 8.5, scaleY: 1.01 },
      mouth: { d: 'M 98 122 Q 106 128 113 121', stroke: '#0a1128', fill: 'none', width: 4.2 },
      brows: { show: true, l: 'M 68 58 Q 78 52 88 59', r: 'M 118 55 Q 128 54 138 56' },
      eyelids: {
        topL: 'M 52 64 H 106 V 67 Q 79 67 52 67 Z',
        botL: 'M 52 118 H 106 V 115 Q 79 115 52 115 Z',
        topR: 'M 102 52 H 152 V 62 Q 127 62 102 62 Z',
        botR: 'M 102 106 H 152 V 100 Q 127 100 102 100 Z'
      },
      pupils: { baseLX: 85, baseLY: 82, baseRX: 133, baseRY: 70, scale: 1.05 },
      blush: 0.5
    },
    confused: {
      posture: { y: 2, rot: -7.5, scaleY: 0.98 },
      mouth: { d: 'M 97 124 Q 102 119 106 123 T 114 121', stroke: '#0a1128', fill: 'none', width: 4.2 },
      brows: { show: true, l: 'M 68 66 Q 78 64 88 61', r: 'M 118 49 Q 128 53 138 56' },
      eyelids: {
        topL: 'M 52 64 H 106 V 76 Q 79 76 52 76 Z',
        botL: 'M 52 118 H 106 V 112 Q 79 112 52 112 Z',
        topR: 'M 102 52 H 152 V 57 Q 127 57 102 57 Z',
        botR: 'M 102 106 H 152 V 103 Q 127 103 102 103 Z'
      },
      pupils: { baseLX: 82, baseLY: 89, baseRX: 130, baseRY: 77, scale: 0.95 },
      blush: 0.35
    },
    surprised: {
      posture: { y: -10, rot: 0, scaleY: 1.06 },
      mouth: { d: 'M 101 117 C 98 117 98 131 101 131 C 108 131 108 117 101 117 Z', stroke: '#0a1128', fill: '#0a1128', width: 2 },
      brows: { show: true, l: 'M 68 53 Q 78 48 88 54', r: 'M 118 42 Q 128 37 138 43' },
      eyelids: {
        topL: 'M 52 64 H 106 V 64 Q 79 64 52 64 Z',
        botL: 'M 52 118 H 106 V 118 Q 79 118 52 118 Z',
        topR: 'M 102 52 H 152 V 52 Q 127 52 102 52 Z',
        botR: 'M 102 106 H 152 V 106 Q 127 106 102 106 Z'
      },
      pupils: { baseLX: 81, baseLY: 87, baseRX: 129, baseRY: 75, scale: 0.8 },
      blush: 0.3
    },
    sleepy: {
      posture: { y: 6, rot: 3, scaleY: 0.96 },
      mouth: { d: 'M 99 123 Q 104 125 109 123', stroke: '#0a1128', fill: 'none', width: 3.5 },
      brows: { show: false, l: 'M 68 64 Q 78 61 88 65', r: 'M 118 53 Q 128 50 138 54' },
      eyelids: {
        topL: 'M 52 64 H 106 V 94 Q 79 97 52 94 Z',
        botL: 'M 52 118 H 106 V 110 Q 79 110 52 110 Z',
        topR: 'M 102 52 H 152 V 82 Q 127 85 102 82 Z',
        botR: 'M 102 106 H 152 V 98 Q 127 98 102 98 Z'
      },
      pupils: { baseLX: 81, baseLY: 93, baseRX: 129, baseRY: 81, scale: 0.88 },
      blush: 0.45
    },
    sad: {
      posture: { y: 5, rot: -2, scaleY: 0.97 },
      mouth: { d: 'M 97 127 Q 104 120 111 127', stroke: '#0a1128', fill: 'none', width: 4.2 },
      brows: { show: true, l: 'M 68 61 Q 78 64 88 67', r: 'M 118 50 Q 128 53 138 56' },
      eyelids: {
        topL: 'M 52 64 H 106 V 82 Q 79 80 52 86 Z',
        botL: 'M 52 118 H 106 V 114 Q 79 114 52 114 Z',
        topR: 'M 102 52 H 152 V 70 Q 127 68 102 74 Z',
        botR: 'M 102 106 H 152 V 102 Q 127 102 102 102 Z'
      },
      pupils: { baseLX: 80, baseLY: 92, baseRX: 128, baseRY: 80, scale: 0.95 },
      blush: 0.25
    },
    annoyed: {
      posture: { y: 1, rot: -4.5, scaleY: 0.99 },
      mouth: { d: 'M 98 123 L 111 120', stroke: '#0a1128', fill: 'none', width: 4.5 },
      brows: { show: true, l: 'M 68 67 Q 78 63 88 60', r: 'M 118 56 Q 128 52 138 49' },
      eyelids: {
        topL: 'M 52 64 H 106 V 83 Q 79 83 52 83 Z',
        botL: 'M 52 118 H 106 V 107 Q 79 107 52 107 Z',
        topR: 'M 102 52 H 152 V 71 Q 127 71 102 71 Z',
        botR: 'M 102 106 H 152 V 95 Q 127 95 102 95 Z'
      },
      pupils: { baseLX: 80, baseLY: 87, baseRX: 128, baseRY: 75, scale: 0.9 },
      blush: 0.2
    },
    embarrassed: {
      posture: { y: 3, rot: 7, scaleY: 0.98 },
      mouth: { d: 'M 98 123 Q 102 126 105 123 T 112 123', stroke: '#0a1128', fill: 'none', width: 3.8 },
      brows: { show: true, l: 'M 68 62 Q 78 63 88 65', r: 'M 118 51 Q 128 52 138 54' },
      eyelids: {
        topL: 'M 52 64 H 106 V 78 Q 79 78 52 78 Z',
        botL: 'M 52 118 H 106 V 105 Q 79 105 52 105 Z',
        topR: 'M 102 52 H 152 V 66 Q 127 66 102 66 Z',
        botR: 'M 102 106 H 152 V 93 Q 127 93 102 93 Z'
      },
      pupils: { baseLX: 79, baseLY: 90, baseRX: 127, baseRY: 78, scale: 0.92 },
      blush: 1.0
    }
  };

  /* --------------------------------------------------------------------------
     6. DOM INJECTION (SVG Rig + Dialogue Bubble + Inspector Suite)
     -------------------------------------------------------------------------- */
  function injectCompanionUI() {
    // 1. Fullscreen Intro Backdrop
    const introBackdrop = document.createElement('div');
    introBackdrop.id = 'tataIntroBackdrop';
    introBackdrop.className = 'tata-intro-backdrop';
    introBackdrop.innerHTML = `<div class="tata-intro-aura"></div>`;

    // 2. Spotlight Elements
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
    badge.innerHTML = `<i data-lucide="sparkles"></i> <span id="gellyPointerText">Lihat di sini</span>`;

    // 3. Companion Mascot Container & SVG Rig from .deleteafterdone.html
    const companion = document.createElement('div');
    companion.id = 'gellyCompanionContainer';
    companion.className = 'gelly-companion-container dock-right';

    // Page-adaptive base sphere gradient
    let gradStop0 = '#38bdf8';
    let gradStop28 = '#0284c7';
    let gradStop68 = '#2563eb';
    let gradStop92 = '#3b28cc';
    let gradStop100 = '#221875';

    if (isWebApps) {
      gradStop0 = '#22d3ee';
      gradStop28 = '#0284c7';
      gradStop68 = '#1d4ed8';
      gradStop92 = '#1e3a8a';
      gradStop100 = '#0f172a';
    } else if (isGateway) {
      gradStop0 = '#818cf8';
      gradStop28 = '#6366f1';
      gradStop68 = '#4338ca';
      gradStop92 = '#312e81';
      gradStop100 = '#0f172a';
    } else if (isRawShowcase) {
      gradStop0 = '#93c5fd';
      gradStop28 = '#3b82f6';
      gradStop68 = '#475569';
      gradStop92 = '#334155';
      gradStop100 = '#1e293b';
    }

    companion.innerHTML = `
      <div class="companion-chamber" id="chamber">
        <div class="shadow-pedestal">
          <div class="shadow-primary" id="shadowPrimary"></div>
          <div class="shadow-contact" id="shadowContact"></div>
        </div>

        <div class="companion-root" id="companionRoot">
          <div class="companion-float-harness" id="floatHarness">
            <div class="companion-body-mesh" id="bodyMesh">
              <svg class="companion-svg-rig" viewBox="0 0 260 260">
                <defs>
                  <radialGradient id="orbSphereGrad" cx="38%" cy="32%" r="68%">
                    <stop offset="0%" stop-color="${gradStop0}" />
                    <stop offset="28%" stop-color="${gradStop28}" />
                    <stop offset="68%" stop-color="${gradStop68}" />
                    <stop offset="92%" stop-color="${gradStop92}" />
                    <stop offset="100%" stop-color="${gradStop100}" />
                  </radialGradient>

                  <linearGradient id="orbRimGrad" x1="15%" y1="10%" x2="85%" y2="90%">
                    <stop offset="0%" stop-color="rgba(255, 255, 255, 0.48)" />
                    <stop offset="35%" stop-color="rgba(56, 189, 248, 0.18)" />
                    <stop offset="100%" stop-color="rgba(0, 0, 0, 0.4)" />
                  </linearGradient>

                  <radialGradient id="helmetGlassGrad" cx="32%" cy="28%" r="70%">
                    <stop offset="0%" stop-color="rgba(255, 255, 255, 0.32)" />
                    <stop offset="35%" stop-color="rgba(255, 255, 255, 0.1)" />
                    <stop offset="85%" stop-color="rgba(255, 255, 255, 0)" />
                  </radialGradient>

                  <radialGradient id="blushGradient" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#d946ef" stop-opacity="0.75" />
                    <stop offset="70%" stop-color="#c084fc" stop-opacity="0.35" />
                    <stop offset="100%" stop-color="#c084fc" stop-opacity="0" />
                  </radialGradient>

                  <clipPath id="leftScleraClip">
                    <ellipse id="clipShapeL" cx="79" cy="91" rx="19" ry="21" transform="rotate(-6 79 91)" />
                  </clipPath>
                  <clipPath id="rightScleraClip">
                    <ellipse id="clipShapeR" cx="127" cy="79" rx="18" ry="20" transform="rotate(8 127 79)" />
                  </clipPath>

                  <filter id="eyeShadowFilter" x="-10%" y="-10%" width="120%" height="120%">
                    <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="#024282" flood-opacity="0.4" />
                  </filter>
                </defs>

                <!-- BASE ORB SPHERE -->
                <circle cx="130" cy="130" r="118" fill="url(#orbSphereGrad)" />
                <circle cx="130" cy="130" r="117" fill="none" stroke="url(#orbRimGrad)" stroke-width="2" />

                <!-- DYNAMIC HEAD COMPLEX (Kinematic 3D Rig) -->
                <g class="head-complex" id="headComplex">
                  <!-- GLASS HELMET VISOR BUBBLE -->
                  <g class="glass-helmet" id="glassHelmet">
                    <circle cx="98" cy="98" r="74" fill="url(#helmetGlassGrad)" stroke="rgba(255, 255, 255, 0.58)" stroke-width="2.6" />
                    <circle cx="98" cy="98" r="72" fill="none" stroke="rgba(255, 255, 255, 0.16)" stroke-width="1.2" />
                    <path d="M 52 74 C 62 48, 88 36, 114 38 C 94 44, 72 58, 62 82 Z" fill="rgba(255, 255, 255, 0.55)" opacity="0.8" />
                    <ellipse cx="64" cy="62" rx="7" ry="12" transform="rotate(-36 64 62)" fill="rgba(255, 255, 255, 0.65)" />
                  </g>

                  <!-- FACIAL RIG -->
                  <g class="face-anchor" id="faceAnchor" transform="translate(0, 0)">
                    <path class="eyebrow-path" id="browLeft" d="M 68 64 Q 78 61 88 65" />
                    <path class="eyebrow-path" id="browRight" d="M 118 53 Q 128 50 138 54" />

                    <!-- LEFT EYE -->
                    <g id="eyeRigLeft" filter="url(#eyeShadowFilter)">
                      <ellipse cx="79" cy="91" rx="19" ry="21" transform="rotate(-6 79 91)" fill="#ffffff" />
                      <g clip-path="url(#leftScleraClip)">
                        <g class="pupil-group" id="pupilLeft">
                          <circle id="pupilCoreL" cx="0" cy="0" r="10.8" fill="#090d16" />
                          <circle id="pupilGlintL" cx="3.2" cy="-3.4" r="3.6" fill="#ffffff" />
                        </g>
                        <path class="eyelid-path" id="eyelidTopL" d="M 52 64 H 106 V 67 Q 79 67 52 67 Z" />
                        <path class="eyelid-path" id="eyelidBottomL" d="M 52 118 H 106 V 115 Q 79 115 52 115 Z" />
                      </g>
                    </g>

                    <!-- RIGHT EYE -->
                    <g id="eyeRigRight" filter="url(#eyeShadowFilter)">
                      <ellipse cx="127" cy="79" rx="18" ry="20" transform="rotate(8 127 79)" fill="#ffffff" />
                      <g clip-path="url(#rightScleraClip)">
                        <g class="pupil-group" id="pupilRight">
                          <circle id="pupilCoreR" cx="0" cy="0" r="10.2" fill="#090d16" />
                          <circle id="pupilGlintR" cx="3.0" cy="-3.2" r="3.4" fill="#ffffff" />
                        </g>
                        <path class="eyelid-path" id="eyelidTopR" d="M 102 52 H 152 V 55 Q 127 55 102 55 Z" />
                        <path class="eyelid-path" id="eyelidBottomR" d="M 102 106 H 152 V 103 Q 127 103 102 103 Z" />
                      </g>
                    </g>

                    <!-- BLUSH PADS -->
                    <ellipse class="blush-pill" id="blushLeft" cx="60" cy="107" rx="8.5" ry="10" transform="rotate(-18 60 107)" fill="url(#blushGradient)" />
                    <ellipse class="blush-pill" id="blushRight" cx="145" cy="94" rx="8" ry="9.5" transform="rotate(12 145 94)" fill="url(#blushGradient)" />

                    <!-- MOUTH -->
                    <path class="mouth-path" id="companionMouth" d="M 97 122 Q 104 128 112 123" />
                  </g>
                </g>
              </svg>
            </div>
          </div>
        </div>
      </div>
    `;

    // 4. Dialogue Speech Bubble
    const bubbleWrapper = document.createElement('div');
    bubbleWrapper.id = 'gellyBubbleWrapper';
    bubbleWrapper.className = 'gelly-bubble-wrapper';

    bubbleWrapper.innerHTML = `
      <div class="gelly-speech-bubble" id="speechBubble">
        <div class="gelly-bubble-header">
          <span class="gelly-tour-badge" id="gellyTourBadge">
            <i data-lucide="sparkles"></i>
            <span id="gellyTourProgressText">Panduan</span>
          </span>
          <div class="gelly-header-tools">
            <button type="button" class="gelly-tool-btn" id="gellyMuteBtn" title="Bisukan Suara">
              <i data-lucide="volume-2" id="muteIcon"></i>
            </button>
            <button type="button" class="gelly-tool-btn" id="gellyMinimizeBtn" title="Kecilkan">
              <i data-lucide="minus"></i>
            </button>
            <button type="button" class="gelly-tool-btn" id="gellyCloseBtn" title="Tutup">
              <i data-lucide="x"></i>
            </button>
          </div>
        </div>

        <div class="gelly-bubble-content">
          <h4 class="gelly-title" id="gellyTitle">Hai! Aku Tata 👋</h4>
          <p class="gelly-message" id="gellyMessage">
            <span id="speechText"></span>
            <span class="typing-cursor" id="typingCursor"></span>
          </p>
          <div class="tata-auto-progress" id="tataAutoProgress">
            <div class="tata-auto-progress-fill" id="tataAutoProgressFill"></div>
          </div>
          <div class="tata-help-menu" id="tataHelpMenu" style="display: none;"></div>
        </div>

        <div class="gelly-actions-footer" id="gellyActionsFooter">
          <button type="button" class="gelly-btn-action primary" id="gellyMainBtn">
            Pandu saya ✨
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(introBackdrop);
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
     7. COMPANION ENGINE CORE
     -------------------------------------------------------------------------- */
  class CompanionEngine {
    constructor() {
      this.currentExprKey = 'neutral';
      this.currentFacing = 'left';

      this.isLifeActive = true;
      this.isHeadFollowActive = true;
      this.isYappingActive = true;
      this.isFaceFidgetActive = true;
      this.isRoamingActive = true;

      // Coordinates & Physics
      this.mousePos = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
      this.headShift = { x: 0, y: 0, rot: 0 };
      this.gazeTarget = { x: 0, y: 0 };
      this.gazeCurrent = { x: 0, y: 0 };
      this.fidgetEyeL = { x: 0, y: 0 };
      this.fidgetEyeR = { x: 0, y: 0 };

      // Timers
      this.blinkTimeout = null;
      this.gazeWanderTimeout = null;
      this.yapTimer = null;
      this.fidgetTimer = null;
      this.headWanderTimer = null;
      this.typewriterInterval = null;
      this.mouthFlapInterval = null;
      this.roamTimer = null;

      // States
      this.isBlinking = false;
      this.isSpeaking = false;
      this.isThinking = false;
      this.isFidgeting = false;
      this.isDragging = false;
      this.companionState = 'idle'; // 'idle', 'walking', 'intro', 'dragging'

      this.dom = {};
    }

    init() {
      this.cacheDom();
      this.setFacing('left');
      this.applyExpression('neutral');
      this.attachEventListeners();
      this.scheduleNextBlink();
      this.scheduleNextGazeWander();
      this.scheduleNextFaceFidget();
      this.scheduleNextHeadWander();
      this.startPhysicsRenderLoop();

      // First-time centered intro check (Bumped to v8)
      const hasSeenIntro = localStorage.getItem('tata_site_introduced_v8');
      if (!hasSeenIntro || window.location.search.includes('reset=1') || window.location.search.includes('intro=1')) {
        setTimeout(() => {
          this.triggerCenteredIntro();
        }, 400);
      } else {
        setTimeout(() => {
          this.resumeRoaming();
          this.scheduleNextYap(28000);
        }, 1800);
      }
    }

    cacheDom() {
      this.dom = {
        container: document.getElementById('gellyCompanionContainer'),
        chamber: document.getElementById('chamber'),
        root: document.getElementById('companionRoot'),
        bodyMesh: document.getElementById('bodyMesh'),
        shadowPrimary: document.getElementById('shadowPrimary'),
        headComplex: document.getElementById('headComplex'),
        faceAnchor: document.getElementById('faceAnchor'),
        glassHelmet: document.getElementById('glassHelmet'),
        browLeft: document.getElementById('browLeft'),
        browRight: document.getElementById('browRight'),
        pupilLeft: document.getElementById('pupilLeft'),
        pupilRight: document.getElementById('pupilRight'),
        eyelidTopL: document.getElementById('eyelidTopL'),
        eyelidBottomL: document.getElementById('eyelidBottomL'),
        eyelidTopR: document.getElementById('eyelidTopR'),
        eyelidBottomR: document.getElementById('eyelidBottomR'),
        mouth: document.getElementById('companionMouth'),
        blushL: document.getElementById('blushLeft'),
        blushR: document.getElementById('blushRight'),
        bubbleWrapper: document.getElementById('gellyBubbleWrapper'),
        speechBubble: document.getElementById('speechBubble'),
        speechText: document.getElementById('speechText'),
        typingCursor: document.getElementById('typingCursor'),
        title: document.getElementById('gellyTitle'),
        progressText: document.getElementById('gellyTourProgressText'),
        autoProgress: document.getElementById('tataAutoProgress'),
        autoProgressFill: document.getElementById('tataAutoProgressFill'),
        helpMenu: document.getElementById('tataHelpMenu'),
        actionsFooter: document.getElementById('gellyActionsFooter'),
        mainBtn: document.getElementById('gellyMainBtn'),
        introBackdrop: document.getElementById('tataIntroBackdrop')
      };
    }

    /* ------------------------------------------------------------------------
       DYNAMIC HEAD FACING (NENGOK-NENGOK RIG)
       ------------------------------------------------------------------------ */
    setFacing(direction) {
      if (!['left', 'center', 'right'].includes(direction)) return;

      if (this.dom && this.dom.container) {
        const rect = this.dom.container.getBoundingClientRect();
        const screenMid = window.innerWidth * 0.5;
        const tataCenterX = rect.left + rect.width / 2;
        const isDockRight = this.dom.container.classList.contains('dock-right');
        const isDockLeft = this.dom.container.classList.contains('dock-left');
        const isRight = isDockRight || (tataCenterX >= screenMid);
        const isLeft = isDockLeft || (tataCenterX < screenMid);

        if (isRight && direction === 'right') {
          direction = 'center';
        } else if (isLeft && direction === 'left') {
          direction = 'center';
        }
      }

      this.currentFacing = direction;
    }

    scheduleNextHeadWander() {
      clearTimeout(this.headWanderTimer);
      if (!this.isHeadFollowActive) return;

      const delay = 8000 + Math.random() * 6000;
      this.headWanderTimer = setTimeout(() => {
        if (!this.isSpeaking && !this.isThinking && this.companionState === 'idle') {
          let choices = ['left', 'center'];
          if (this.dom && this.dom.container) {
            const rect = this.dom.container.getBoundingClientRect();
            const tataCenterX = rect.left + rect.width / 2;
            if (tataCenterX < window.innerWidth * 0.5) {
              choices = ['right', 'center'];
            }
          }
          const chosen = choices[Math.floor(Math.random() * choices.length)];
          this.setFacing(chosen);
        }
        this.scheduleNextHeadWander();
      }, delay);
    }

    /* ------------------------------------------------------------------------
       MOOD EXPRESSION ENGINE
       ------------------------------------------------------------------------ */
    applyExpression(key) {
      const cfg = EXPRESSIONS[key];
      if (!cfg) return;
      this.currentExprKey = key;

      if (!this.isFidgeting) {
        this.fidgetEyeL = { x: 0, y: 0 };
        this.fidgetEyeR = { x: 0, y: 0 };
      }

      this.dom.root.style.transform = `
        translateY(${cfg.posture.y}px) 
        rotate(${cfg.posture.rot}deg) 
        scaleY(${cfg.posture.scaleY})
      `;

      this.dom.browLeft.setAttribute('d', cfg.brows.l);
      this.dom.browRight.setAttribute('d', cfg.brows.r);
      this.dom.browLeft.style.opacity = cfg.brows.show ? '1' : '0';
      this.dom.browRight.style.opacity = cfg.brows.show ? '1' : '0';

      if (!this.isBlinking) {
        this.dom.eyelidTopL.setAttribute('d', cfg.eyelids.topL);
        this.dom.eyelidBottomL.setAttribute('d', cfg.eyelids.botL);
        this.dom.eyelidTopR.setAttribute('d', cfg.eyelids.topR);
        this.dom.eyelidBottomR.setAttribute('d', cfg.eyelids.botR);
      }

      if (!this.isSpeaking && !this.isFidgeting) {
        this.dom.mouth.setAttribute('d', cfg.mouth.d);
        this.dom.mouth.setAttribute('fill', cfg.mouth.fill);
        this.dom.mouth.setAttribute('stroke', cfg.mouth.stroke);
        this.dom.mouth.style.strokeWidth = cfg.mouth.width;
      }

      this.dom.blushL.style.opacity = cfg.blush;
      this.dom.blushR.style.opacity = cfg.blush;

      this.dom.exprButtons.forEach(btn => {
        btn.classList.toggle('is-active', btn.dataset.expr === key);
      });
    }

    /* ------------------------------------------------------------------------
       FACE FIDGETS ENGINE (TINGKAH RAUT MUKA SAAT DIAM)
       ------------------------------------------------------------------------ */
    triggerFaceFidget(type) {
      if (this.isSpeaking || this.isThinking) return;
      this.isFidgeting = true;

      switch (type) {
        case 'manyun_kiri':
          this.dom.mouth.setAttribute('d', 'M 93 122 Q 97 117 103 121');
          this.dom.mouth.style.strokeWidth = '5';
          this.dom.root.style.transform = 'rotate(-6deg) translateY(-2px)';
          this.dom.blushL.style.transform = 'translate(-3px, -2px) scale(1.15)';
          this.fidgetEyeL = { x: -4, y: 1 };
          this.fidgetEyeR = { x: -4, y: 0 };
          break;

        case 'manyun_kanan':
          this.dom.mouth.setAttribute('d', 'M 106 121 Q 112 117 117 122');
          this.dom.mouth.style.strokeWidth = '5';
          this.dom.root.style.transform = 'rotate(6deg) translateY(-2px)';
          this.dom.blushR.style.transform = 'translate(3px, -2px) scale(1.15)';
          this.fidgetEyeL = { x: 4, y: 0 };
          this.fidgetEyeR = { x: 4, y: 1 };
          break;

        case 'shifty_eyes':
          this.dom.browLeft.style.opacity = '1';
          this.dom.browRight.style.opacity = '1';
          this.dom.mouth.setAttribute('d', 'M 98 124 L 110 122');
          this.fidgetEyeL = { x: 7, y: -2 };
          this.fidgetEyeR = { x: 7, y: -2 };
          setTimeout(() => {
            if (this.isFidgeting) {
              this.fidgetEyeL = { x: -7, y: 2 };
              this.fidgetEyeR = { x: -7, y: 2 };
              this.dom.root.style.transform = 'rotate(4deg)';
            }
          }, 600);
          break;

        case 'derp':
          this.dom.browLeft.setAttribute('d', 'M 68 59 Q 78 64 88 61');
          this.dom.browRight.setAttribute('d', 'M 118 61 Q 128 64 138 59');
          this.dom.browLeft.style.opacity = '1';
          this.dom.browRight.style.opacity = '1';
          this.dom.mouth.setAttribute('d', 'M 95 124 Q 100 119 105 125 T 115 122');
          this.dom.mouth.style.strokeWidth = '4';
          this.fidgetEyeL = { x: 6, y: 2 };
          this.fidgetEyeR = { x: -6, y: 2 };
          this.dom.root.style.transform = 'scaleY(0.96) translateY(3px)';
          break;

        case 'whistle':
          this.dom.mouth.setAttribute('d', 'M 103 121 C 100 121 100 127 103 127 C 107 127 107 121 103 121 Z');
          this.dom.mouth.setAttribute('fill', '#0a1128');
          this.dom.mouth.style.strokeWidth = '2';
          this.dom.browLeft.style.opacity = '0';
          this.dom.browRight.style.opacity = '0';
          this.dom.root.style.transform = 'translateY(-6px) rotate(3deg)';
          this.fidgetEyeL = { x: 4, y: -7 };
          this.fidgetEyeR = { x: 4, y: -7 };
          break;

        case 'wink':
          this.dom.eyelidTopR.setAttribute('d', 'M 102 52 H 152 V 85 Q 127 85 102 85 Z');
          this.dom.eyelidBottomR.setAttribute('d', 'M 102 106 H 152 V 83 Q 127 83 102 83 Z');
          this.dom.browRight.setAttribute('d', 'M 118 56 Q 128 54 138 58');
          this.dom.browRight.style.opacity = '1';
          this.dom.browLeft.setAttribute('d', 'M 68 56 Q 78 50 88 57');
          this.dom.browLeft.style.opacity = '1';
          this.dom.mouth.setAttribute('d', 'M 96 123 Q 103 128 114 119');
          this.dom.root.style.transform = 'rotate(-5deg) translateY(-3px)';
          break;

        case 'smirk':
          this.dom.browLeft.setAttribute('d', 'M 68 57 Q 78 52 88 58');
          this.dom.browLeft.style.opacity = '1';
          this.dom.browRight.setAttribute('d', 'M 118 55 Q 128 55 138 57');
          this.dom.browRight.style.opacity = '1';
          this.dom.mouth.setAttribute('d', 'M 97 124 Q 104 126 114 118');
          this.dom.root.style.transform = 'rotate(4deg)';
          this.fidgetEyeL = { x: 3, y: -2 };
          this.fidgetEyeR = { x: 3, y: -2 };
          break;

        case 'brow_dance':
          this.dom.mouth.setAttribute('d', 'M 98 122 Q 104 126 112 123');
          this.dom.browLeft.setAttribute('d', 'M 68 54 Q 78 48 88 55');
          this.dom.browRight.setAttribute('d', 'M 118 60 Q 128 64 138 62');
          this.dom.browLeft.style.opacity = '1';
          this.dom.browRight.style.opacity = '1';
          setTimeout(() => {
            if (this.isFidgeting) {
              this.dom.browLeft.setAttribute('d', 'M 68 62 Q 78 65 88 63');
              this.dom.browRight.setAttribute('d', 'M 118 50 Q 128 45 138 52');
              this.dom.root.style.transform = 'rotate(-3deg)';
            }
          }, 450);
          break;
      }

      const holdDuration = (type === 'shifty_eyes' || type === 'brow_dance') ? 1600 : 1300;
      setTimeout(() => {
        this.isFidgeting = false;
        this.dom.blushL.style.transform = 'none';
        this.dom.blushR.style.transform = 'none';
        this.fidgetEyeL = { x: 0, y: 0 };
        this.fidgetEyeR = { x: 0, y: 0 };
        if (!this.isSpeaking && !this.isThinking) {
          this.applyExpression(this.currentExprKey);
        }
      }, holdDuration);
    }

    scheduleNextFaceFidget() {
      clearTimeout(this.fidgetTimer);
      if (!this.isFaceFidgetActive) return;

      const delay = 3500 + Math.random() * 2500;
      this.fidgetTimer = setTimeout(() => {
        if (!this.isSpeaking && !this.isThinking && !this.isFidgeting && this.companionState === 'idle') {
          const fidgets = ['manyun_kiri', 'manyun_kanan', 'shifty_eyes', 'derp', 'whistle', 'wink', 'smirk', 'brow_dance'];
          const chosen = fidgets[Math.floor(Math.random() * fidgets.length)];
          this.triggerFaceFidget(chosen);
        }
        this.scheduleNextFaceFidget();
      }, delay);
    }

    /* ------------------------------------------------------------------------
       BLINK SYSTEM
       ------------------------------------------------------------------------ */
    triggerBlink(isDouble = false) {
      if (this.isBlinking) return;
      this.isBlinking = true;

      const blinkDown = () => {
        this.dom.eyelidTopL.setAttribute('d', 'M 52 64 H 106 V 98 Q 79 98 52 98 Z');
        this.dom.eyelidBottomL.setAttribute('d', 'M 52 118 H 106 V 96 Q 79 96 52 96 Z');
        this.dom.eyelidTopR.setAttribute('d', 'M 102 52 H 152 V 86 Q 127 86 102 86 Z');
        this.dom.eyelidBottomR.setAttribute('d', 'M 102 106 H 152 V 84 Q 127 84 102 84 Z');
      };

      const blinkRestore = () => {
        const cfg = EXPRESSIONS[this.currentExprKey];
        this.dom.eyelidTopL.setAttribute('d', cfg.eyelids.topL);
        this.dom.eyelidBottomL.setAttribute('d', cfg.eyelids.botL);
        this.dom.eyelidTopR.setAttribute('d', cfg.eyelids.topR);
        this.dom.eyelidBottomR.setAttribute('d', cfg.eyelids.botR);
      };

      blinkDown();

      setTimeout(() => {
        blinkRestore();
        if (isDouble) {
          setTimeout(() => {
            blinkDown();
            setTimeout(() => {
              blinkRestore();
              this.isBlinking = false;
            }, 80);
          }, 110);
        } else {
          setTimeout(() => {
            this.isBlinking = false;
          }, 60);
        }
      }, 110);
    }

    scheduleNextBlink() {
      if (!this.isLifeActive) return;
      const delay = 3200 + Math.random() * 3800;
      this.blinkTimeout = setTimeout(() => {
        if (!this.isFidgeting) {
          const isDouble = Math.random() < 0.2;
          this.triggerBlink(isDouble);
        }
        this.scheduleNextBlink();
      }, delay);
    }

    /* ------------------------------------------------------------------------
       AUTONOMOUS EYE WANDERING
       ------------------------------------------------------------------------ */
    scheduleNextGazeWander() {
      if (!this.isLifeActive) return;
      const delay = 2600 + Math.random() * 2600;
      this.gazeWanderTimeout = setTimeout(() => {
        if (!this.isThinking && !this.isFidgeting) {
          const angle = Math.random() * Math.PI * 2;
          const distance = Math.random() * 5;
          this.gazeTarget.x = Math.cos(angle) * distance;
          this.gazeTarget.y = Math.sin(angle) * distance;
        }
        this.scheduleNextGazeWander();
      }, delay);
    }

    /* ------------------------------------------------------------------------
       THINKING & YAPPING ENGINE ("mikir..." + Mouth Flapping Sync)
       ------------------------------------------------------------------------ */
    startThinkingAndYap(forcedIndex = null) {
      if (this.isSpeaking || this.isThinking) return;

      // Respect user dismissal cooldown (45s) so Tata doesn't speak to itself after being closed
      if (forcedIndex === null && (Date.now() - userDismissedBubbleAt < 45000)) return;

      const script = (forcedIndex !== null)
        ? COMPANION_SCRIPTS[forcedIndex]
        : COMPANION_SCRIPTS[Math.floor(Math.random() * COMPANION_SCRIPTS.length)];

      this.isThinking = true;
      this.applyExpression('curious');

      this.gazeTarget.x = 2;
      this.gazeTarget.y = -5;

      this.dom.title.innerText = "Tata";
      this.dom.speechBubble.classList.add('is-thinking');
      this.dom.bubbleWrapper.classList.add('active', 'banter-mode');
      this.dom.bubbleWrapper.classList.remove('intro-centered-bubble');
      this.dom.typingCursor.classList.remove('is-hidden');
      this.dom.helpMenu.style.display = 'none';
      this.dom.autoProgress.classList.remove('active');
      this.dom.actionsFooter.style.display = 'none';

      this.dom.speechText.textContent = "mikir";
      this.updateBubblePosition();

      let thinkDots = 0;
      const thinkInterval = setInterval(() => {
        thinkDots = (thinkDots + 1) % 4;
        this.dom.speechText.textContent = "mikir" + ".".repeat(thinkDots);
      }, 260);

      setTimeout(() => {
        clearInterval(thinkInterval);
        this.isThinking = false;
        this.dom.speechBubble.classList.remove('is-thinking');
        this.executeSpeech(script);
      }, 1400);
    }

    executeSpeech(script) {
      this.isSpeaking = true;
      this.applyExpression(script.expr);
      this.dom.speechText.textContent = '';
      this.dom.typingCursor.classList.remove('is-hidden');
      this.dom.bubbleWrapper.classList.add('active');

      let mouthIndex = 0;
      this.mouthFlapInterval = setInterval(() => {
        mouthIndex = (mouthIndex + 1) % TALK_MOUTH_FRAMES.length;
        this.dom.mouth.setAttribute('d', TALK_MOUTH_FRAMES[mouthIndex]);
        this.dom.mouth.setAttribute('fill', 'none');
        this.dom.mouth.setAttribute('stroke', '#0a1128');
        this.dom.mouth.style.strokeWidth = '4.2';
      }, 115);

      let charIndex = 0;
      const text = script.text;
      const typingSpeed = 32;

      this.typewriterInterval = setInterval(() => {
        if (charIndex < text.length) {
          this.dom.speechText.textContent += text.charAt(charIndex);
          charIndex++;
        } else {
          clearInterval(this.typewriterInterval);
          clearInterval(this.mouthFlapInterval);

          const cfg = EXPRESSIONS[this.currentExprKey];
          this.dom.mouth.setAttribute('d', cfg.mouth.d);
          this.dom.mouth.setAttribute('fill', cfg.mouth.fill);
          this.dom.mouth.setAttribute('stroke', cfg.mouth.stroke);
          this.dom.mouth.style.strokeWidth = cfg.mouth.width;

          this.dom.typingCursor.classList.add('is-hidden');

          const readingDuration = Math.max(3400, text.length * 60);
          setTimeout(() => {
            this.dom.bubbleWrapper.classList.remove('active');
            this.isSpeaking = false;

            setTimeout(() => {
              if (!this.isSpeaking && !this.isThinking && !this.isFidgeting) {
                this.applyExpression('neutral');
              }
            }, 1000);

            if (this.isYappingActive) {
              this.scheduleNextYap();
            }
          }, readingDuration);
        }
      }, typingSpeed);
    }

    scheduleNextYap(customDelay = null) {
      clearTimeout(this.yapTimer);
      if (!this.isYappingActive) return;

      const delay = customDelay || (30000 + Math.random() * 25000);
      this.yapTimer = setTimeout(() => {
        if (!isBubbleOpen && !isTourActive && !this.isDragging) {
          this.startThinkingAndYap();
        }
      }, delay);
    }

    /* ------------------------------------------------------------------------
       PHYSICS LOOP (CONTINUOUS 3D KINEMATICS & EYE TRACKING from .deleteafterdone copy.html)
       ------------------------------------------------------------------------ */
    startPhysicsRenderLoop() {
      const step = () => {
        if (!this.dom.chamber || !this.dom.headComplex) {
          requestAnimationFrame(step);
          return;
        }

        // Target coordinates: user mouse position
        const targetX = this.mousePos.x;
        const targetY = this.mousePos.y;

        // Get Companion World Center
        const rect = this.dom.chamber.getBoundingClientRect();
        const compCenterX = rect.left + rect.width / 2;
        const compCenterY = rect.top + rect.height / 2;

        // Vector from Companion to Target
        const dx = targetX - compCenterX;
        const dy = targetY - compCenterY;
        const dist = Math.hypot(dx, dy) || 1;

        // --------------------------------------------------------------------
        // A. TRUE 3D HEAD TURNING (Continuous Yaw, Pitch, Translation)
        // --------------------------------------------------------------------
        const screenW = window.innerWidth;
        const ratioX = (targetX / screenW) - 0.5; // -0.5 (left) to +0.5 (right)

        // Head turn range from .deleteafterdone copy.html:
        // left is ~0px, center ~28px, right ~58px
        let targetHeadX = 28 + (ratioX * 48);
        let targetHeadY = Math.min(Math.max((dy / 400) * 16, -16), 14);
        let targetHeadRot = (ratioX * 18);

        // Apply Side-Adaptive Constraints (kalau di kanan, wajah di kiri/tengah; kalau di kiri, wajah di kanan/tengah)
        const isDockRight = this.dom.container && this.dom.container.classList.contains('dock-right');
        const isDockLeft = this.dom.container && this.dom.container.classList.contains('dock-left');
        const screenMid = screenW * 0.5;
        const isRightSide = isDockRight || (compCenterX >= screenMid);
        const isLeftSide = isDockLeft || (compCenterX < screenMid);

        if (this.companionState === 'intro') {
          // Centered intro: looking straight ahead
          targetHeadX = 28;
          targetHeadY = 0;
          targetHeadRot = 0;
        } else if (isRightSide) {
          // Tata on right side: head can only face LEFT (0 to 14) or CENTER (~28). NEVER right (> 28)!
          targetHeadX = Math.min(28, Math.max(0, targetHeadX));
          targetHeadRot = Math.min(0, Math.max(-14, targetHeadRot));
        } else if (isLeftSide) {
          // Tata on left side: head can only face RIGHT (42 to 58) or CENTER (~28). NEVER left (< 28)!
          targetHeadX = Math.max(28, Math.min(56, targetHeadX));
          targetHeadRot = Math.max(0, Math.min(14, targetHeadRot));
        }

        // Lerp Head Complex (smooth continuous 60fps)
        this.headShift.x += (targetHeadX - this.headShift.x) * 0.08;
        this.headShift.y += (targetHeadY - this.headShift.y) * 0.08;
        this.headShift.rot += (targetHeadRot - this.headShift.rot) * 0.08;

        this.dom.headComplex.setAttribute(
          'transform',
          `translate(${this.headShift.x.toFixed(2)}, ${this.headShift.y.toFixed(2)}) rotate(${this.headShift.rot.toFixed(2)} 130 130)`
        );

        // Ground shadow reacts to head movement
        if (this.dom.shadowPrimary) {
          this.dom.shadowPrimary.style.transform = `translateX(${(this.headShift.x * 0.4).toFixed(2)}px)`;
        }

        // --------------------------------------------------------------------
        // B. TRUE EYE GAZE & CONVERGENCE (Pupils Lock On Target)
        // --------------------------------------------------------------------
        const maxDeflectX = 8.0;
        const maxDeflectY = 8.5;
        const normDist = Math.min(dist / 380, 1);

        let targetGazeX = 0;
        let targetGazeY = 0;

        if (this.isThinking) {
          targetGazeX = 2.0;
          targetGazeY = -7.5;
        } else if (this.isFidgeting && (this.fidgetEyeL.x !== 0 || this.fidgetEyeL.y !== 0)) {
          targetGazeX = this.fidgetEyeL.x;
          targetGazeY = this.fidgetEyeL.y;
        } else {
          targetGazeX = (dx / dist) * maxDeflectX * normDist;
          targetGazeY = (dy / dist) * maxDeflectY * normDist;

          // Side-adaptive gaze constraints so eyes don't roll off into bezel
          if (isRightSide && dx > 0) {
            targetGazeX = Math.min(0.5, targetGazeX);
          } else if (isLeftSide && dx < 0) {
            targetGazeX = Math.max(-0.5, targetGazeX);
          }
        }

        // Lerp Pupils
        this.gazeCurrent.x += (targetGazeX - this.gazeCurrent.x) * 0.12;
        this.gazeCurrent.y += (targetGazeY - this.gazeCurrent.y) * 0.12;

        // Visor Glass 3D Parallax
        const parallaxX = (this.gazeCurrent.x * 0.35).toFixed(2);
        const parallaxY = (this.gazeCurrent.y * 0.35).toFixed(2);
        this.dom.faceAnchor.setAttribute('transform', `translate(${parallaxX}, ${parallaxY})`);

        // Apply Pupils Positions (Left eye base: 84, 86 | Right eye base: 132, 74)
        const fidLX = this.isFidgeting ? this.fidgetEyeL.x : 0;
        const fidLY = this.isFidgeting ? this.fidgetEyeL.y : 0;
        const fidRX = this.isFidgeting ? this.fidgetEyeR.x : 0;
        const fidRY = this.isFidgeting ? this.fidgetEyeR.y : 0;

        const lx = 84 + this.gazeCurrent.x + fidLX;
        const ly = 86 + this.gazeCurrent.y + fidLY;
        const rx = 132 + (this.gazeCurrent.x * 0.94) + fidRX;
        const ry = 74 + (this.gazeCurrent.y * 0.94) + fidRY;

        this.dom.pupilLeft.setAttribute('transform', `translate(${lx.toFixed(2)}, ${ly.toFixed(2)})`);
        this.dom.pupilRight.setAttribute('transform', `translate(${rx.toFixed(2)}, ${ry.toFixed(2)})`);

        requestAnimationFrame(step);
      };

      requestAnimationFrame(step);
    }

    /* ------------------------------------------------------------------------
       FIRST-TIME CENTERED INTRO SEQUENCE
       ------------------------------------------------------------------------ */
    triggerCenteredIntro() {
      this.companionState = 'intro';
      this.stopRoaming();

      if (this.dom.introBackdrop) this.dom.introBackdrop.classList.add('active');
      if (this.dom.container) {
        this.dom.container.classList.add('intro-centered');
        this.dom.container.classList.remove('dock-right', 'dock-left', 'roaming');
        this.dom.container.style.left = '';
        this.dom.container.style.top = '';
        this.dom.container.style.bottom = '';
        this.dom.container.style.right = '';
        this.dom.container.style.transform = '';
      }

      this.setFacing('center');
      this.applyExpression('excited');
      playSound('chime');

      setTimeout(() => {
        if (this.dom.bubbleWrapper) {
          this.dom.bubbleWrapper.classList.add('active', 'intro-centered-bubble');
          this.dom.bubbleWrapper.classList.remove('banter-mode', 'dock-left');
        }

        this.dom.progressText.innerText = "Selamat Datang!";
        this.dom.title.innerText = "Hai! Aku Tata 👋";
        this.dom.helpMenu.style.display = 'none';
        this.dom.autoProgress.classList.remove('active');

        this.dom.actionsFooter.innerHTML = `
          <button type="button" class="gelly-btn-action secondary" id="btnIntroMyself">
            Jelajahi Sendiri
          </button>
          <button type="button" class="gelly-btn-action primary" id="btnIntroGuide">
            Pandu Saya ✨
          </button>
        `;
        this.dom.actionsFooter.style.display = 'flex';

        const introText = "Aku pemandu interaktifmu di Prototype. Mau tur singkat bareng aku, atau mau keliling sendiri dulu?";
        this.typeIntroMessage(introText);
      }, 500);
    }

    typeIntroMessage(text) {
      this.dom.speechText.textContent = '';
      this.dom.typingCursor.classList.remove('is-hidden');
      let i = 0;
      const speed = 20;

      const tick = () => {
        if (i < text.length) {
          this.dom.speechText.textContent += text.charAt(i);
          i++;
          setTimeout(tick, speed);
        } else {
          this.dom.typingCursor.classList.add('is-hidden');

          const btnGuide = document.getElementById('btnIntroGuide');
          const btnMyself = document.getElementById('btnIntroMyself');

          if (btnGuide) {
            btnGuide.onclick = () => {
              localStorage.setItem('tata_site_introduced_v8', 'true');
              if (this.dom.introBackdrop) this.dom.introBackdrop.classList.remove('active');
              if (this.dom.bubbleWrapper) this.dom.bubbleWrapper.classList.remove('intro-centered-bubble');
              playSound('chime');
              this.applyExpression('happy');

              this.transitionFromCenterToEdge(() => {
                this.renderTourStep(0);
              });
            };
          }

          if (btnMyself) {
            btnMyself.onclick = () => {
              localStorage.setItem('tata_site_introduced_v8', 'true');
              playSound('sad');
              this.triggerFaceFidget('manyun_kiri');

              this.dom.actionsFooter.style.display = 'none';
              this.dom.speechText.textContent = "Siap! Aku bakal jalan-jalan santai di sekitar. Klik aku kapan aja kalau butuh bantuan ya! 🫧";

              setTimeout(() => {
                this.applyExpression('happy');
                if (this.dom.introBackdrop) this.dom.introBackdrop.classList.remove('active');
                this.dom.bubbleWrapper.classList.remove('active');
                this.transitionFromCenterToEdge(() => {
                  this.resumeRoaming();
                });
              }, 1800);
            };
          }
        }
      };
      tick();
    }

    transitionFromCenterToEdge(onComplete) {
      if (!this.dom.container) return;

      const dockOffset = window.innerWidth <= 680 ? -10 : -15;
      const containerW = this.dom.container.offsetWidth || 140;
      const containerH = this.dom.container.offsetHeight || 140;

      const rect = this.dom.container.getBoundingClientRect();
      this.dom.container.classList.remove('intro-centered');
      this.dom.container.classList.add('dock-right', 'gliding-to-dock');
      this.dom.container.style.transition = 'none';
      this.dom.container.style.left = `${rect.left}px`;
      this.dom.container.style.top = `${rect.top}px`;
      this.dom.container.style.bottom = 'auto';
      this.dom.container.style.right = 'auto';
      this.dom.container.style.transform = 'none';

      void this.dom.container.offsetHeight;

      const targetX = window.innerWidth - containerW - dockOffset;
      const targetY = window.innerHeight - containerH - dockOffset;

      this.dom.container.style.transition = 'left 1.1s cubic-bezier(0.34, 1.15, 0.64, 1), top 1.1s cubic-bezier(0.34, 1.15, 0.64, 1)';
      this.dom.container.style.left = `${targetX}px`;
      this.dom.container.style.top = `${targetY}px`;

      setTimeout(() => {
        this.dom.container.classList.remove('gliding-to-dock');
        this.dom.container.style.transition = '';
        this.dom.container.style.left = 'auto';
        this.dom.container.style.top = 'auto';
        this.dom.container.style.right = `${dockOffset}px`;
        this.dom.container.style.bottom = `${dockOffset}px`;
        this.companionState = 'idle';
        this.setFacing('left');
        this.updateBubblePosition();
        if (typeof onComplete === 'function') onComplete();
      }, 1100);
    }

    /* ------------------------------------------------------------------------
       SLOW MULTI-DIRECTIONAL FREE WANDERING (NO CHECKPOINTS)
       ------------------------------------------------------------------------ */
    startFreeRoamStep() {
      if (!this.isRoamingActive || isBubbleOpen || isTourActive || this.isDragging) return;
      if (!this.dom.container || this.dom.container.classList.contains('intro-centered') || this.companionState === 'returning') return;

      const rect = this.dom.container.getBoundingClientRect();
      const currentX = rect.left;
      const currentY = rect.top;

      const padding = 25;
      const size = window.innerWidth <= 680 ? 100 : 140;
      const maxW = Math.max(100, window.innerWidth - size - padding);
      const maxH = Math.max(100, window.innerHeight - size - padding);

      const targetX = Math.floor(padding + Math.random() * (maxW - padding));
      const targetY = Math.floor(padding + Math.random() * (maxH - padding));

      const dx = targetX - currentX;
      const dy = targetY - currentY;
      const dist = Math.hypot(dx, dy);

      const speed = 36; // px/sec (slow & calm)
      const durationSec = Math.max(3.2, Math.min(8.5, dist / speed));

      this.companionState = 'walking';
      const tiltAngle = Math.max(-8, Math.min(8, (dx / 40)));

      // Turn head in direction of motion!
      if (dx > 50) this.setFacing('right');
      else if (dx < -50) this.setFacing('left');
      else this.setFacing('center');

      // Set explicit current pixel coordinates before animating to avoid CSS snap
      this.dom.container.style.transition = 'none';
      this.dom.container.style.left = `${currentX}px`;
      this.dom.container.style.top = `${currentY}px`;
      this.dom.container.style.bottom = 'auto';
      this.dom.container.style.right = 'auto';

      void this.dom.container.offsetHeight;

      this.dom.container.classList.add('roaming');
      this.dom.container.style.transition = `left ${durationSec}s cubic-bezier(0.35, 0, 0.25, 1), top ${durationSec}s cubic-bezier(0.35, 0, 0.25, 1), transform 0.4s ease`;
      this.dom.container.style.left = `${targetX}px`;
      this.dom.container.style.top = `${targetY}px`;
      this.dom.container.style.transform = `rotate(${tiltAngle}deg)`;

      this.applyExpression(dist > 300 ? 'curious' : 'happy');

      clearTimeout(this.roamTimer);
      this.roamTimer = setTimeout(() => {
        this.companionState = 'idle';
        this.dom.container.style.transform = 'rotate(0deg)';
        this.applyExpression('neutral');

        // Pause peacefully for 6-12s, triggering idle fidgets while resting
        const pauseTime = Math.floor(6000 + Math.random() * 6000);
        this.roamTimer = setTimeout(() => {
          this.startFreeRoamStep();
        }, pauseTime);
      }, durationSec * 1000);
    }

    resumeRoaming() {
      clearTimeout(this.roamTimer);
      this.roamTimer = setTimeout(() => {
        this.startFreeRoamStep();
      }, 2500);
    }

    stopRoaming() {
      clearTimeout(this.roamTimer);
      this.companionState = 'idle';
      if (this.dom.container) {
        this.dom.container.style.transform = 'rotate(0deg)';
      }
    }

    returnToHomeCorner(byClick = true, onComplete = null) {
      if (!this.dom.container) return;

      clearTimeout(this.roamTimer);
      this.companionState = 'returning';

      this.dom.container.classList.remove('roaming');
      this.dom.container.classList.add('returning');

      const isDockLeft = this.dom.container.classList.contains('dock-left');
      const dockOffset = window.innerWidth <= 680 ? -10 : -15;
      const containerW = this.dom.container.offsetWidth || 140;
      const containerH = this.dom.container.offsetHeight || 140;

      // Capture exact current coordinates
      const currentRect = this.dom.container.getBoundingClientRect();
      this.dom.container.style.transition = 'none';
      this.dom.container.style.left = `${currentRect.left}px`;
      this.dom.container.style.top = `${currentRect.top}px`;
      this.dom.container.style.bottom = 'auto';
      this.dom.container.style.right = 'auto';

      void this.dom.container.offsetHeight; // Force reflow

      // Destination coordinates in pixels
      const targetX = isDockLeft ? dockOffset : (window.innerWidth - containerW - dockOffset);
      const targetY = window.innerHeight - containerH - dockOffset;

      // Face direction of return & smile
      this.setFacing(isDockLeft ? 'right' : 'left');
      this.applyExpression('happy');

      if (byClick) {
        playSound('slide');
      }

      this.dom.container.style.transition = 'left 0.85s cubic-bezier(0.34, 1.25, 0.64, 1), top 0.85s cubic-bezier(0.34, 1.25, 0.64, 1), transform 0.45s ease';
      this.dom.container.style.left = `${targetX}px`;
      this.dom.container.style.top = `${targetY}px`;
      this.dom.container.style.transform = 'rotate(0deg)';

      setTimeout(() => {
        this.dom.container.classList.remove('returning');
        this.dom.container.style.transition = '';

        // Lock cleanly into CSS corner dock with negative offset (peek-a-boo cut off)
        this.dom.container.style.left = isDockLeft ? `${dockOffset}px` : 'auto';
        this.dom.container.style.right = isDockLeft ? 'auto' : `${dockOffset}px`;
        this.dom.container.style.top = 'auto';
        this.dom.container.style.bottom = `${dockOffset}px`;
        this.dom.container.style.transform = 'none';

        this.companionState = 'idle';
        this.setFacing(isDockLeft ? 'right' : 'left');
        this.updateBubblePosition();

        if (byClick) {
          this.openHelpListMenu();
        }
        if (typeof onComplete === 'function') {
          onComplete();
        }
      }, 850);
    }

    /* ------------------------------------------------------------------------
       POST-GUIDANCE QUICK OPTIONS MENU (ON CLICK)
       ------------------------------------------------------------------------ */
    openHelpListMenu() {
      isTourActive = false;
      hideSpotlight();
      clearTimeout(autoAdvanceTimer);
      clearTimeout(typewriterTimer);
      clearInterval(this.typewriterInterval);
      clearInterval(this.mouthFlapInterval);

      if (this.dom.bubbleWrapper) {
        this.dom.bubbleWrapper.classList.remove('banter-mode', 'intro-centered-bubble');
      }

      this.dom.autoProgress.classList.remove('active');
      this.dom.progressText.innerText = "Menu Cepat";
      this.dom.title.innerText = "Ada yang bisa kubantu? 🌟";
      this.dom.speechText.textContent = "";
      this.dom.typingCursor.classList.add('is-hidden');

      let menuHtml = '';
      if (isGlassShowcase) {
        menuHtml = `
          <div class="tata-help-item" data-action="copy">
            <i data-lucide="copy"></i> Cara salin kode komponen
          </div>
          <div class="tata-help-item" data-action="bg">
            <i data-lucide="palette"></i> Ganti ke Mesh Wallpaper
          </div>
          <div class="tata-help-item" data-action="random">
            <i data-lucide="shuffle"></i> Acak susunan kartu komponen
          </div>
          <div class="tata-help-item" data-action="apps">
            <i data-lucide="layout"></i> Buka Web Apps Studio
          </div>
          <div class="tata-help-item" data-action="tour">
            <i data-lucide="sparkles"></i> Ulangi tur panduan
          </div>
          <div class="tata-help-item" data-action="bye">
            <i data-lucide="smile"></i> Cukup, terima kasih! 👋
          </div>
        `;
      } else if (isWebApps) {
        menuHtml = `
          <div class="tata-help-item" data-action="viewport">
            <i data-lucide="smartphone"></i> Uji simulator viewport
          </div>
          <div class="tata-help-item" data-action="glass">
            <i data-lucide="layers"></i> Lihat 44 Komponen Glass
          </div>
          <div class="tata-help-item" data-action="tour">
            <i data-lucide="sparkles"></i> Ulangi tur panduan
          </div>
          <div class="tata-help-item" data-action="bye">
            <i data-lucide="smile"></i> Cukup, terima kasih! 👋
          </div>
        `;
      } else if (isRawShowcase) {
        menuHtml = `
          <div class="tata-help-item" data-action="glass">
            <i data-lucide="sparkles"></i> Lihat Komponen Glass Dark
          </div>
          <div class="tata-help-item" data-action="hub">
            <i data-lucide="home"></i> Kembali ke Portal Master
          </div>
          <div class="tata-help-item" data-action="tour">
            <i data-lucide="sparkles"></i> Ulangi tur panduan
          </div>
          <div class="tata-help-item" data-action="bye">
            <i data-lucide="smile"></i> Cukup, terima kasih! 👋
          </div>
        `;
      } else {
        // Gateway Hub
        menuHtml = `
          <div class="tata-help-item" data-action="apps">
            <i data-lucide="layout"></i> Buka Web Applications Studio
          </div>
          <div class="tata-help-item" data-action="glass">
            <i data-lucide="sparkles"></i> Eksplorasi 44 Komponen Glass
          </div>
          <div class="tata-help-item" data-action="taxonomy">
            <i data-lucide="book-open"></i> Kamus Taksonomi Komponen
          </div>
          <div class="tata-help-item" data-action="tour">
            <i data-lucide="sparkles"></i> Ulangi tur panduan
          </div>
          <div class="tata-help-item" data-action="bye">
            <i data-lucide="smile"></i> Cukup, terima kasih! 👋
          </div>
        `;
      }

      this.dom.helpMenu.innerHTML = menuHtml;
      this.dom.helpMenu.style.display = 'flex';
      this.dom.actionsFooter.style.display = 'none';

      if (window.lucide) window.lucide.createIcons();

      this.dom.helpMenu.querySelectorAll('.tata-help-item').forEach(item => {
        item.onclick = () => {
          const act = item.getAttribute('data-action');
          if (act === 'copy') {
            highlightElement('.card-actions-tools, .component-card:first-of-type .card-actions-tools', "👉 Klik tombol Salin");
            this.dom.title.innerText = "Salin Kode Mandiri";
            this.dom.speechText.textContent = "Klik tombol Salin di kartu mana pun untuk mengambil kode HTML + CSS!";
            this.dom.helpMenu.style.display = 'none';
            this.dom.actionsFooter.style.display = 'flex';
            this.dom.mainBtn.innerText = "Mengerti! 👍";
            this.dom.mainBtn.onclick = () => {
              this.hideBubble();
              this.resumeRoaming();
            };
          } else if (act === 'bg') {
            highlightElement('.grid-bg-selector', "👉 Pengalih Tema");
            const meshBtn = document.querySelector('.grid-bg-btn[data-bg="mesh"]');
            if (meshBtn) meshBtn.click();
            this.dom.title.innerText = "Wallpaper Mesh Berwarna";
            this.dom.speechText.textContent = "Latar belakang berhasil diubah ke Mesh Berwarna!";
            this.dom.helpMenu.style.display = 'none';
            this.dom.actionsFooter.style.display = 'flex';
            this.dom.mainBtn.innerText = "Bagus! 🎨";
            this.dom.mainBtn.onclick = () => {
              this.hideBubble();
              this.resumeRoaming();
            };
          } else if (act === 'random') {
            if (typeof window.randomizeGrid === 'function') window.randomizeGrid();
            this.dom.title.innerText = "Grid Diacak! 🎲";
            this.dom.speechText.textContent = "Seluruh kartu komponen berhasil diacak tata letaknya!";
            this.dom.helpMenu.style.display = 'none';
            this.dom.actionsFooter.style.display = 'flex';
            this.dom.mainBtn.innerText = "Keren! 🎲";
            this.dom.mainBtn.onclick = () => {
              this.hideBubble();
              this.resumeRoaming();
            };
          } else if (act === 'viewport') {
            highlightElement('.viewport-buttons, .mode-toggle-cluster', "👉 Pengalih Ukuran Layar");
            this.dom.title.innerText = "Simulator Multi-Viewport";
            this.dom.speechText.textContent = "Gunakan tombol atas untuk berganti ukuran mobile, tablet, dan desktop!";
            this.dom.helpMenu.style.display = 'none';
            this.dom.actionsFooter.style.display = 'flex';
            this.dom.mainBtn.innerText = "Paham! 📱";
            this.dom.mainBtn.onclick = () => {
              this.hideBubble();
              this.resumeRoaming();
            };
          } else if (act === 'apps') {
            window.location.href = isGlassShowcase ? '../../apps.html' : (isGateway ? 'ui/web/apps.html' : 'apps.html');
          } else if (act === 'glass') {
            window.location.href = isGateway ? 'ui/web/components/glass/showcase.html' : (isWebApps ? 'components/glass/showcase.html' : '../glass/showcase.html');
          } else if (act === 'hub') {
            window.location.href = isGateway ? 'index.html' : '../../../../index.html';
          } else if (act === 'taxonomy') {
            window.location.href = isGateway ? 'component.md' : '../../component.md';
          } else if (act === 'tour') {
            this.renderTourStep(0);
          } else if (act === 'bye') {
            this.applyExpression('happy');
            this.dom.title.innerText = "Selamat bereksplorasi! 👋";
            this.dom.speechText.textContent = "Aku selalu di sini jika kamu butuh bantuan!";
            this.dom.helpMenu.style.display = 'none';
            userDismissedBubbleAt = Date.now();
            setTimeout(() => {
              this.hideBubble();
              this.resumeRoaming();
            }, 800);
          }
        };
      });

      this.showBubble();
    }

    showBubble() {
      if (this.dom.bubbleWrapper) this.dom.bubbleWrapper.classList.add('active');
      isBubbleOpen = true;
      this.updateBubblePosition();
    }

    hideBubble() {
      if (this.dom.bubbleWrapper) this.dom.bubbleWrapper.classList.remove('active');
      isBubbleOpen = false;
      clearTimeout(autoAdvanceTimer);
      clearTimeout(typewriterTimer);
      hideSpotlight();
    }

    updateBubblePosition() {
      if (!this.dom.container || !this.dom.bubbleWrapper || this.dom.bubbleWrapper.classList.contains('intro-centered-bubble')) return;

      const rect = this.dom.container.getBoundingClientRect();
      const isLeft = rect.left < window.innerWidth * 0.5;
      this.dom.bubbleWrapper.classList.toggle('dock-left', isLeft);

      const isDockLeft = this.dom.container.classList.contains('dock-left');
      const isAtHomeCorner = isDockLeft
        ? (rect.left <= 10 && rect.bottom >= window.innerHeight - 15)
        : (rect.right >= window.innerWidth - 10 && rect.bottom >= window.innerHeight - 15);

      if (isAtHomeCorner) {
        this.dom.bubbleWrapper.style.top = 'auto';
        this.dom.bubbleWrapper.style.bottom = window.innerWidth <= 680 ? '96px' : '128px';
        if (isDockLeft) {
          this.dom.bubbleWrapper.style.left = '24px';
          this.dom.bubbleWrapper.style.right = 'auto';
        } else {
          this.dom.bubbleWrapper.style.right = '24px';
          this.dom.bubbleWrapper.style.left = 'auto';
        }
        return;
      }

      const bubbleH = this.dom.bubbleWrapper.offsetHeight || 160;
      let bubbleTop = rect.top - bubbleH - 14;
      if (bubbleTop < 20) {
        bubbleTop = rect.bottom + 14;
      }

      this.dom.bubbleWrapper.style.top = `${Math.max(16, Math.min(window.innerHeight - bubbleH - 16, bubbleTop))}px`;
      this.dom.bubbleWrapper.style.bottom = 'auto';

      if (isLeft) {
        this.dom.bubbleWrapper.style.left = `${Math.max(16, rect.left)}px`;
        this.dom.bubbleWrapper.style.right = 'auto';
      } else {
        this.dom.bubbleWrapper.style.right = `${Math.max(16, window.innerWidth - rect.right)}px`;
        this.dom.bubbleWrapper.style.left = 'auto';
      }
    }

    /* ------------------------------------------------------------------------
       GUIDED TOUR STEPPER
       ------------------------------------------------------------------------ */
    renderTourStep(index) {
      clearTimeout(autoAdvanceTimer);
      clearTimeout(typewriterTimer);
      isTourActive = true;

      if (index < 0) index = 0;

      if (index >= activeTourSteps.length) {
        clearTimeout(autoAdvanceTimer);
        hideSpotlight();
        isTourActive = false;
        this.applyExpression('excited');
        playSound('chime');
        localStorage.setItem('tata_guidance_completed', 'true');
        this.openHelpListMenu();
        return;
      }

      currentStepIndex = index;
      const step = activeTourSteps[currentStepIndex];

      if (step.selector) {
        const target = document.querySelector(step.selector);
        if (!target || window.getComputedStyle(target).display === 'none') {
          this.renderTourStep(index + 1);
          return;
        }
      }

      this.applyExpression(index % 2 === 0 ? 'happy' : 'curious');
      this.dom.progressText.innerText = `${currentStepIndex + 1}/${activeTourSteps.length}`;
      this.dom.title.innerText = step.title;
      this.dom.helpMenu.style.display = 'none';
      this.dom.actionsFooter.style.display = 'none';

      if (step.selector) {
        highlightElement(step.selector, step.pointerText);
      } else {
        hideSpotlight();
      }

      this.dom.autoProgress.classList.add('active');
      this.dom.autoProgressFill.style.transition = 'none';
      this.dom.autoProgressFill.style.width = '0%';

      playSound('pop');
      this.dom.speechText.textContent = '';
      this.dom.typingCursor.classList.remove('is-hidden');

      let charIdx = 0;
      const text = step.message;
      clearInterval(this.typewriterInterval);

      this.typewriterInterval = setInterval(() => {
        if (charIdx < text.length) {
          this.dom.speechText.textContent += text.charAt(charIdx);
          charIdx++;
        } else {
          clearInterval(this.typewriterInterval);
          this.dom.typingCursor.classList.add('is-hidden');

          const delayMs = 4500;
          this.dom.autoProgressFill.style.transition = `width ${delayMs}ms linear`;
          this.dom.autoProgressFill.style.width = '100%';

          autoAdvanceTimer = setTimeout(() => {
            this.renderTourStep(currentStepIndex + 1);
          }, delayMs);
        }
      }, 20);

      this.showBubble();
    }

    /* ------------------------------------------------------------------------
       EVENT LISTENERS & USER INTERACTIONS
       ------------------------------------------------------------------------ */
    attachEventListeners() {
      // Real-time dynamic mouse tracking
      window.addEventListener('mousemove', (e) => {
        this.mousePos.x = e.clientX;
        this.mousePos.y = e.clientY;
      }, { passive: true });

      // Click on Companion Chamber: Return to corner if roaming/away, or toggle Quick Menu if at home
      this.dom.chamber.addEventListener('click', (e) => {
        if (this.hasMoved) return;
        e.stopPropagation();

        if (this.companionState === 'intro') return;

        const isDockLeft = this.dom.container.classList.contains('dock-left');
        const rect = this.dom.container.getBoundingClientRect();
        const isAtCorner = isDockLeft
          ? (rect.left <= 10 && rect.bottom >= window.innerHeight - 15)
          : (rect.right >= window.innerWidth - 10 && rect.bottom >= window.innerHeight - 15);

        if (this.companionState === 'walking' || !isAtCorner) {
          // If roaming or away from corner: glide back to corner & show help options!
          this.returnToHomeCorner(true);
        } else {
          // Already at home corner: toggle options menu
          this.triggerFaceFidget('smirk');
          playSound('squish');
          if (!isBubbleOpen) {
            this.openHelpListMenu();
          } else {
            this.hideBubble();
            userDismissedBubbleAt = Date.now();
            this.resumeRoaming();
          }
        }
      });

      // Bubble header tools
      const closeBtn = document.getElementById('gellyCloseBtn');
      const minBtn = document.getElementById('gellyMinimizeBtn');
      const soundBtn = document.getElementById('gellySoundBtn');

      if (closeBtn) {
        closeBtn.onclick = () => {
          this.hideBubble();
          userDismissedBubbleAt = Date.now();
          this.resumeRoaming();
        };
      }

      if (minBtn) {
        minBtn.onclick = () => {
          this.hideBubble();
          userDismissedBubbleAt = Date.now();
          playSound('squish');
          this.resumeRoaming();
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

      // Drag and drop setup
      this.initDragAndDrop();
    }

    initDragAndDrop() {
      let dragStartX = 0;
      let dragStartY = 0;
      let initialContainerX = 0;
      let initialContainerY = 0;
      this.hasMoved = false;

      const startDrag = (clientX, clientY) => {
        if (this.dom.container.classList.contains('intro-centered')) return false;

        this.stopRoaming();
        this.isDragging = true;
        this.hasMoved = false;
        dragStartX = clientX;
        dragStartY = clientY;

        const rect = this.dom.container.getBoundingClientRect();
        initialContainerX = rect.left;
        initialContainerY = rect.top;

        this.dom.container.classList.add('dragging');
        this.dom.container.classList.remove('roaming');
        this.dom.container.style.transition = 'none';
        return true;
      };

      const moveDrag = (clientX, clientY) => {
        if (!this.isDragging) return;
        const dx = clientX - dragStartX;
        const dy = clientY - dragStartY;

        if (Math.abs(dx) > 5 || Math.abs(dy) > 5) this.hasMoved = true;

        const newX = Math.max(5, Math.min(window.innerWidth - 130, initialContainerX + dx));
        const newY = Math.max(5, Math.min(window.innerHeight - 130, initialContainerY + dy));

        this.dom.container.style.left = `${newX}px`;
        this.dom.container.style.top = `${newY}px`;
        this.dom.container.style.bottom = 'auto';
        this.dom.container.style.right = 'auto';

        if (clientX < window.innerWidth * 0.4) {
          this.dom.container.classList.add('dock-left');
          this.dom.container.classList.remove('dock-right');
        } else if (clientX > window.innerWidth * 0.6) {
          this.dom.container.classList.add('dock-right');
          this.dom.container.classList.remove('dock-left');
        }

        this.updateBubblePosition();
      };

      const endDrag = () => {
        if (!this.isDragging) return;
        this.isDragging = false;
        this.dom.container.classList.remove('dragging');

        if (!isBubbleOpen) {
          this.resumeRoaming();
        }
      };

      this.dom.chamber.addEventListener('mousedown', (e) => {
        if (e.button === 0) startDrag(e.clientX, e.clientY);
      });

      window.addEventListener('mousemove', (e) => {
        moveDrag(e.clientX, e.clientY);
      });

      window.addEventListener('mouseup', endDrag);

      this.dom.chamber.addEventListener('touchstart', (e) => {
        if (e.touches && e.touches[0]) {
          startDrag(e.touches[0].clientX, e.touches[0].clientY);
        }
      }, { passive: true });

      window.addEventListener('touchmove', (e) => {
        if (e.touches && e.touches[0]) {
          moveDrag(e.touches[0].clientX, e.touches[0].clientY);
        }
      }, { passive: true });

      window.addEventListener('touchend', endDrag);
    }
  }

  /* --------------------------------------------------------------------------
     8. SPOTLIGHT HIGHLIGHTING ENGINE (DYNAMIC SCROLL & RESIZE TRACKING)
     -------------------------------------------------------------------------- */
  let currentHighlightedElement = null;
  let currentPointerText = "Lihat di sini";
  let spotlightRafId = null;
  let scrollDebounceTimer = null;

  function updateSpotlightRect(el, pointerText = null) {
    if (!el) return;
    const overlay = document.getElementById('gellySpotlightOverlay');
    const box = document.getElementById('gellySpotlightBox');
    const badge = document.getElementById('gellyPointerBadge');
    const badgeText = document.getElementById('gellyPointerText');

    if (!overlay || !box || !badge) return;

    if (!document.body.contains(el) || window.getComputedStyle(el).display === 'none') {
      hideSpotlight();
      return;
    }

    const rect = el.getBoundingClientRect();
    const zoom = parseFloat(getComputedStyle(document.documentElement).zoom) || 1;
    const pad = 8;
    const top = (rect.top / zoom) - pad;
    const left = (rect.left / zoom) - pad;
    const width = (rect.width / zoom) + (pad * 2);
    const height = (rect.height / zoom) + (pad * 2);
    // Check if element is completely scrolled out of the viewport
    const isOutOfView = (rect.bottom < -40 || rect.top > (window.innerHeight / zoom) + 40 || rect.right < -40 || rect.left > (window.innerWidth / zoom) + 40);

    if (isOutOfView) {
      box.style.display = 'none';
      badge.style.display = 'none';
      return;
    }

    box.style.display = 'block';
    box.style.top = `${top}px`;
    box.style.left = `${left}px`;
    box.style.width = `${width}px`;
    box.style.height = `${height}px`;

    const textToUse = pointerText || currentPointerText || "Lihat di sini";
    if (badgeText && textToUse) {
      badgeText.innerText = textToUse;
    }

    badge.style.display = 'flex';
    // Position badge above or below depending on available space
    if (top > 60) {
      badge.style.top = `${top - 42}px`;
      badge.style.left = `${Math.min((window.innerWidth / zoom) - 190, Math.max(12, left))}px`;
    } else {
      badge.style.top = `${top + height + 14}px`;
      badge.style.left = `${Math.min((window.innerWidth / zoom) - 190, Math.max(12, left))}px`;
    }

    overlay.classList.add('active');
    if (window.lucide) window.lucide.createIcons();
  }

  function highlightElement(selector, pointerText = "Lihat di sini") {
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
    currentPointerText = pointerText;

    // Smooth scroll to target element
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Initial rect update
    updateSpotlightRect(el, pointerText);

    // Run animation frame loop for 850ms during smooth scroll so highlight stays glued to element
    if (spotlightRafId) cancelAnimationFrame(spotlightRafId);
    const startTime = performance.now();
    const trackScrollAnimation = (now) => {
      if (!currentHighlightedElement || currentHighlightedElement !== el) return;
      updateSpotlightRect(el, currentPointerText);
      if (now - startTime < 850) {
        spotlightRafId = requestAnimationFrame(trackScrollAnimation);
      }
    };
    spotlightRafId = requestAnimationFrame(trackScrollAnimation);
  }

  function hideSpotlight() {
    if (spotlightRafId) cancelAnimationFrame(spotlightRafId);
    currentHighlightedElement = null;
    currentPointerText = '';
    const overlay = document.getElementById('gellySpotlightOverlay');
    const box = document.getElementById('gellySpotlightBox');
    const badge = document.getElementById('gellyPointerBadge');
    if (overlay) overlay.classList.remove('active');
    if (box) box.style.display = 'none';
    if (badge) badge.style.display = 'none';
  }

  // Real-time dynamic alignment during scroll and resize
  window.addEventListener('scroll', () => {
    if (currentHighlightedElement) {
      const box = document.getElementById('gellySpotlightBox');
      const badge = document.getElementById('gellyPointerBadge');
      if (box) box.style.transition = 'none';
      if (badge) badge.style.transition = 'none';

      updateSpotlightRect(currentHighlightedElement, currentPointerText);

      clearTimeout(scrollDebounceTimer);
      scrollDebounceTimer = setTimeout(() => {
        if (box) box.style.transition = '';
        if (badge) badge.style.transition = '';
      }, 120);
    }
  }, { passive: true, capture: true });

  window.addEventListener('resize', () => {
    if (currentHighlightedElement) {
      updateSpotlightRect(currentHighlightedElement, currentPointerText);
    }
  });

  /* --------------------------------------------------------------------------
     9. INITIALIZATION
     -------------------------------------------------------------------------- */
  function init() {
    injectCompanionUI();
    window.__companion = new CompanionEngine();
    window.__companion.init();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
