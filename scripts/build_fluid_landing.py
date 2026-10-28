import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI_DIR = os.path.join(ROOT, "ui", "web", "apps", "ai-landing-page")
INDEX_PATH = os.path.join(AI_DIR, "index.html")
FLUID_PATH = os.path.join(AI_DIR, "index-fluid.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Title and Meta
content = re.sub(r"<title>.*?</title>", "<title>Aetheris — Chromatic Fluid & Neural Aurora Workspace</title>", content)

# 2. Update Brand Logo in Sidebar (Fluid Quantum Rings SVG)
fluid_logo_svg = """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" class="text-cyan-300">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-dasharray="4 2" opacity="0.6"/>
            <ellipse cx="12" cy="12" rx="9" ry="4" stroke="currentColor" transform="rotate(-30 12 12)" opacity="0.85"/>
            <ellipse cx="12" cy="12" rx="9" ry="4" stroke="currentColor" transform="rotate(30 12 12)" opacity="0.85"/>
            <circle cx="12" cy="12" r="2.5" fill="#38bdf8"/>
          </svg>"""

content = re.sub(
    r'<button id="logo-btn" title=".*?">.*?</button>',
    f'<button id="logo-btn" title="Trigger Cinematic Zoom (00:07)" class="w-9 h-9 flex items-center justify-center rounded-lg text-white/90 hover:text-white transition-transform hover:scale-105 focus:outline-none">{fluid_logo_svg}</button>',
    content,
    flags=re.DOTALL
)

# 3. Add Topbar Badge for Fluid Light Edition & Quick Switch to Kurage Original
topbar_fluid_pill = """      <!-- Version / Switcher Pill -->
      <a href="index.html" title="Kembali ke Kurage (Versi Asli)" class="kurage-glass-pill flex items-center gap-2 px-3 py-1.5 rounded-[10px] text-white/90 hover:text-white text-[12px] font-medium border border-cyan-400/30 bg-cyan-500/10 hover:bg-cyan-500/20 transition-all">
        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#38bdf8]"></span>
        <span class="font-mono-code font-semibold">Aetheris Fluid</span>
        <span class="text-white/40 text-[11px] hidden sm:inline">(Non-ASCII)</span>
        <span class="text-[10px] px-1.5 py-0.5 rounded bg-white/10 text-cyan-200 ml-1">Switch to Kurage</span>
      </a>
"""

if '<!-- Version / Switcher Pill -->' not in content:
    content = content.replace('<!-- History Button (1:1 Match) -->', f'{topbar_fluid_pill}\n      <!-- History Button (1:1 Match) -->')

# 4. Hero Phrases for Fluid Edition
fluid_phrases = """    const HERO_PHRASES = [
      { text: "synthesize chromatic ideas", accentStart: 18 },
      { text: "fluid intelligence in motion", accentStart: 19 },
      { text: "navigate generative currents", accentStart: 19 },
      { text: "seamless neural resonance", accentStart: 16 },
      { text: "what shall we create today?", accentStart: 11 }
    ];"""

content = re.sub(
    r'const HERO_PHRASES = \[.*?\];',
    fluid_phrases,
    content,
    flags=re.DOTALL
)

# 5. Non-ASCII Fluid Aurora, Plasma Metaballs & Quantum Particle Mesh Engine
FLUID_ENGINE = """
    /*************************************************************************
     * 2. NON-ASCII VOLUMETRIC LIQUID PLASMA, CHROMATIC AURORA & NEURAL MESH
     *************************************************************************/
    const canvas = document.getElementById('kurage-canvas');
    const ctx = canvas.getContext('2d', { alpha: true });

    let width = 0;
    let height = 0;
    let dpr = 1;
    let isSimulationPaused = false;
    let simTime = 0;

    let mouseX = -1000;
    let mouseY = -1000;
    let targetMouseX = -1000;
    let targetMouseY = -1000;
    let isMouseActive = false;

    window.addEventListener('mousemove', (e) => {
      targetMouseX = e.clientX;
      targetMouseY = e.clientY;
      isMouseActive = true;
    });

    window.addEventListener('mouseleave', () => {
      isMouseActive = false;
    });

    function resizeCanvas() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      initParticles();
    }

    // -----------------------------------------------------------------------
    // PARTICLE CONSTELLATION MESH (Non-ASCII, Smooth Glowing Vector Orbs)
    // -----------------------------------------------------------------------
    const PARTICLE_COUNT = 180;
    const particles = [];

    const PALETTE = [
      { r: 56,  g: 189, b: 248 }, // Cyan (#38BDF8)
      { r: 45,  g: 212, b: 191 }, // Mint Aqua (#2DD4BF)
      { r: 192, g: 132, b: 252 }, // Purple (#C084FC)
      { r: 244, g: 114, b: 182 }, // Rose Pink (#F472B6)
      { r: 253, g: 224, b: 71  }  // Amber Gold (#FDE047)
    ];

    function initParticles() {
      particles.length = 0;
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        const col = PALETTE[Math.floor(Math.random() * PALETTE.length)];
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.75,
          vy: (Math.random() - 0.5) * 0.75,
          radius: 1.2 + Math.random() * 2.2,
          baseAlpha: 0.25 + Math.random() * 0.65,
          pulseSpeed: 1 + Math.random() * 2,
          pulsePhase: Math.random() * Math.PI * 2,
          color: col
        });
      }
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // -----------------------------------------------------------------------
    // LIQUID PLASMA BLOBS (Volumetric Bioluminescent Gradient Fields)
    // -----------------------------------------------------------------------
    const BLOBS = [
      {
        baseX: 0.26, baseY: 0.32,
        radius: 280,
        speedX: 0.35, speedY: 0.42,
        r1: 6, g1: 182, b1: 212, // Cyan Core
        r2: 59, g2: 130, b2: 246  // Blue Edge
      },
      {
        baseX: 0.72, baseY: 0.38,
        radius: 310,
        speedX: 0.28, speedY: 0.36,
        r1: 168, g1: 85, b1: 247, // Violet Core
        r2: 236, g2: 72, b2: 153  // Pink Edge
      },
      {
        baseX: 0.50, baseY: 0.72,
        radius: 340,
        speedX: 0.45, speedY: 0.25,
        r1: 45,  g1: 212, b1: 191, // Mint Core
        r2: 14,  g2: 165, b2: 233  // Sky Edge
      },
      {
        baseX: 0.85, baseY: 0.78,
        radius: 240,
        speedX: 0.32, speedY: 0.48,
        r1: 244, g1: 114, b1: 182, // Rose Core
        r2: 139, g2: 92,  b2: 246  // Indigo Edge
      }
    ];

    // -----------------------------------------------------------------------
    // MAIN RENDER LOOP (60 FPS Native Canvas 2D)
    // -----------------------------------------------------------------------
    function renderLoop(timestamp) {
      if (!isSimulationPaused) {
        simTime += 0.016;
      }

      // Smooth mouse interpolation
      if (isMouseActive) {
        mouseX += (targetMouseX - mouseX) * 0.12;
        mouseY += (targetMouseY - mouseY) * 0.12;
      } else {
        mouseX = width * 0.5 + Math.sin(simTime * 0.4) * 120;
        mouseY = height * 0.5 + Math.cos(simTime * 0.5) * 80;
      }

      // 1. Clear with deep void (#04060A)
      ctx.globalCompositeOperation = 'source-over';
      ctx.fillStyle = '#04060a';
      ctx.fillRect(0, 0, width, height);

      // 2. Draw Subtle 1px Technical Grid (Matches Glass aesthetic)
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.024)';
      ctx.lineWidth = 1;
      const GRID_STEP = 44;
      ctx.beginPath();
      for (let x = 0; x <= width; x += GRID_STEP) {
        ctx.moveTo(x + 0.5, 0); ctx.lineTo(x + 0.5, height);
      }
      for (let y = 0; y <= height; y += GRID_STEP) {
        ctx.moveTo(0, y + 0.5); ctx.lineTo(width, y + 0.5);
      }
      ctx.stroke();

      // 3. Render Volumetric Liquid Plasma Blobs (Chromatic Screen Blending)
      ctx.globalCompositeOperation = 'screen';
      for (let i = 0; i < BLOBS.length; i++) {
        const b = BLOBS[i];
        const driftX = Math.sin(simTime * b.speedX + i * 1.5) * (width * 0.08);
        const driftY = Math.cos(simTime * b.speedY + i * 1.2) * (height * 0.08);
        const bx = b.baseX * width + driftX;
        const by = b.baseY * height + driftY;

        // Radial breathing expansion
        const curR = b.radius * (1 + 0.12 * Math.sin(simTime * 1.4 + i));

        const grad = ctx.createRadialGradient(bx, by, 0, bx, by, curR);
        grad.addColorStop(0, `rgba(${b.r1}, ${b.g1}, ${b.b1}, 0.28)`);
        grad.addColorStop(0.45, `rgba(${b.r2}, ${b.g2}, ${b.b2}, 0.14)`);
        grad.addColorStop(0.85, `rgba(${b.r2}, ${b.g2}, ${b.b2}, 0.03)`);
        grad.addColorStop(1, 'transparent');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(bx, by, curR, 0, Math.PI * 2);
        ctx.fill();
      }

      // 4. Render Harmonic Aurora Waves (Smooth Chromatic Bézier Ribbons)
      const WAVE_COUNT = 3;
      for (let w = 0; w < WAVE_COUNT; w++) {
        const waveBaseY = height * (0.35 + w * 0.16);
        const waveAmp = 45 + w * 20;
        const waveSpeed = 0.85 + w * 0.35;
        const phase = simTime * waveSpeed + w * 2.1;

        ctx.beginPath();
        const SEGMENTS = 12;
        const segWidth = width / SEGMENTS;
        ctx.moveTo(0, waveBaseY);

        for (let s = 0; s <= SEGMENTS; s++) {
          const sx = s * segWidth;
          const u = s / SEGMENTS;
          
          // Sine + Cosine harmonic displacement
          let sy = waveBaseY +
            Math.sin(u * 5.2 + phase) * waveAmp +
            Math.cos(u * 2.8 - phase * 0.6) * (waveAmp * 0.45);

          // Dynamic mouse wave repulsion
          const dmx = sx - mouseX;
          const dmy = sy - mouseY;
          const mDistSq = dmx * dmx + dmy * dmy;
          if (mDistSq < 45000) {
            const mFactor = (1 - mDistSq / 45000);
            sy += Math.sin(dmx * 0.05) * (40 * mFactor);
          }

          if (s === 0) {
            ctx.moveTo(sx, sy);
          } else {
            const prevX = (s - 1) * segWidth;
            const cpx = (prevX + sx) * 0.5;
            ctx.quadraticCurveTo(prevX, sy, cpx, sy);
          }
        }

        // Aurora Ribbon Stroke
        const ribbonGrad = ctx.createLinearGradient(0, 0, width, 0);
        if (w === 0) {
          ribbonGrad.addColorStop(0, 'rgba(56, 189, 248, 0.05)');
          ribbonGrad.addColorStop(0.3, 'rgba(45, 212, 191, 0.45)');
          ribbonGrad.addColorStop(0.7, 'rgba(59, 130, 246, 0.38)');
          ribbonGrad.addColorStop(1, 'rgba(168, 85, 247, 0.05)');
        } else if (w === 1) {
          ribbonGrad.addColorStop(0, 'rgba(168, 85, 247, 0.05)');
          ribbonGrad.addColorStop(0.4, 'rgba(244, 114, 182, 0.42)');
          ribbonGrad.addColorStop(0.8, 'rgba(253, 224, 71, 0.35)');
          ribbonGrad.addColorStop(1, 'rgba(45, 212, 191, 0.05)');
        } else {
          ribbonGrad.addColorStop(0, 'rgba(45, 212, 191, 0.05)');
          ribbonGrad.addColorStop(0.5, 'rgba(56, 189, 248, 0.32)');
          ribbonGrad.addColorStop(1, 'rgba(139, 92, 246, 0.05)');
        }

        ctx.strokeStyle = ribbonGrad;
        ctx.lineWidth = 2.2 + (2 - w) * 0.8;
        ctx.shadowBlur = 16;
        ctx.shadowColor = w === 0 ? 'rgba(56, 189, 248, 0.6)' : 'rgba(236, 72, 153, 0.5)';
        ctx.stroke();
        ctx.shadowBlur = 0;
      }

      // 5. Render Interactive Particle Constellation Mesh
      ctx.globalCompositeOperation = 'lighter';
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        // Update position
        p.x += p.vx + Math.sin(simTime * 0.8 + p.pulsePhase) * 0.25;
        p.y += p.vy + Math.cos(simTime * 0.6 + p.pulsePhase) * 0.25;

        // Wrap around screen edges
        if (p.x < -10) p.x = width + 10;
        if (p.x > width + 10) p.x = -10;
        if (p.y < -10) p.y = height + 10;
        if (p.y > height + 10) p.y = -10;

        // Mouse vortex / repulsive physics
        const dx = p.x - mouseX;
        const dy = p.y - mouseY;
        const distSq = dx * dx + dy * dy;
        const MOUSE_RADIUS = 150;
        if (distSq < MOUSE_RADIUS * MOUSE_RADIUS) {
          const dist = Math.sqrt(distSq) || 1;
          const force = (1 - dist / MOUSE_RADIUS) * 2.8;
          // Normal push
          p.x += (dx / dist) * force;
          p.y += (dy / dist) * force;
          // Tangential swirl
          p.x += (-dy / dist) * (force * 0.6);
          p.y += (dx / dist) * (force * 0.6);
        }

        // Pulse alpha
        const curAlpha = p.baseAlpha * (0.65 + 0.35 * Math.sin(simTime * p.pulseSpeed + p.pulsePhase));

        // Connect nearby particles with delicate laser filaments
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const cdx = p.x - p2.x;
          const cdy = p.y - p2.y;
          const connDistSq = cdx * cdx + cdy * cdy;
          const MAX_CONN_SQ = 78 * 78;

          if (connDistSq < MAX_CONN_SQ) {
            const lineAlpha = (1 - connDistSq / MAX_CONN_SQ) * 0.22 * Math.min(curAlpha, p2.baseAlpha);
            ctx.strokeStyle = `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, ${lineAlpha.toFixed(3)})`;
            ctx.lineWidth = 0.85;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }

        // Draw glowing particle orb
        ctx.fillStyle = `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, ${curAlpha.toFixed(3)})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();

        // High intensity specular core on larger particles
        if (p.radius > 2.2) {
          ctx.fillStyle = `rgba(255, 255, 255, ${(curAlpha * 0.85).toFixed(3)})`;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius * 0.45, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // 6. Interactive Mouse Glowing Cursor Aura
      if (isMouseActive) {
        const mouseGlow = ctx.createRadialGradient(mouseX, mouseY, 0, mouseX, mouseY, 110);
        mouseGlow.addColorStop(0, 'rgba(56, 189, 248, 0.24)');
        mouseGlow.addColorStop(0.5, 'rgba(168, 85, 247, 0.08)');
        mouseGlow.addColorStop(1, 'transparent');
        ctx.fillStyle = mouseGlow;
        ctx.beginPath();
        ctx.arc(mouseX, mouseY, 110, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.globalCompositeOperation = 'source-over';
      requestAnimationFrame(renderLoop);
    }
"""

# Replace Section 2 completely
pattern = r'/\*{70,}\s*\*\s*2\. PROCEDURAL ASCII.*?\n\s*/\*{70,}\s*\*\s*3\. UI INTERACTIONS'
replacement = f"{FLUID_ENGINE}\n    /*************************************************************************\n     * 3. UI INTERACTIONS"
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(FLUID_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully generated non-ASCII fluid landing page: {FLUID_PATH} ({len(content)} bytes)")
