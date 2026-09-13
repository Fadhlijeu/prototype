/**
 * ==========================================================================
 * TATA — Interactive Physics-Driven Blob Companion & Guidance System
 * Inspired by FeralUI playful physics elements (https://feralui.dev/blob)
 * 
 * Features:
 * - Mascot official name: "TATA"
 * - Full English casual conversational dialogues & short playful yappings
 * - Dramatic first-time fullscreen website backdrop blur introduction
 * - Active mobile touch tracking (touchstart/touchmove follows user's finger)
 * - Page-adaptive theme colors (Glass, Web Apps, Raw Semantic, Gateway)
 * - Zero idle jiggle: calm and stable when still; only jiggles when walking!
 * - Super slow, gentle, relaxing walking motion along screen edge
 * - Instant playful slide return when tapped during walking ("Eep! You caught me!")
 * - Non-disappearing peek minimize (eyes keep watching and blinking)
 * - Ultra-translucent glass speech popup with minimal buttons to prevent confusion
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
                osc.frequency.exponentialRampToValueAtTime(220, now + 0.3);
                gain.gain.setValueAtTime(0.15, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
                osc.start(now);
                osc.stop(now + 0.35);
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

    document.body.classList.add(`page-theme-${currentPageKey}`);

    const pageGreetings = {
        gateway: {
            title: "HIII! I'm Tata 👋",
            message: "Welcome to <strong>Prototype Gateway</strong>! Curious about what this website is? It connects 44 glass components, standalone web apps, and raw HTML. Want a quick tour?",
            badge: "Gateway Portal"
        },
        glass: {
            title: "HIII! I'm Tata 👋",
            message: "Welcome to the <strong>Glass Showroom</strong>! 44 dark glass components live here. Curious to see how it works, or want to test the <strong>Randomize</strong> button?",
            badge: "Glass Showroom"
        },
        webapps: {
            title: "HIII! I'm Tata 👋",
            message: "You made it to <strong>Web Applications Studio</strong>! These are full working apps, not just isolated snippets. Try toggling between <strong>Mobile</strong> and <strong>Desktop</strong> viewports!",
            badge: "Web Apps Studio"
        },
        raw: {
            title: "HIII! I'm Tata 👋",
            message: "Welcome to <strong>Raw HTML Showcase</strong>! Pure semantic HTML5 components with zero CSS, perfect for structural and accessibility reference.",
            badge: "Raw Semantic"
        }
    };

    /* --------------------------------------------------------------------------
       3. CASUAL SHORT YAPPINGS & FUN FACTS (Pure natural dialogue, no buttons!)
       -------------------------------------------------------------------------- */
    const casualDialogues = [
        {
            title: "hi.",
            message: "just wanted to say hi.",
            expression: 'happy'
        },
        {
            title: "Hello beauty... ✨",
            message: "You're looking sharp today! What kind of cool web stuff are we building?",
            expression: 'wink'
        },
        {
            title: "Did you know? 💡",
            message: "All 44 components here are 100% standalone—no npm, no node_modules, no build tools required!",
            expression: 'surprised'
        },
        {
            title: "staring contest 👀",
            message: "3... 2... 1... ha! You blinked first! Don't worry, my eyes are always open.",
            expression: 'laugh'
        },
        {
            title: "Did you know? 💡",
            message: "The Randomize button shuffles all 44 component cards into a fresh layout in a blink!",
            expression: 'happy'
        },
        {
            title: "poke me! 🫧",
            message: "poke me again and I might wobble for you! I'm made of squishy jelly.",
            expression: 'happy'
        },
        {
            title: "Did you know? 💡",
            message: "Glassmorphism uses real-time backdrop blur to guide focus directly to your primary content.",
            expression: 'ponder'
        },
        {
            title: "just vibing ☕",
            message: "just hanging out in the corner, don't mind me. Take your time exploring.",
            expression: 'ponder'
        },
        {
            title: "Did you know? 💡",
            message: "Clicking 'Full' on any card unlocks a live interactive sandbox with device resizers.",
            expression: 'surprised'
        },
        {
            title: "bloop bloop 🫧",
            message: "bloop bloop bloop... okay, I'm done. Back to serious coding mode!",
            expression: 'laugh'
        },
        {
            title: "Did you know? 💡",
            message: "Dark mode actually saves battery life on OLED and AMOLED phone screens!",
            expression: 'happy'
        },
        {
            title: "hey you!",
            message: "take a sip of water and stretch your shoulders. Coding posture is important!",
            expression: 'happy'
        },
        {
            title: "Did you know? 💡",
            message: "There are zero fake AI buttons here. Every slider, tab, and card really works.",
            expression: 'laugh'
        },
        {
            title: "watch out! 💨",
            message: "if you leave me alone for a bit, I might go for a slow walk up your screen!",
            expression: 'wink'
        },
        {
            title: "Did you know? 💡",
            message: "Web Applications Studio has full apps like Cloud File Manager with synthesized sound!",
            expression: 'surprised'
        },
        {
            title: "Curious? 🧭",
            message: "Want to know how this whole showroom works? Tap the tour button below!",
            expression: 'happy'
        }
    ];

    let dialogueIdx = 0;
    let currentExpression = 'happy'; // 'happy', 'laugh', 'wink', 'surprised', 'ponder'

    /* --------------------------------------------------------------------------
       4. CONCISE TOUR CONFIGURATIONS (Simple, clean, English)
       -------------------------------------------------------------------------- */
    const showcaseTour = [
        {
            title: "1. Category Filter",
            message: "Filter components by type: <strong>Buttons</strong>, <strong>Cards</strong>, <strong>Inputs</strong>, or full <strong>UI Kits</strong>.",
            selector: "#filterTabs, .filter-tabs",
            pointerText: "👉 Category Filter",
            btnText: "Next"
        },
        {
            title: "2. Grid Layout Switcher",
            message: "Adjust the grid layout to <strong>1, 2, 3, 4 columns, or Auto</strong> to suit your display.",
            selector: ".layout-selector, .controls-right",
            pointerText: "👉 Grid Columns",
            btnText: "Next"
        },
        {
            title: "3. Component Showroom (44 Items)",
            message: "Here's the main showroom! All 44 interactive glass components are ready to test and inspect.",
            selector: "#componentsGrid, .components-grid",
            pointerText: "👉 44 Components Grid",
            btnText: "Next"
        },
        {
            title: "4. Background Theme Switcher",
            message: "Toggle between deep <strong>Obsidian Dark</strong> and colorful <strong>Mesh Gradient</strong> wallpapers.",
            selector: ".grid-bg-selector",
            pointerText: "👉 Background Theme",
            btnText: "Next"
        },
        {
            title: "5. One-Click Code Copy",
            message: "Every component is <strong>standalone</strong>. Click <strong>Copy</strong> to grab the complete HTML, CSS, and JS code instantly!",
            selector: ".card-actions-tools, .component-card:first-of-type .card-actions-tools",
            pointerText: "👉 Copy Standalone Code",
            btnText: "Next"
        },
        {
            title: "6. Fullscreen Component Sandbox",
            message: "Click <strong>Full</strong> on any card to open the fullscreen sandbox with multi-device resizers.",
            selector: ".btn-card-full, .component-card:first-of-type .btn-card-full",
            pointerText: "👉 Full Sandbox",
            btnText: "Finish ✦"
        }
    ];

    const gatewayTour = [
        {
            title: "1. Web Applications Studio",
            message: "Explore full-scale production apps like <strong>Cloud File Manager</strong> and <strong>AI Agent Studio</strong>.",
            selector: ".hub-card[href*='apps.html'], .hub-grid a:first-child",
            pointerText: "👉 Web Apps Studio",
            btnText: "Next"
        },
        {
            title: "2. Glass Style Showcase",
            message: "Catalog of <strong>44 Glass Dark Premium</strong> components with live previews and copyable code.",
            selector: ".hub-card[href*='showcase.html'], .hub-grid a:nth-child(2)",
            pointerText: "👉 Glass Showcase",
            btnText: "Next"
        },
        {
            title: "3. Raw Semantic HTML & Taxonomy",
            message: "Unstyled semantic HTML5 components and taxonomy reference with 120+ standard elements.",
            selector: ".hub-card[href*='raw/showcase.html'], .hub-grid a:nth-child(3)",
            pointerText: "👉 Raw HTML5",
            btnText: "Finish ✦"
        }
    ];

    const webappsTour = [
        {
            title: "1. App Simulator Canvas",
            message: "Live interactive canvas displaying the active web application.",
            selector: "#stageSection, .app-showcase-box",
            pointerText: "👉 Live Simulator",
            btnText: "Next"
        },
        {
            title: "2. Multi-Device Viewport Switcher",
            message: "Test responsive behavior by switching between <strong>Mobile</strong>, <strong>Tablet</strong>, and <strong>Desktop</strong> sizes!",
            selector: ".viewport-buttons, .mode-toggle-cluster",
            pointerText: "👉 Viewport Switcher",
            btnText: "Next"
        },
        {
            title: "3. Project Selector Tabs",
            message: "Select which project to launch: Cloud File Manager, AI Studio, and future projects.",
            selector: ".project-tabs-cluster, .projects-selection-bar",
            pointerText: "👉 Choose App",
            btnText: "Finish ✦"
        }
    ];

    const rawTour = [
        {
            title: "1. Raw HTML5 Components",
            message: "Catalog of browser native forms, tables, meters, and dialogs without any CSS styling.",
            selector: ".raw-grid, .components-grid",
            pointerText: "👉 Raw Components",
            btnText: "Next"
        },
        {
            title: "2. Navigation",
            message: "Use the top header links to return to Gateway or jump into the Glass Showcase.",
            selector: ".header-actions",
            pointerText: "👉 Navigation",
            btnText: "Finish ✦"
        }
    ];

    let activeTourSteps = showcaseTour;
    if (isWebApps) activeTourSteps = webappsTour;
    else if (isRawShowcase) activeTourSteps = rawTour;
    else if (isGateway) activeTourSteps = gatewayTour;

    let currentStepIndex = 0;
    let isTourActive = false;

    /* --------------------------------------------------------------------------
       5. INJECT DOM ELEMENTS & GRAND INTRO OVERLAY (Clean, no button overload!)
       -------------------------------------------------------------------------- */
    function injectCompanionUI() {
        // 1. Fullscreen First-Time Intro Overlay (Blurs entire website!)
        const introOverlay = document.createElement('div');
        introOverlay.id = 'tataIntroOverlay';
        introOverlay.className = 'tata-intro-overlay';
        introOverlay.innerHTML = `
            <div class="tata-intro-card">
                <div class="tata-intro-avatar">🐾</div>
                <div class="tata-intro-tag">✨ Meet Tata</div>
                <h3 class="tata-intro-title">HIII! I'm Tata 👋</h3>
                <p class="tata-intro-desc">
                    Your squishy companion in <strong>Prototype</strong>! Curious about this website? I'm here to show you 44 dark glass components, web apps, or just hang out. Ready to explore?
                </p>
                <div class="tata-intro-actions">
                    <button type="button" class="btn-intro-secondary" id="btnIntroSkip">Explore Myself</button>
                    <button type="button" class="btn-intro-primary" id="btnIntroStart">Show me around! 🚀</button>
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
        badge.innerHTML = `<i data-lucide="sparkles"></i> <span id="gellyPointerText">Guide</span>`;

        // 3. Blob Mascot Container
        const companion = document.createElement('div');
        companion.id = 'gellyCompanionContainer';
        companion.className = 'gelly-companion-container';

        const canvas = document.createElement('canvas');
        canvas.id = 'gellyCanvas';
        canvas.className = 'gelly-canvas';
        canvas.width = 280;
        canvas.height = 280;
        canvas.title = "Hiii! I'm Tata. Tap me to chat or take a tour.";

        const pingDot = document.createElement('div');
        pingDot.className = 'gelly-ping-dot';
        pingDot.title = "New tip from Tata!";

        companion.appendChild(canvas);
        companion.appendChild(pingDot);

        // 4. Speech Bubble Wrapper (Ultra-translucent frosted glass, NO button overload!)
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
                        <button type="button" class="gelly-tool-btn" id="gellySoundBtn" title="Toggle Sound">
                            <i data-lucide="${isMuted ? 'volume-x' : 'volume-2'}"></i>
                        </button>
                        <button type="button" class="gelly-tool-btn" id="gellyMinimizeBtn" title="Minimize Tata">
                            <i data-lucide="minus"></i>
                        </button>
                        <button type="button" class="gelly-tool-btn" id="gellyCloseBtn" title="Close">
                            <i data-lucide="x"></i>
                        </button>
                    </div>
                </div>

                <div class="gelly-bubble-content">
                    <h4 class="gelly-title" id="gellyTitle">${pageGreetings[currentPageKey].title}</h4>
                    <p class="gelly-message" id="gellyMessage">${pageGreetings[currentPageKey].message}</p>
                </div>

                <!-- Clean Actions Footer (NO button clutter!) -->
                <div class="gelly-actions-footer">
                    <button type="button" class="gelly-btn-action secondary" id="gellyPrevBtn" style="display: none;">
                        <i data-lucide="arrow-left"></i> Back
                    </button>
                    <button type="button" class="gelly-btn-action highlight" id="gellyHighlightBtn" style="display: none;">
                        <i data-lucide="crosshair"></i> Focus
                    </button>
                    <button type="button" class="gelly-btn-action primary" id="gellyNextBtn" style="width: 100%; justify-content: center;">
                        Show me around ✨
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

    function highlightElement(selector, pointerText = "👉 Look here!") {
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
            const pointerText = badge ? document.getElementById('gellyPointerText').innerText : "Guide";
            updateSpotlightRect(currentHighlightedElement, pointerText);
        }
    }, { passive: true });

    window.addEventListener('resize', () => {
        if (currentHighlightedElement) {
            const badge = document.getElementById('gellyPointerBadge');
            const pointerText = badge ? document.getElementById('gellyPointerText').innerText : "Guide";
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
            document.getElementById('gellyTitle').innerText = "You're All Set! 🎉";
            document.getElementById('gellyMessage').innerHTML = "You've seen all the main features. Tap me anytime for a quick chat, or just explore on your own!";
            document.getElementById('gellyStepCounter').innerText = "";
            document.getElementById('gellyPrevBtn').style.display = 'none';
            document.getElementById('gellyHighlightBtn').style.display = 'none';
            document.getElementById('gellyNextBtn').style.width = '100%';
            document.getElementById('gellyNextBtn').innerHTML = `Got it! <i data-lucide="check"></i>`;
            if (window.lucide) window.lucide.createIcons();
            return;
        }

        currentStepIndex = index;
        const step = activeTourSteps[currentStepIndex];

        currentExpression = (index % 2 === 0) ? 'happy' : 'wink';
        document.getElementById('gellyBadgeText').innerText = "Tata's Tour";
        document.getElementById('gellyTitle').innerText = step.title;
        document.getElementById('gellyMessage').innerHTML = step.message;
        document.getElementById('gellyStepCounter').innerText = `(${currentStepIndex + 1}/${activeTourSteps.length})`;

        const prevBtn = document.getElementById('gellyPrevBtn');
        const nextBtn = document.getElementById('gellyNextBtn');
        const hlBtn = document.getElementById('gellyHighlightBtn');

        prevBtn.style.display = currentStepIndex > 0 ? 'inline-flex' : 'none';
        nextBtn.style.width = currentStepIndex > 0 ? 'auto' : '100%';
        
        if (step.selector && document.querySelector(step.selector)) {
            hlBtn.style.display = 'inline-flex';
            highlightElement(step.selector, step.pointerText);
        } else {
            hlBtn.style.display = 'none';
            hideSpotlight();
        }

        const isLast = currentStepIndex === activeTourSteps.length - 1;
        nextBtn.innerHTML = isLast ? `Finish <i data-lucide="check"></i>` : `${step.btnText || 'Next'} <i data-lucide="arrow-right"></i>`;

        if (window.lucide) window.lucide.createIcons();
        playSound('pop');
    }

    // Spontaneous natural yapping & fun facts when user taps Tata
    function triggerSpontaneousDialogue() {
        isTourActive = false;
        hideSpotlight();
        const dlg = casualDialogues[dialogueIdx % casualDialogues.length];
        dialogueIdx++;

        currentExpression = dlg.expression || 'happy';
        document.getElementById('gellyBadgeText').innerText = "Tata ✦";
        document.getElementById('gellyStepCounter').innerText = "";
        document.getElementById('gellyTitle').innerText = dlg.title;
        document.getElementById('gellyMessage').innerHTML = dlg.message;

        document.getElementById('gellyPrevBtn').style.display = 'none';
        document.getElementById('gellyHighlightBtn').style.display = 'none';
        const nextBtn = document.getElementById('gellyNextBtn');
        nextBtn.style.width = '100%';
        nextBtn.innerHTML = `Show me around ✨`;

        showBubble();
        playSound('chime');
    }

    /* --------------------------------------------------------------------------
       8. RANDOM WANDERING & JIGGLE WALKING ALONG SCREEN EDGE (Super Slow!)
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

        // Pick gentle height on the right side of the screen (between 160px and 50vh)
        const randomBottom = Math.floor(160 + Math.random() * (window.innerHeight * 0.4));
        container.style.bottom = `${randomBottom}px`;
        container.style.right = `-5px`;

        playSound('squish');

        // Auto return after 18 seconds of slow walk if user doesn't touch her
        clearTimeout(walkInterval);
        walkInterval = setTimeout(() => {
            if (companionState === 'walking') {
                returnToHomeCorner(false);
            }
        }, 18000);
    }

    // When clicked/tapped during walking: instant playful slide return back to home corner!
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
            document.getElementById('gellyTitle').innerText = "Eep! You caught me 💨";
            document.getElementById('gellyMessage').innerHTML = "I was just taking a slow stroll up your screen... sliding right back to my corner!";
            document.getElementById('gellyPrevBtn').style.display = 'none';
            document.getElementById('gellyHighlightBtn').style.display = 'none';
            document.getElementById('gellyNextBtn').style.width = '100%';
            document.getElementById('gellyNextBtn').innerHTML = `Show me around ✨`;
            showBubble();
        } else {
            currentExpression = 'happy';
        }

        setTimeout(() => {
            container.classList.remove('returning');
            companionState = 'idle';
        }, 1100);
    }

    function resetIdleTimer() {
        clearTimeout(idleTimer);
        // Start slow wander walk after 28 seconds of quiet idle
        idleTimer = setTimeout(() => {
            if (companionState === 'idle' && !isBubbleOpen) {
                startWanderWalk();
            }
        }, 28000);
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

        function dismissIntro(startTour = false) {
            if (introOverlay) {
                introOverlay.classList.remove('active');
                localStorage.setItem('tata_intro_seen_v4', 'true');
                playSound('chime');
                setTimeout(() => {
                    if (startTour) {
                        showBubble();
                        renderTourStep(0);
                    } else {
                        showBubble();
                    }
                }, 400);
            }
        }

        if (introStart) introStart.onclick = () => dismissIntro(true);
        if (introSkip) introSkip.onclick = () => dismissIntro(false);

        if (closeBtn) closeBtn.onclick = () => hideBubble();
        
        // Minimize: Tata doesn't disappear! Her eyes keep peeking gently
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
                if (nextBtn.innerText.includes('Show me around')) {
                    renderTourStep(0);
                } else if (currentStepIndex >= activeTourSteps.length - 1 && nextBtn.innerText.includes('Got it')) {
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
    }

    /* --------------------------------------------------------------------------
       9. FERALUI-INSPIRED SOFT-BODY SPRING PHYSICS JELLY BLOB (Canvas 2D)
       NO IDLE JIGGLE: Perfectly calm and stable when still!
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
                        p.vr += 3.0;
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
                            p.vr += 3.5;
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

            // IF TATA IS WALKING: Play slide return back to home corner!
            if (companionState === 'walking') {
                returnToHomeCorner(true);
                return;
            }

            // Normal click: Squish and spontaneous casual dialogue!
            squashX = 1.30;
            squashY = 0.75;
            squashVx = -0.18;
            squashVy = 0.18;

            points.forEach((p) => {
                p.vr += (Math.random() - 0.5) * 16;
            });

            playSound('squish');

            const container = document.getElementById('gellyCompanionContainer');
            if (container && container.classList.contains('minimized')) {
                container.classList.remove('minimized');
                showBubble();
            } else if (!isBubbleOpen) {
                // Spontaneous funny remark / fun fact when clicked!
                triggerSpontaneousDialogue();
            } else {
                toggleBubble();
            }
        });

        let lastTime = performance.now();

        function render(now) {
            const dt = Math.min((now - lastTime) / 1000, 0.1);
            lastTime = now;

            // SUPER SLOW WALKING JIGGLE (Only active while walking!)
            if (companionState === 'walking') {
                squashY = 1 + Math.sin(now * 0.003) * 0.10;
                squashX = 1 - Math.sin(now * 0.003) * 0.06;
            } else {
                // Return smoothly to 1.0 and STAY STILL (NO IDLE JIGGLE!)
                const springK = 80;
                const springDamp = 8.0;

                const fx = (1 - squashX) * springK - squashVx * springDamp;
                squashVx += fx * dt;
                squashX += squashVx * dt;

                const fy = (1 - squashY) * springK - squashVy * springDamp;
                squashVy += fy * dt;
                squashY += squashVy * dt;
            }

            // Radial Spring simulation:
            // When IDLE: target is strictly baseRadius with ZERO sinus wave! Smooth & calm!
            // When WALKING: subtle gentle crawl wave!
            const pSpringK = 85;
            const pDamp = 7.5;

            points.forEach((p, i) => {
                let target = p.baseRadius;
                if (companionState === 'walking') {
                    target += Math.sin(now * 0.003 + i * 0.6) * 3.0; // gentle walk wave
                }
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
                blinkProgress += dt * 8;
                if (blinkProgress >= 1) {
                    isBlinking = false;
                    blinkProgress = 0;
                    nextBlinkTime = now + (2800 + Math.random() * 4500);
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
                grad.addColorStop(0, '#22D3EE');
                grad.addColorStop(0.4, '#0284C7');
                grad.addColorStop(0.8, '#2563EB');
                grad.addColorStop(1, '#0F172A');
            } else if (isRawShowcase) {
                grad.addColorStop(0, '#93C5FD');
                grad.addColorStop(0.4, '#3B82F6');
                grad.addColorStop(0.8, '#475569');
                grad.addColorStop(1, '#1E293B');
            } else {
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
                
                if (currentExpression === 'wink' && isWinkEye) {
                    ctx.scale(1, 0.15);
                } else if (currentExpression === 'laugh') {
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
                ctx.beginPath();
                ctx.arc(mouthCenter.x, mouthCenter.y - 2, 9, 0, Math.PI, false);
                ctx.fill();
            } else if (currentExpression === 'surprised' || companionState === 'walking') {
                ctx.beginPath();
                ctx.arc(mouthCenter.x, mouthCenter.y, 5, 0, Math.PI * 2);
                ctx.stroke();
            } else if (currentExpression === 'ponder') {
                ctx.beginPath();
                ctx.moveTo(mouthCenter.x - 7, mouthCenter.y);
                ctx.quadraticCurveTo(mouthCenter.x - 3, mouthCenter.y - 3, mouthCenter.x, mouthCenter.y);
                ctx.quadraticCurveTo(mouthCenter.x + 3, mouthCenter.y + 3, mouthCenter.x + 7, mouthCenter.y);
                ctx.stroke();
            } else if (isHovered || isBubbleOpen || currentExpression === 'wink') {
                ctx.beginPath();
                ctx.arc(mouthCenter.x, mouthCenter.y, 8, 0.15 * Math.PI, 0.85 * Math.PI, false);
                ctx.stroke();
            } else {
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
        const hasSeenIntro = localStorage.getItem('tata_intro_seen_v5');
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
