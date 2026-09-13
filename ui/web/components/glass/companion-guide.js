/**
 * ==========================================================================
 * TATA — Interactive Physics-Driven Blob Companion & Guidance System
 * Inspired by FeralUI playful physics elements (https://feralui.dev/blob)
 * 
 * New Upgrades:
 * - Auto-advancing guidance with smooth delays (NO Next button, NO Focus button)
 * - Typewriter text effect with synchronized mouth movement
 * - Edge Drag & Drop: Drag Tata vertically; snaps to screen edges
 * - Disappointed pout reaction if user picks "Explore Myself"
 * - Auto-wander when minimized or after guidance finishes
 * - Zero idle jiggle: completely calm and stable when still
 * - Ultra-slow, relaxing jiggle walk
 * - Single-time site intro bug fix (does NOT re-trigger on page switch)
 * - Finished tour leads to friendly help menu (does NOT loop back)
 * - Mobile check: skips desktop-only column selector on small screens
 * - Plain bubble header without name tag
 * ==========================================================================
 */

(function () {
    'use strict';

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
            if (audioCtx.state === 'suspended') audioCtx.resume();

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
                osc.frequency.exponentialRampToValueAtTime(280, now + 0.25);
                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
                osc.start(now);
                osc.stop(now + 0.3);
            }
        } catch (e) {}
    }

    /* --------------------------------------------------------------------------
       2. PAGE IDENTIFICATION & THEME
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

    /* --------------------------------------------------------------------------
       3. CASUAL SHORT YAPPINGS & FUN FACTS
       -------------------------------------------------------------------------- */
    const casualDialogues = [
        { title: "hi.", message: "just wanted to say hi.", expression: 'happy' },
        { title: "Hello beauty... ✨", message: "You're looking sharp today! What are we building?", expression: 'wink' },
        { title: "Did you know? 💡", message: "All 44 components here are 100% standalone—no npm, no node_modules required!", expression: 'surprised' },
        { title: "staring contest 👀", message: "3... 2... 1... ha! You blinked first! My eyes are always watching.", expression: 'laugh' },
        { title: "Did you know? 💡", message: "The Randomize button shuffles all 44 component cards instantly!", expression: 'happy' },
        { title: "poke me! 🫧", message: "poke me again and I might wobble for you!", expression: 'happy' },
        { title: "Did you know? 💡", message: "Glassmorphism uses backdrop blur so you focus right on primary actions.", expression: 'ponder' },
        { title: "just vibing ☕", message: "just hanging out by the edge, don't mind me. Take your time.", expression: 'ponder' },
        { title: "Did you know? 💡", message: "Clicking 'Full' on any card unlocks a live interactive device resizer!", expression: 'surprised' },
        { title: "bloop bloop 🫧", message: "bloop bloop bloop... okay, I'm done. Back to coding mode!", expression: 'laugh' },
        { title: "Did you know? 💡", message: "Dark mode saves battery life on modern OLED phone screens!", expression: 'happy' },
        { title: "hey you!", message: "take a sip of water and stretch those shoulders.", expression: 'happy' },
        { title: "Did you know? 💡", message: "There are zero dummy AI buttons here. Every single component works!", expression: 'laugh' },
        { title: "watch out! 💨", message: "if you leave me alone, I might go for a slow stroll up your screen!", expression: 'wink' },
        { title: "Did you know? 💡", message: "You can drag me up and down along the side of your screen!", expression: 'wink' }
    ];

    let dialogueIdx = 0;
    let currentExpression = 'happy'; // 'happy', 'laugh', 'wink', 'surprised', 'ponder', 'pout'
    let isTalking = false;

    /* --------------------------------------------------------------------------
       4. CONCISE TOUR CONFIGURATIONS (Simplified, Beginner-Friendly)
       -------------------------------------------------------------------------- */
    const isMobileDevice = window.innerWidth <= 680;

    const showcaseTour = [
        {
            title: "Category Filter",
            message: "Filter cards by type: Buttons, Cards, Inputs, or full UI Kits.",
            selector: "#filterTabs, .filter-tabs",
            pointerText: "👉 Category Filter"
        },
        // Only include Grid Columns switcher if on desktop (hidden on mobile)
        ...(!isMobileDevice ? [{
            title: "Grid Columns",
            message: "Switch between 1, 2, 3, 4 columns or Auto to fit your screen.",
            selector: ".layout-selector, .controls-right",
            pointerText: "👉 Grid Columns"
        }] : []),
        {
            title: "44 Glass Components",
            message: "Here's the main grid! All 44 interactive dark glass components are live.",
            selector: "#componentsGrid, .components-grid",
            pointerText: "👉 44 Components Grid"
        },
        {
            title: "Background Theme",
            message: "Toggle between deep Obsidian Dark and colorful Mesh Gradient wallpapers.",
            selector: ".grid-bg-selector",
            pointerText: "👉 Background Theme"
        },
        {
            title: "One-Click Copy",
            message: "Every component is standalone. Click Copy to grab HTML, CSS, and JS code instantly!",
            selector: ".card-actions-tools, .component-card:first-of-type .card-actions-tools",
            pointerText: "👉 Copy Code"
        },
        {
            title: "Fullscreen Studio",
            message: "Click Full on any card to test it with interactive device screen resizers.",
            selector: ".btn-card-full, .component-card:first-of-type .btn-card-full",
            pointerText: "👉 Full Studio"
        }
    ];

    const gatewayTour = [
        {
            title: "Web Applications Studio",
            message: "Full-scale production apps like Cloud File Manager and AI Studio.",
            selector: ".hub-card[href*='apps.html'], .hub-grid a:first-child",
            pointerText: "👉 Web Apps"
        },
        {
            title: "Glass Style Showcase",
            message: "Catalog of 44 Glass Dark components with live copyable code.",
            selector: ".hub-card[href*='showcase.html'], .hub-grid a:nth-child(2)",
            pointerText: "👉 Glass Showcase"
        },
        {
            title: "Raw HTML5 Showcase",
            message: "Unstyled semantic HTML5 elements for anatomy and accessibility reference.",
            selector: ".hub-card[href*='raw/showcase.html'], .hub-grid a:nth-child(3)",
            pointerText: "👉 Raw HTML"
        }
    ];

    const webappsTour = [
        {
            title: "Live App Simulator",
            message: "Interact with live web applications directly inside this canvas.",
            selector: "#stageSection, .app-showcase-box",
            pointerText: "👉 Live App"
        },
        {
            title: "Viewport Switcher",
            message: "Test responsive layouts for Mobile, Tablet, and Desktop sizes!",
            selector: ".viewport-buttons, .mode-toggle-cluster",
            pointerText: "👉 Viewport Switcher"
        },
        {
            title: "Choose Web App",
            message: "Select which project to launch: Cloud File Manager or AI Studio.",
            selector: ".project-tabs-cluster, .projects-selection-bar",
            pointerText: "👉 Choose App"
        }
    ];

    const rawTour = [
        {
            title: "Raw HTML5 Components",
            message: "Catalog of browser native forms, tables, and dialogs without CSS styling.",
            selector: ".raw-grid, .components-grid",
            pointerText: "👉 Raw Components"
        },
        {
            title: "Header Navigation",
            message: "Jump back to Master Gateway or visit the Glass Showcase.",
            selector: ".header-actions",
            pointerText: "👉 Navigation"
        }
    ];

    let activeTourSteps = showcaseTour;
    if (isWebApps) activeTourSteps = webappsTour;
    else if (isRawShowcase) activeTourSteps = rawTour;
    else if (isGateway) activeTourSteps = gatewayTour;

    let currentStepIndex = 0;
    let isTourActive = false;
    let autoAdvanceTimer = null;
    let typewriterTimer = null;

    /* --------------------------------------------------------------------------
       5. TYPEWRITER EFFECT ENGINE
       -------------------------------------------------------------------------- */
    function typeText(targetEl, text, speed = 20, onComplete) {
        clearTimeout(typewriterTimer);
        targetEl.innerHTML = '';
        isTalking = true;

        const cursor = document.createElement('span');
        cursor.className = 'tata-typing-cursor';
        targetEl.appendChild(cursor);

        let i = 0;
        function tick() {
            if (i < text.length) {
                const char = text.charAt(i);
                cursor.insertAdjacentText('beforebegin', char);
                i++;
                typewriterTimer = setTimeout(tick, speed);
            } else {
                cursor.remove();
                isTalking = false;
                if (typeof onComplete === 'function') onComplete();
            }
        }
        tick();
    }

    /* --------------------------------------------------------------------------
       6. DOM INJECTION (Plain & Clean, No Clutter)
       -------------------------------------------------------------------------- */
    function injectCompanionUI() {
        // 1. First-time Intro Modal (Plain, Tata talks directly in 1st person)
        const introOverlay = document.createElement('div');
        introOverlay.id = 'tataIntroOverlay';
        introOverlay.className = 'tata-intro-overlay';
        const avatarSrc = isGlassShowcase ? 'tata_avatar.jpg' : (isWebApps ? 'components/glass/tata_avatar.jpg' : 'ui/web/components/glass/tata_avatar.jpg');
        introOverlay.innerHTML = `
            <div class="tata-intro-card">
                <div class="tata-intro-avatar" style="overflow: hidden; padding: 0;">
                    <img src="${avatarSrc}" alt="Tata" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%; display: block;">
                </div>
                <h3 class="tata-intro-title">Hiiiiiii! I am Tata! ✨</h3>
                <p class="tata-intro-desc">
                    Welcome to <strong>Prototype</strong>! Should we take a quick look around all 44 glass components and web apps? Let's goooo! 🚀
                </p>
                <div class="tata-intro-actions">
                    <button type="button" class="btn-intro-secondary" id="btnIntroMyself">I'll explore myself</button>
                    <button type="button" class="btn-intro-primary" id="btnIntroGuide">Yes, let's goooo! 🚀</button>
                </div>
            </div>
        `;

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
        badge.innerHTML = `<i data-lucide="sparkles"></i> <span id="gellyPointerText">Look here</span>`;

        // 3. Companion Mascot Container (Draggable along sides)
        const companion = document.createElement('div');
        companion.id = 'gellyCompanionContainer';
        companion.className = 'gelly-companion-container dock-right';

        const canvas = document.createElement('canvas');
        canvas.id = 'gellyCanvas';
        canvas.className = 'gelly-canvas';
        canvas.width = 280;
        canvas.height = 280;
        canvas.title = "Hiii! I'm Tata. Drag me along the edge, or tap to chat!";

        const pingDot = document.createElement('div');
        pingDot.className = 'gelly-ping-dot';

        companion.appendChild(canvas);
        companion.appendChild(pingDot);

        // 4. Speech Bubble (Plain minimal header, auto progress bar, help menu)
        const bubbleWrapper = document.createElement('div');
        bubbleWrapper.id = 'gellyBubbleWrapper';
        bubbleWrapper.className = 'gelly-bubble-wrapper';

        bubbleWrapper.innerHTML = `
            <div class="gelly-bubble">
                <div class="gelly-bubble-header">
                    <div class="gelly-status-indicator">
                        <span class="gelly-badge-dot"></span>
                        <span id="gellyTourProgressText"></span>
                    </div>
                    <div class="gelly-header-tools">
                        <button type="button" class="gelly-tool-btn" id="gellySoundBtn" title="Toggle Sound">
                            <i data-lucide="${isMuted ? 'volume-x' : 'volume-2'}"></i>
                        </button>
                        <button type="button" class="gelly-tool-btn" id="gellyMinimizeBtn" title="Minimize">
                            <i data-lucide="minus"></i>
                        </button>
                        <button type="button" class="gelly-tool-btn" id="gellyCloseBtn" title="Close">
                            <i data-lucide="x"></i>
                        </button>
                    </div>
                </div>

                <div class="gelly-bubble-content">
                    <h4 class="gelly-title" id="gellyTitle">Hiii! I am Tata 👋</h4>
                    <p class="gelly-message" id="gellyMessage"></p>
                    <div class="tata-auto-progress" id="tataAutoProgress">
                        <div class="tata-auto-progress-fill" id="tataAutoProgressFill"></div>
                    </div>
                    <!-- Post-Guidance Help Menu (Populated when tour ends) -->
                    <div class="tata-help-menu" id="tataHelpMenu" style="display: none;"></div>
                </div>

                <!-- Footer with minimal single action button -->
                <div class="gelly-actions-footer" id="gellyActionsFooter">
                    <button type="button" class="gelly-btn-action primary" id="gellyMainBtn">
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
       7. SPOTLIGHT HIGHLIGHTING ENGINE (Zero Blur, Zoom-Aware)
       -------------------------------------------------------------------------- */
    let currentHighlightedElement = null;

    function highlightElement(selector, pointerText = "👉 Look here!") {
        if (!selector) {
            hideSpotlight();
            return;
        }

        const el = document.querySelector(selector);
        if (!el || window.getComputedStyle(el).display === 'none') {
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

        if (badgeText && pointerText) badgeText.innerText = pointerText;

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
       8. AUTO-ADVANCING TOUR FLOW (No Next Button, No Focus Button)
       -------------------------------------------------------------------------- */
    let isBubbleOpen = false;

    function showBubble() {
        const bubble = document.getElementById('gellyBubbleWrapper');
        const container = document.getElementById('gellyCompanionContainer');
        if (bubble) bubble.classList.add('active');
        if (container) container.classList.remove('minimized', 'has-unread');
        isBubbleOpen = true;
        updateBubblePosition();
        playSound('pop');
    }

    function hideBubble() {
        const bubble = document.getElementById('gellyBubbleWrapper');
        if (bubble) bubble.classList.remove('active');
        isBubbleOpen = false;
        clearTimeout(autoAdvanceTimer);
        clearTimeout(typewriterTimer);
        hideSpotlight();
    }

    function toggleBubble() {
        if (isBubbleOpen) hideBubble();
        else showBubble();
    }

    function renderTourStep(index) {
        clearTimeout(autoAdvanceTimer);
        clearTimeout(typewriterTimer);
        isTourActive = true;

        if (index < 0) index = 0;

        // When guidance finishes: Show helpful assistant list! Do NOT restart tour!
        if (index >= activeTourSteps.length) {
            finishTourAndShowHelpList();
            return;
        }

        currentStepIndex = index;
        const step = activeTourSteps[currentStepIndex];

        // If target element is hidden/missing, advance to next step immediately
        if (step.selector) {
            const target = document.querySelector(step.selector);
            if (!target || window.getComputedStyle(target).display === 'none') {
                renderTourStep(index + 1);
                return;
            }
        }

        currentExpression = (index % 2 === 0) ? 'happy' : 'wink';
        document.getElementById('gellyTourProgressText').innerText = `${currentStepIndex + 1}/${activeTourSteps.length}`;
        document.getElementById('gellyTitle').innerText = step.title;
        document.getElementById('tataHelpMenu').style.display = 'none';

        // Hide main button during auto-tour (NO button clutter!)
        const footer = document.getElementById('gellyActionsFooter');
        footer.style.display = 'none';

        // Trigger spotlight
        if (step.selector) {
            highlightElement(step.selector, step.pointerText);
        } else {
            hideSpotlight();
        }

        // Progress countdown bar
        const prog = document.getElementById('tataAutoProgress');
        const fill = document.getElementById('tataAutoProgressFill');
        prog.classList.add('active');
        fill.style.transition = 'none';
        fill.style.width = '0%';

        // Typewriter text
        const msgEl = document.getElementById('gellyMessage');
        playSound('pop');

        typeText(msgEl, step.message, 20, () => {
            // After typing finishes, auto-advance after delay
            const delayMs = 4500;
            fill.style.transition = `width ${delayMs}ms linear`;
            fill.style.width = '100%';

            autoAdvanceTimer = setTimeout(() => {
                renderTourStep(currentStepIndex + 1);
            }, delayMs);
        });

        showBubble();
    }

    // Post-guidance helpful menu
    function finishTourAndShowHelpList() {
        clearTimeout(autoAdvanceTimer);
        hideSpotlight();
        isTourActive = false;
        currentExpression = 'laugh';
        playSound('chime');

        document.getElementById('tataAutoProgress').classList.remove('active');
        document.getElementById('gellyTourProgressText').innerText = "All Set!";
        document.getElementById('gellyTitle').innerText = "All set! Can I help you with anything? 🌟";
        document.getElementById('gellyMessage').innerHTML = "";

        const helpMenu = document.getElementById('tataHelpMenu');
        helpMenu.innerHTML = `
            <div class="tata-help-item" data-action="copy">
                <i data-lucide="copy"></i> How to copy component code
            </div>
            ${isGlassShowcase ? `
            <div class="tata-help-item" data-action="bg">
                <i data-lucide="palette"></i> Switch to Mesh Wallpaper
            </div>
            <div class="tata-help-item" data-action="random">
                <i data-lucide="shuffle"></i> Shuffle components layout
            </div>
            ` : ''}
            <div class="tata-help-item" data-action="apps">
                <i data-lucide="layout"></i> Jump to Web Apps Studio
            </div>
            <div class="tata-help-item" data-action="bye">
                <i data-lucide="smile"></i> I'm good, thanks!
            </div>
        `;
        helpMenu.style.display = 'flex';

        const footer = document.getElementById('gellyActionsFooter');
        footer.style.display = 'none'; // Clean, no extra buttons!

        if (window.lucide) window.lucide.createIcons();

        // Bind help items
        helpMenu.querySelectorAll('.tata-help-item').forEach(item => {
            item.onclick = function () {
                const act = this.getAttribute('data-action');
                if (act === 'copy') {
                    highlightElement('.card-actions-tools, .component-card:first-of-type .card-actions-tools', "👉 Click Copy Button");
                    document.getElementById('gellyTitle').innerText = "Copy Standalone Code";
                    document.getElementById('gellyMessage').innerText = "Just click the Copy button on any card. Complete HTML, CSS, and JS is instantly copied!";
                    helpMenu.style.display = 'none';
                    footer.style.display = 'flex';
                    document.getElementById('gellyMainBtn').innerText = "Got it! 👍";
                    document.getElementById('gellyMainBtn').onclick = () => {
                        hideBubble();
                        startWanderWalk();
                    };
                } else if (act === 'bg') {
                    highlightElement('.grid-bg-selector', "👉 Theme Switcher");
                    const meshBtn = document.querySelector('.grid-bg-btn[data-bg="mesh"]');
                    if (meshBtn) meshBtn.click();
                    document.getElementById('gellyTitle').innerText = "Mesh Wallpaper";
                    document.getElementById('gellyMessage').innerText = "Enjoy the colorful ambient mesh refraction!";
                    helpMenu.style.display = 'none';
                    footer.style.display = 'flex';
                    document.getElementById('gellyMainBtn').innerText = "Looks great! 🎨";
                    document.getElementById('gellyMainBtn').onclick = () => {
                        hideBubble();
                        startWanderWalk();
                    };
                } else if (act === 'random') {
                    if (typeof window.randomizeGrid === 'function') window.randomizeGrid();
                    document.getElementById('gellyTitle').innerText = "Shuffled! 🎲";
                    document.getElementById('gellyMessage').innerText = "All cards have been randomly shuffled!";
                    helpMenu.style.display = 'none';
                    footer.style.display = 'flex';
                    document.getElementById('gellyMainBtn').innerText = "Cool! 🎲";
                    document.getElementById('gellyMainBtn').onclick = () => {
                        hideBubble();
                        startWanderWalk();
                    };
                } else if (act === 'apps') {
                    window.location.href = isGlassShowcase ? '../../apps.html' : 'ui/web/apps.html';
                } else if (act === 'bye') {
                    document.getElementById('gellyTitle').innerText = "Have fun exploring! 👋";
                    document.getElementById('gellyMessage').innerText = "I'll be right here if you need me!";
                    helpMenu.style.display = 'none';
                    setTimeout(() => {
                        hideBubble();
                        startWanderWalk(); // Automatic wander!
                    }, 1800);
                }
            };
        });
    }

    // Spontaneous casual dialogue / yapping with auto-dismiss
    let autoBanterDismissTimer = null;
    function triggerSpontaneousDialogue(isAuto = false) {
        isTourActive = false;
        hideSpotlight();
        clearTimeout(autoAdvanceTimer);
        clearTimeout(typewriterTimer);
        clearTimeout(autoBanterDismissTimer);

        const dlg = casualDialogues[dialogueIdx % casualDialogues.length];
        dialogueIdx++;

        currentExpression = dlg.expression || 'happy';
        document.getElementById('gellyTourProgressText').innerText = "";
        document.getElementById('gellyTitle').innerText = dlg.title;
        document.getElementById('tataHelpMenu').style.display = 'none';
        document.getElementById('tataAutoProgress').classList.remove('active');

        const footer = document.getElementById('gellyActionsFooter');
        footer.style.display = 'flex';
        const mainBtn = document.getElementById('gellyMainBtn');
        mainBtn.innerText = "Show me around ✨";
        mainBtn.onclick = () => renderTourStep(0);

        const msgEl = document.getElementById('gellyMessage');
        typeText(msgEl, dlg.message, 18, () => {
            if (isAuto) {
                // Auto-fade banter after 5 seconds if left untouched
                autoBanterDismissTimer = setTimeout(() => {
                    if (!isTourActive && isBubbleOpen) {
                        hideBubble();
                        startWanderWalk();
                    }
                }, 5000);
            }
        });

        showBubble();
        playSound('chime');
    }

    // Banter scheduler (Frequent banter every 8-15 seconds!)
    let banterSchedulerTimer = null;
    function scheduleNextBanter(delayMs) {
        clearTimeout(banterSchedulerTimer);
        const delay = delayMs !== undefined ? delayMs : Math.floor(8000 + Math.random() * 7000);
        banterSchedulerTimer = setTimeout(() => {
            if (!isBubbleOpen && !isTourActive && !isDragging) {
                triggerSpontaneousDialogue(true);
            }
            scheduleNextBanter();
        }, delay);
    }

    /* --------------------------------------------------------------------------
       9. RANDOM WANDERING & JIGGLE WALKING (Immediate on close/minimize)
       -------------------------------------------------------------------------- */
    let companionState = 'idle'; // 'idle', 'walking', 'returning', 'dragging'
    let walkInterval = null;

    function startWanderWalk() {
        if (companionState === 'walking' || isDragging) return;
        hideBubble();

        const container = document.getElementById('gellyCompanionContainer');
        if (!container) return;

        companionState = 'walking';
        currentExpression = 'surprised';
        container.classList.add('walking');

        // Drift gently upwards
        const randomBottom = Math.floor(140 + Math.random() * (window.innerHeight * 0.40));
        container.style.bottom = `${randomBottom}px`;

        playSound('squish');

        clearTimeout(walkInterval);
        walkInterval = setTimeout(() => {
            if (companionState === 'walking') {
                returnToHomeCorner(false);
            }
        }, 11000);
    }

    function returnToHomeCorner(byClick = true) {
        const container = document.getElementById('gellyCompanionContainer');
        if (!container) return;

        clearTimeout(walkInterval);
        companionState = 'returning';
        container.classList.remove('walking');
        container.classList.add('returning');

        container.style.bottom = '-15px';

        if (byClick) {
            currentExpression = 'wink';
            playSound('slide');
            document.getElementById('gellyTourProgressText').innerText = "";
            document.getElementById('gellyTitle').innerText = "Eep! You caught me 💨";
            document.getElementById('tataHelpMenu').style.display = 'none';
            document.getElementById('tataAutoProgress').classList.remove('active');

            const footer = document.getElementById('gellyActionsFooter');
            footer.style.display = 'flex';
            const mainBtn = document.getElementById('gellyMainBtn');
            mainBtn.innerText = "Show me around ✨";
            mainBtn.onclick = () => renderTourStep(0);

            const msgEl = document.getElementById('gellyMessage');
            typeText(msgEl, "I was just taking a slow stroll up your screen... sliding right back to my corner!", 18);
            showBubble();
        } else {
            currentExpression = 'happy';
        }

        setTimeout(() => {
            container.classList.remove('returning');
            companionState = 'idle';
        }, 1200);
    }

    function resetIdleTimer() {
        clearTimeout(idleTimer);
        // Fully randomized interval between 18s and 40s!
        const randomDelay = Math.floor(18000 + Math.random() * 22000);
        idleTimer = setTimeout(() => {
            if (companionState === 'idle' && !isBubbleOpen) {
                startWanderWalk();
            }
        }, randomDelay);
    }

    window.addEventListener('mousemove', resetIdleTimer, { passive: true });
    window.addEventListener('touchstart', resetIdleTimer, { passive: true });
    window.addEventListener('scroll', resetIdleTimer, { passive: true });

    /* --------------------------------------------------------------------------
       10. DRAG & DROP SUPPORT (Docked to screen sides)
       -------------------------------------------------------------------------- */
    let isDragging = false;
    let dragStartY = 0;
    let dragStartBottom = 0;
    let hasMoved = false;

    function initDragAndDrop() {
        const container = document.getElementById('gellyCompanionContainer');
        const canvas = document.getElementById('gellyCanvas');
        if (!container || !canvas) return;

        function startDrag(clientY) {
            if (companionState === 'walking') {
                returnToHomeCorner(true);
                return false;
            }
            isDragging = true;
            hasMoved = false;
            dragStartY = clientY;
            const rect = container.getBoundingClientRect();
            dragStartBottom = window.innerHeight - rect.bottom;
            container.classList.add('dragging');
            return true;
        }

        function moveDrag(clientX, clientY) {
            if (!isDragging) return;
            const deltaY = dragStartY - clientY;
            if (Math.abs(deltaY) > 5) hasMoved = true;

            const newBottom = Math.max(-15, Math.min(window.innerHeight - 130, dragStartBottom + deltaY));
            container.style.bottom = `${newBottom}px`;

            // Snap to left or right if dragged past halfway
            if (clientX < window.innerWidth * 0.4) {
                container.classList.add('dock-left');
                container.classList.remove('dock-right');
            } else if (clientX > window.innerWidth * 0.6) {
                container.classList.add('dock-right');
                container.classList.remove('dock-left');
            }

            updateBubblePosition();
        }

        function endDrag() {
            if (!isDragging) return;
            isDragging = false;
            container.classList.remove('dragging');
        }

        canvas.addEventListener('mousedown', (e) => {
            startDrag(e.clientY);
        });

        window.addEventListener('mousemove', (e) => {
            moveDrag(e.clientX, e.clientY);
        });

        window.addEventListener('mouseup', endDrag);

        canvas.addEventListener('touchstart', (e) => {
            if (e.touches && e.touches[0]) {
                startDrag(e.touches[0].clientY);
            }
        }, { passive: true });

        window.addEventListener('touchmove', (e) => {
            if (e.touches && e.touches[0]) {
                moveDrag(e.touches[0].clientX, e.touches[0].clientY);
            }
        }, { passive: true });

        window.addEventListener('touchend', endDrag);
    }

    function updateBubblePosition() {
        const container = document.getElementById('gellyCompanionContainer');
        const bubble = document.getElementById('gellyBubbleWrapper');
        if (!container || !bubble) return;

        const isLeft = container.classList.contains('dock-left');
        bubble.classList.toggle('dock-left', isLeft);

        const bottomVal = parseFloat(container.style.bottom) || -15;
        bubble.style.bottom = `${Math.min(window.innerHeight - 300, Math.max(80, bottomVal + 140))}px`;
    }

    /* --------------------------------------------------------------------------
       11. EVENT LISTENERS SETUP
       -------------------------------------------------------------------------- */
    function setupBubbleEvents() {
        const closeBtn = document.getElementById('gellyCloseBtn');
        const minBtn = document.getElementById('gellyMinimizeBtn');
        const soundBtn = document.getElementById('gellySoundBtn');
        const mainBtn = document.getElementById('gellyMainBtn');

        // Intro modal buttons
        const btnGuide = document.getElementById('btnIntroGuide');
        const btnMyself = document.getElementById('btnIntroMyself');
        const introOverlay = document.getElementById('tataIntroOverlay');

        // Option 1: "Yes, let's goooo! 🚀" -> Starts auto-advancing guidance
        if (btnGuide) {
            btnGuide.onclick = () => {
                introOverlay.classList.remove('active');
                localStorage.setItem('tata_site_introduced_v7', 'true');
                playSound('chime');
                setTimeout(() => {
                    renderTourStep(0);
                }, 400);
            };
        }

        // Option 2: "I'll explore myself" -> Pout disappointed reaction, then warm encouragement
        if (btnMyself) {
            btnMyself.onclick = () => {
                introOverlay.classList.remove('active');
                localStorage.setItem('tata_site_introduced_v7', 'true');
                playSound('sad');

                currentExpression = 'pout'; // Disappointed cute pout!
                document.getElementById('gellyTourProgressText').innerText = "";
                document.getElementById('gellyTitle').innerText = "Aww, okay... (｡•́︿•̀｡)";
                document.getElementById('tataHelpMenu').style.display = 'none';

                const footer = document.getElementById('gellyActionsFooter');
                footer.style.display = 'none';

                const msgEl = document.getElementById('gellyMessage');
                typeText(msgEl, "No worries! But remember, if you ever need anything, just tap me anytime! 🌟", 18, () => {
                    setTimeout(() => {
                        hideBubble();
                        startWanderWalk(); // Automatic wander immediately!
                    }, 1500);
                });

                showBubble();
            };
        }

        if (closeBtn) {
            closeBtn.onclick = () => {
                hideBubble();
                startWanderWalk(); // Walk immediately!
            };
        }

        // Minimize: NO SHRINK! Stays normal scale, and immediately starts wandering!
        if (minBtn) {
            minBtn.onclick = () => {
                hideBubble();
                const container = document.getElementById('gellyCompanionContainer');
                if (container) container.classList.add('minimized');
                playSound('squish');
                startWanderWalk(); // Walk immediately!
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

        if (mainBtn) {
            mainBtn.onclick = () => {
                if (mainBtn.innerText.includes('Show me around')) {
                    renderTourStep(0);
                } else {
                    hideBubble();
                }
            };
        }
    }

    /* --------------------------------------------------------------------------
       12. FERALUI-INSPIRED SOFT-BODY SPRING PHYSICS JELLY BLOB (Canvas 2D)
       Zero idle jiggle! Ultra-slow gentle hop when walking!
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
                    if (diff < 0.6 || Math.abs(diff - Math.PI * 2) < 0.6) p.vr += 3.0;
                });
            } else {
                isHovered = false;
            }
        });

        function handleTouch(e) {
            if (e.touches && e.touches[0]) {
                mouseScreenX = e.touches[0].clientX;
                mouseScreenY = e.touches[0].clientY;
            }
        }
        window.addEventListener('touchstart', handleTouch, { passive: true });
        window.addEventListener('touchmove', handleTouch, { passive: true });

        canvas.addEventListener('click', (e) => {
            if (hasMoved) return; // Don't trigger click if it was a drag!
            e.stopPropagation();

            if (companionState === 'walking') {
                returnToHomeCorner(true);
                return;
            }

            squashX = 1.30;
            squashY = 0.75;
            squashVx = -0.16;
            squashVy = 0.16;

            points.forEach((p) => {
                p.vr += (Math.random() - 0.5) * 14;
            });

            playSound('squish');

            const container = document.getElementById('gellyCompanionContainer');
            if (container && container.classList.contains('minimized')) {
                container.classList.remove('minimized');
                showBubble();
            } else if (!isBubbleOpen) {
                triggerSpontaneousDialogue();
            } else {
                toggleBubble();
            }
        });

        let lastTime = performance.now();

        function render(now) {
            const dt = Math.min((now - lastTime) / 1000, 0.1);
            lastTime = now;

            // ULTRA-SLOW GENTLE JIGGLE (Only active when walking!)
            if (companionState === 'walking') {
                squashY = 1 + Math.sin(now * 0.0016) * 0.09;
                squashX = 1 - Math.sin(now * 0.0016) * 0.05;
            } else {
                // Return smoothly to 1.0 and stay motionless when idle (ZERO IDLE JIGGLE!)
                const springK = 85;
                const springDamp = 8.5;

                const fx = (1 - squashX) * springK - squashVx * springDamp;
                squashVx += fx * dt;
                squashX += squashVx * dt;

                const fy = (1 - squashY) * springK - squashVy * springDamp;
                squashVy += fy * dt;
                squashY += squashVy * dt;
            }

            // Radial Spring simulation:
            // When IDLE: target is baseRadius without ANY wave! Perfectly calm and still.
            // When WALKING: super slow gentle wave.
            const pSpringK = 85;
            const pDamp = 8.0;

            points.forEach((p, i) => {
                let target = p.baseRadius;
                if (companionState === 'walking') {
                    target += Math.sin(now * 0.0016 + i * 0.6) * 2.8;
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

            // Page-Adaptive Gradient Colors
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

            // Eye & Pupil Tracking
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
                } else if (currentExpression === 'pout') {
                    ctx.scale(1, 0.65); // Slightly drooping sad eyes
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

            if (isTalking) {
                // Animated speaking mouth synchronized with typewriter!
                const talkOpen = Math.abs(Math.sin(now * 0.015)) * 6 + 3;
                ctx.beginPath();
                ctx.arc(mouthCenter.x, mouthCenter.y, talkOpen, 0, Math.PI * 2);
                ctx.fill();
            } else if (currentExpression === 'pout') {
                // Cute disappointed pout curve (｡•́︿•̀｡)
                ctx.beginPath();
                ctx.arc(mouthCenter.x, mouthCenter.y + 4, 6, 1.2 * Math.PI, 1.8 * Math.PI, false);
                ctx.stroke();
            } else if (currentExpression === 'laugh') {
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
       13. INITIALIZE ON PAGE LOAD (Fixed Single-Time Intro Across Entire Site!)
       -------------------------------------------------------------------------- */
    function init() {
        injectCompanionUI();
        setupBubbleEvents();
        initGellyPhysicsCanvas();
        initDragAndDrop();
        resetIdleTimer();
        scheduleNextBanter(3500); // Frequent banter starts within 3.5s!

        // 1. Check if first-time visitor needs the grand introduction with website blur!
        // FIXED BUG: Only shows ONCE globally across the whole website! Never re-triggers on page switch.
        const hasSeenIntro = localStorage.getItem('tata_site_introduced_v7');
        if (!hasSeenIntro) {
            const intro = document.getElementById('tataIntroOverlay');
            if (intro) {
                setTimeout(() => {
                    intro.classList.add('active');
                    playSound('chime');
                }, 350);
            }
        } else {
            // Contextual welcome without re-running the grand blur intro
            const lastPage = sessionStorage.getItem('tata_last_page');
            const isPageSwitch = lastPage && lastPage !== currentPageKey;
            sessionStorage.setItem('tata_last_page', currentPageKey);

            if (isPageSwitch) {
                setTimeout(() => {
                    triggerSpontaneousDialogue();
                }, 800);
            }
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
