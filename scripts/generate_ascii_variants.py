import os
import sys
import json
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI_DIR = os.path.join(ROOT, "ui", "web", "apps", "ai-landing-page")
INDEX_PATH = os.path.join(AI_DIR, "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    base_html = f.read()

# Pixel Logos for each theme (11x11 viewBox)
LOGOS = {
    "jellyfish": """<svg width="22" height="22" viewBox="0 0 11 11" fill="currentColor">
            <rect x="3" y="1" width="5" height="1" /><rect x="2" y="2" width="7" height="1" /><rect x="1" y="3" width="9" height="1" /><rect x="1" y="4" width="9" height="1" /><rect x="2" y="5" width="7" height="1" />
            <rect x="2" y="6" width="1" height="2" opacity="0.85" /><rect x="4" y="6" width="1" height="3" opacity="0.95" /><rect x="6" y="6" width="1" height="4" opacity="0.95" /><rect x="8" y="6" width="1" height="2" opacity="0.85" />
            <rect x="3" y="8" width="1" height="2" opacity="0.65" /><rect x="5" y="9" width="1" height="1" opacity="0.65" /><rect x="7" y="8" width="1" height="2" opacity="0.65" />
          </svg>""",
    "blackhole": """<svg width="22" height="22" viewBox="0 0 11 11" fill="currentColor">
            <rect x="4" y="0" width="3" height="1" /><rect x="2" y="1" width="7" height="1" /><rect x="1" y="2" width="9" height="1" /><rect x="0" y="4" width="11" height="3" />
            <rect x="1" y="8" width="9" height="1" /><rect x="2" y="9" width="7" height="1" /><rect x="4" y="10" width="3" height="1" />
            <!-- Event horizon dark core -->
            <rect x="4" y="4" width="3" height="3" fill="#05070a" />
          </svg>""",
    "manta": """<svg width="22" height="22" viewBox="0 0 11 11" fill="currentColor">
            <rect x="5" y="1" width="1" height="2" /><rect x="4" y="2" width="3" height="2" />
            <rect x="0" y="4" width="11" height="1" /><rect x="1" y="5" width="9" height="1" /><rect x="2" y="6" width="7" height="1" /><rect x="4" y="7" width="3" height="1" />
            <!-- Tail -->
            <rect x="5" y="8" width="1" height="3" opacity="0.75" />
          </svg>""",
    "torus": """<svg width="22" height="22" viewBox="0 0 11 11" fill="currentColor">
            <rect x="2" y="1" width="3" height="1" /><rect x="6" y="1" width="3" height="1" />
            <rect x="1" y="2" width="2" height="2" /><rect x="8" y="2" width="2" height="2" />
            <rect x="2" y="4" width="7" height="3" fill="#05070a" /><rect x="4" y="4" width="3" height="3" />
            <rect x="1" y="7" width="2" height="2" /><rect x="8" y="7" width="2" height="2" />
            <rect x="2" y="9" width="3" height="1" /><rect x="6" y="9" width="3" height="1" />
          </svg>""",
    "dragon": """<svg width="22" height="22" viewBox="0 0 11 11" fill="currentColor">
            <rect x="2" y="1" width="2" height="1" /><rect x="7" y="1" width="2" height="1" />
            <rect x="3" y="2" width="5" height="2" /><rect x="4" y="4" width="3" height="1" />
            <rect x="2" y="5" width="7" height="1" /><rect x="3" y="6" width="5" height="1" /><rect x="4" y="7" width="3" height="2" /><rect x="5" y="9" width="1" height="2" />
          </svg>""",
    "lotus": """<svg width="22" height="22" viewBox="0 0 11 11" fill="currentColor">
            <rect x="5" y="1" width="1" height="2" /><rect x="4" y="2" width="3" height="2" />
            <rect x="2" y="4" width="7" height="1" /><rect x="1" y="5" width="9" height="2" /><rect x="2" y="7" width="7" height="1" /><rect x="3" y="8" width="5" height="1" /><rect x="5" y="9" width="1" height="1" />
          </svg>"""
}

# The 6 Themes definitions
THEMES = [
    {
        "id": "jellyfish",
        "file": "index.html",
        "title": "Kurage",
        "badge": "Jellyfish",
        "dot": "bg-teal-400",
        "tagline": "Cyber-Organic Undulating Jellyfish",
        "desc": "Simulasi 4 ubur-ubur biologis dengan tentakel sinusoidal dan gelembung partikel apung",
        "icon_bg": "bg-teal-500/20 text-teal-300",
        "accent_tint": "#c4b5fd",
        "accent_tint_deep": "#a78bfa",
        "phrases": [
            {"text": "summarize today's meetings", "accentStart": 18},
            {"text": "catch up on Slack threads", "accentStart": 18},
            {"text": "plan tomorrow's priorities", "accentStart": 16},
            {"text": "draft the weekly update", "accentStart": 17},
            {"text": "what are we working on?", "accentStart": 12}
        ]
    },
    {
        "id": "blackhole",
        "file": "index-blackhole.html",
        "title": "Singularity",
        "badge": "Black Hole",
        "dot": "bg-amber-400",
        "tagline": "Cosmic Black Hole & Accretion Vortex",
        "desc": "Lubang hitam relativistik dengan cincin foton bersinar, Doppler beaming, dan semburan jet partikel",
        "icon_bg": "bg-amber-500/20 text-amber-300",
        "accent_tint": "#fde047",
        "accent_tint_deep": "#f59e0b",
        "phrases": [
            {"text": "explore the singularity", "accentStart": 12},
            {"text": "relativistic reasoning engine", "accentStart": 13},
            {"text": "beyond the event horizon", "accentStart": 11},
            {"text": "warp space, time and knowledge", "accentStart": 17},
            {"text": "what shall we synthesize?", "accentStart": 11}
        ]
    },
    {
        "id": "manta",
        "file": "index-manta.html",
        "title": "Aqualis",
        "badge": "Manta Ray",
        "dot": "bg-cyan-400",
        "tagline": "Cybernetic Manta Ray & Nano-School",
        "desc": "Ikan pari futuristik mengepakkan sayap fluida sinusoidal diiringi 18 nanobot boid bioluminesensi",
        "icon_bg": "bg-cyan-500/20 text-cyan-300",
        "accent_tint": "#67e8f9",
        "accent_tint_deep": "#06b6d4",
        "phrases": [
            {"text": "navigate deep neural oceans", "accentStart": 14},
            {"text": "bioluminescent swarm logic", "accentStart": 14},
            {"text": "glide through latent currents", "accentStart": 14},
            {"text": "hydro-cybernetic synthesis", "accentStart": 17},
            {"text": "what shall we discover?", "accentStart": 11}
        ]
    },
    {
        "id": "torus",
        "file": "index-torus.html",
        "title": "Tesseract",
        "badge": "3D Torus Knot",
        "dot": "bg-purple-400",
        "tagline": "3D Quantum Torus Knot & Voxel Matrix",
        "desc": "Knot trefoil topologi 3D berputar kontinu dengan proyeksi kedalaman ortografis dan soliton denyut",
        "icon_bg": "bg-purple-500/20 text-purple-300",
        "accent_tint": "#f472b6",
        "accent_tint_deep": "#c084fc",
        "phrases": [
            {"text": "quantum topological thinking", "accentStart": 13},
            {"text": "hyperdimensional 3D logic", "accentStart": 17},
            {"text": "tesseract loop synthesis", "accentStart": 10},
            {"text": "continuous non-linear reasoning", "accentStart": 11},
            {"text": "what geometry shall we forge?", "accentStart": 14}
        ]
    },
    {
        "id": "dragon",
        "file": "index-dragon.html",
        "title": "Ryūjin",
        "badge": "Celestial Dragon",
        "dot": "bg-emerald-400",
        "tagline": "Bio-Serpentine Celestial Dragon Stream",
        "desc": "Naga kosmik 42 vertebra kinematika berantai dengan kumis sutra melambai dan mutiara energi sakral",
        "icon_bg": "bg-emerald-500/20 text-emerald-300",
        "accent_tint": "#34d399",
        "accent_tint_deep": "#10b981",
        "phrases": [
            {"text": "channel the dragon stream", "accentStart": 12},
            {"text": "serpentine neural flow", "accentStart": 11},
            {"text": "mythic synthetic intelligence", "accentStart": 17},
            {"text": "undulating infinite cognition", "accentStart": 11},
            {"text": "what vision shall we awaken?", "accentStart": 11}
        ]
    },
    {
        "id": "lotus",
        "file": "index-lotus.html",
        "title": "Nirvana",
        "badge": "Cyber Lotus",
        "dot": "bg-rose-400",
        "tagline": "Sacred Cyber Lotus Mandala",
        "desc": "Mandala bunga teratai fraktal 4 lapis kelopak mekar berdenyut dengan gelombang aura riak resonansi",
        "icon_bg": "bg-rose-500/20 text-rose-300",
        "accent_tint": "#fb7185",
        "accent_tint_deep": "#f472b6",
        "phrases": [
            {"text": "bloom into pure clarity", "accentStart": 11},
            {"text": "sacred geometric intelligence", "accentStart": 17},
            {"text": "fractal lotus consciousness", "accentStart": 14},
            {"text": "infinite petals of cognition", "accentStart": 16},
            {"text": "what truth shall we unfold?", "accentStart": 11}
        ]
    }
]

# 1. BLACK HOLE CANVAS CODE
CANVAS_BLACKHOLE = """
    /*************************************************************************
     * 2. PROCEDURAL ASCII BLACK HOLE (SINGULARITY) & ACCRETION VORTEX ENGINE
     *************************************************************************/
    const canvas = document.getElementById('kurage-canvas');
    const ctx = canvas.getContext('2d', { alpha: false });

    const CELL_SIZE = 13;
    const ASCII_RAMP = ['.', "'", ':', ';', 'o', 't', '+', 'S', 'X', '%', '8', '@', '#'];

    let width = 0;
    let height = 0;
    let cols = 0;
    let rows = 0;
    let dpr = 1;
    let isSimulationPaused = false;
    let simTime = 0;

    let mouseX = -1000;
    let mouseY = -1000;
    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function resizeCanvas() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cols = Math.ceil(width / CELL_SIZE);
      rows = Math.ceil(height / CELL_SIZE);
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function renderLoop(timestamp) {
      if (!isSimulationPaused) {
        simTime += 0.018;
      }

      ctx.fillStyle = '#030407';
      ctx.fillRect(0, 0, width, height);

      // Grid lines
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let c = 0; c <= cols; c++) {
        const x = c * CELL_SIZE + 0.5;
        ctx.moveTo(x, 0); ctx.lineTo(x, height);
      }
      for (let r = 0; r <= rows; r++) {
        const y = r * CELL_SIZE + 0.5;
        ctx.moveTo(0, y); ctx.lineTo(width, y);
      }
      ctx.stroke();

      const cx = width * 0.52 + Math.sin(simTime * 0.25) * 8;
      const cy = height * 0.44 + Math.cos(simTime * 0.3) * 6;
      const rEH = 62; // Event horizon radius

      ctx.font = '500 10.5px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      const diskAngle = -0.36;
      const cosD = Math.cos(diskAngle);
      const sinD = Math.sin(diskAngle);

      for (let r = 0; r < rows; r++) {
        const wy = r * CELL_SIZE + CELL_SIZE * 0.5;
        const dy = wy - cy;

        for (let c = 0; c < cols; c++) {
          const wx = c * CELL_SIZE + CELL_SIZE * 0.5;
          const dx = wx - cx;
          const distToCenter = Math.sqrt(dx * dx + dy * dy);

          if (distToCenter < rEH) {
            continue;
          }

          let density = 0;
          let cr = 245, cg = 158, cb = 11;

          // 1. Photon Sphere Ring
          const photonDist = Math.abs(distToCenter - rEH * 1.38);
          if (photonDist < 18) {
            const photonDensity = Math.pow(1 - photonDist / 18, 2) * 0.96;
            if (photonDensity > density) {
              density = photonDensity;
              cr = 254; cg = 240; cb = 138;
            }
          }

          // 2. Gravitational Lensing Arc (Light bent around top shadow)
          const arcUpperDist = Math.abs(Math.sqrt(dx * dx + (dy + 24) * (dy + 24)) - rEH * 1.9);
          if (arcUpperDist < 26) {
            const arcDensity = Math.pow(1 - arcUpperDist / 26, 1.8) * 0.78;
            if (arcDensity > density) {
              density = arcDensity;
              cr = 249; cg = 115; cb = 22;
            }
          }

          // 3. Tilted Accretion Disk (Spiral Plasma)
          const rotX = dx * cosD + dy * sinD;
          const rotY = (-dx * sinD + dy * cosD) * 2.85;
          const rDisk = Math.sqrt(rotX * rotX + rotY * rotY);

          if (rDisk >= rEH * 1.15 && rDisk <= 400) {
            const diskU = (rDisk - rEH * 1.15) / (400 - rEH * 1.15);
            const theta = Math.atan2(rotY, rotX);
            const spiral = 0.5 + 0.5 * Math.sin(theta * 2.0 - Math.log(rDisk + 1) * 4.2 + simTime * 2.8);
            const radialFalloff = Math.sin(diskU * Math.PI) * Math.pow(1 - diskU, 0.45);
            const doppler = rotX < 0 ? 1.68 : 0.54;
            const diskDensity = spiral * radialFalloff * doppler;

            if (diskDensity > density) {
              density = diskDensity;
              if (diskU < 0.35) {
                cr = 253; cg = 224; cb = 71;
              } else if (diskU < 0.72) {
                cr = 249; cg = 115; cb = 22;
              } else {
                cr = 168; cg = 85; cb = 247;
              }
            }
          }

          // 4. Polar Relativistic Particle Jets
          const jetX = Math.abs(dx * sinD - dy * cosD);
          const jetY = Math.abs(dx * cosD + dy * sinD);
          if (jetX < 34 && jetY > rEH * 0.8 && jetY < 340) {
            const jetFade = (1 - jetX / 34) * (1 - jetY / 340);
            const jetNoise = 0.5 + 0.5 * Math.sin(jetY * 0.14 - simTime * 4.4);
            const jetDensity = jetFade * jetNoise * 0.68;
            if (jetDensity > density) {
              density = jetDensity;
              cr = 192; cg = 132; cb = 252;
            }
          }

          // Mouse gravity pull
          const mdx = wx - mouseX;
          const mdy = wy - mouseY;
          if (mdx * mdx + mdy * mdy < 14000) {
            density = Math.min(1, density + 0.28);
          }

          if (density > 0.08) {
            const cellX = c * CELL_SIZE;
            const cellY = r * CELL_SIZE;
            const cellHash = ((c * 374761393 + r * 668265263) ^ Math.floor(simTime * 4)) & 0xff;
            const jitter = ((cellHash / 255) - 0.5) * 0.12;
            const dJit = Math.max(0.05, Math.min(0.999, density + jitter));

            const bgAlpha = Math.min(0.44, density * 0.38);
            ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${bgAlpha.toFixed(3)})`;
            ctx.fillRect(cellX + 1, cellY + 1, CELL_SIZE - 1, CELL_SIZE - 1);

            if (dJit > 0.84) {
              ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, 0.84)`;
              ctx.fillRect(cellX + 2, cellY + 2, CELL_SIZE - 3, CELL_SIZE - 3);
              ctx.fillStyle = '#030407';
              ctx.fillRect(cellX + 5, cellY + 5, CELL_SIZE - 9, CELL_SIZE - 9);
            } else {
              const charIndex = Math.min(ASCII_RAMP.length - 1, Math.floor(dJit * ASCII_RAMP.length));
              const glyph = ASCII_RAMP[charIndex];
              const textAlpha = Math.min(1, 0.42 + density * 0.74);
              ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${textAlpha.toFixed(3)})`;
              ctx.fillText(glyph, wx, wy + 0.5);
            }
          }
        }
      }

      // Event horizon void cutout
      ctx.fillStyle = '#020306';
      ctx.beginPath();
      ctx.arc(cx, cy, rEH - 1, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(253, 224, 71, 0.55)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      requestAnimationFrame(renderLoop);
    }
"""

# 2. MANTA RAY CANVAS CODE
CANVAS_MANTA = """
    /*************************************************************************
     * 2. PROCEDURAL ASCII MANTA RAY (AQUALIS) & OCEANIC SWARM ENGINE
     *************************************************************************/
    const canvas = document.getElementById('kurage-canvas');
    const ctx = canvas.getContext('2d', { alpha: false });

    const CELL_SIZE = 13;
    const ASCII_RAMP = ['.', "'", ':', ';', 'o', 't', '+', 'S', 'X', '%', '8', '@', '#'];

    let width = 0;
    let height = 0;
    let cols = 0;
    let rows = 0;
    let dpr = 1;
    let isSimulationPaused = false;
    let simTime = 0;

    let mouseX = -1000;
    let mouseY = -1000;
    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function resizeCanvas() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cols = Math.ceil(width / CELL_SIZE);
      rows = Math.ceil(height / CELL_SIZE);
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function sampleManta(cx, cy, heading, wingSpan, bodyLen, t, wx, wy) {
      const dx = wx - cx;
      const dy = wy - cy;
      const cosH = Math.cos(heading);
      const sinH = Math.sin(heading);
      const lx = dx * cosH + dy * sinH;
      const ly = -dx * sinH + dy * cosH;

      const halfSpan = wingSpan * 0.5;
      if (Math.abs(lx) > halfSpan || ly < -bodyLen * 0.6 || ly > bodyLen * 1.5) {
        return 0;
      }

      const flapZ = Math.sin(Math.abs(lx) * 0.024 - t * 3.4) * (Math.abs(lx) * 0.22);
      const normX = Math.abs(lx) / halfSpan;
      
      // Triangular wing profile with curved trailing edge
      const frontEdge = -bodyLen * 0.45 + normX * bodyLen * 0.35;
      const backEdge = bodyLen * 0.55 - Math.pow(normX, 1.4) * bodyLen * 0.42 + flapZ * 0.25;

      let density = 0;
      if (ly >= frontEdge && ly <= backEdge) {
        const wingDist = 1 - normX;
        const spanFalloff = Math.pow(wingDist, 0.55);
        const thickness = 1 - Math.abs(ly - (frontEdge + backEdge) * 0.5) / ((backEdge - frontEdge) * 0.55);
        density = Math.max(0, spanFalloff * Math.max(0, thickness) * 0.95);

        // Spine glow
        if (Math.abs(lx) < 22) {
          density = Math.min(1, density + 0.35 * (1 - Math.abs(lx) / 22));
        }
      }

      // Cephalic horns at snout
      if (ly < frontEdge && ly > frontEdge - 28 && Math.abs(lx) > 12 && Math.abs(lx) < 38) {
        const hornDist = 1 - (Math.abs(lx) - 25) * (Math.abs(lx) - 25) / 169;
        if (hornDist > 0) density = Math.max(density, hornDist * 0.85);
      }

      // Whip tail trailing behind
      if (ly > backEdge && ly < backEdge + 240) {
        const tailU = (ly - backEdge) / 240;
        const tailWave = Math.sin(tailU * 8.5 - t * 3.8) * (20 * tailU);
        const distToTail = Math.abs(lx - tailWave);
        if (distToTail < 9 * (1 - tailU * 0.7)) {
          const tailDensity = (1 - distToTail / (9 * (1 - tailU * 0.7))) * (1 - tailU * 0.85) * 0.85;
          density = Math.max(density, tailDensity);
        }
      }

      return Math.min(1, density);
    }

    function renderLoop(timestamp) {
      if (!isSimulationPaused) {
        simTime += 0.016;
      }

      ctx.fillStyle = '#03070d';
      ctx.fillRect(0, 0, width, height);

      // Grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let c = 0; c <= cols; c++) {
        const x = c * CELL_SIZE + 0.5;
        ctx.moveTo(x, 0); ctx.lineTo(x, height);
      }
      for (let r = 0; r <= rows; r++) {
        const y = r * CELL_SIZE + 0.5;
        ctx.moveTo(0, y); ctx.lineTo(width, y);
      }
      ctx.stroke();

      ctx.font = '500 10.5px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      // Primary Manta Center
      const m1x = width * 0.55 + Math.sin(simTime * 0.42) * 28;
      const m1y = height * 0.48 + Math.cos(simTime * 0.35) * 18;
      // Secondary Manta Center
      const m2x = width * 0.22 + Math.cos(simTime * 0.38) * 22;
      const m2y = height * 0.26 + Math.sin(simTime * 0.45) * 15;

      for (let r = 0; r < rows; r++) {
        const wy = r * CELL_SIZE + CELL_SIZE * 0.5;

        for (let c = 0; c < cols; c++) {
          const wx = c * CELL_SIZE + CELL_SIZE * 0.5;

          // Sample primary manta (large)
          let d1 = sampleManta(m1x, m1y, -0.22, 280, 190, simTime, wx, wy);
          // Sample secondary manta (smaller escort)
          let d2 = sampleManta(m2x, m2y, 0.35, 170, 115, simTime + 1.5, wx, wy);

          let density = Math.max(d1, d2);
          let cr = 45, cg = 212, cb = 191; // Mint Aqua

          // 18 Nanobot Fish Swarm (Lissajous curves)
          for (let k = 0; k < 18; k++) {
            const boidPhase = simTime * 1.8 + k * 0.42;
            const bx = m1x + Math.sin(boidPhase) * (180 + k * 8) + Math.cos(boidPhase * 0.5) * 45;
            const by = m1y + Math.cos(boidPhase * 0.8) * (90 + k * 4) + Math.sin(boidPhase * 1.2) * 35;
            const fdx = wx - bx;
            const fdy = wy - by;
            if (fdx * fdx + fdy * fdy < 95) {
              density = Math.max(density, 0.88);
              cr = 56; cg = 189; cb = 248; // Cyan swarm
            }
          }

          if (density > 0.075) {
            const cellX = c * CELL_SIZE;
            const cellY = r * CELL_SIZE;
            const cellHash = ((c * 374761393 + r * 668265263) ^ Math.floor(simTime * 3.5)) & 0xff;
            const jitter = ((cellHash / 255) - 0.5) * 0.12;
            const dJit = Math.max(0.05, Math.min(0.999, density + jitter));

            const bgAlpha = Math.min(0.42, density * 0.36);
            ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${bgAlpha.toFixed(3)})`;
            ctx.fillRect(cellX + 1, cellY + 1, CELL_SIZE - 1, CELL_SIZE - 1);

            if (dJit > 0.83) {
              ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, 0.78)`;
              ctx.fillRect(cellX + 2, cellY + 2, CELL_SIZE - 3, CELL_SIZE - 3);
              ctx.fillStyle = '#03070d';
              ctx.fillRect(cellX + 5, cellY + 5, CELL_SIZE - 9, CELL_SIZE - 9);
            } else {
              const charIndex = Math.min(ASCII_RAMP.length - 1, Math.floor(dJit * ASCII_RAMP.length));
              const glyph = ASCII_RAMP[charIndex];
              const textAlpha = Math.min(1, 0.4 + density * 0.72);
              ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${textAlpha.toFixed(3)})`;
              ctx.fillText(glyph, wx, wy + 0.5);
            }
          }
        }
      }

      requestAnimationFrame(renderLoop);
    }
"""

# 3. 3D TORUS KNOT CANVAS CODE
CANVAS_TORUS = """
    /*************************************************************************
     * 2. PROCEDURAL ASCII 3D QUANTUM TORUS KNOT (TESSERACT) ENGINE
     *************************************************************************/
    const canvas = document.getElementById('kurage-canvas');
    const ctx = canvas.getContext('2d', { alpha: false });

    const CELL_SIZE = 13;
    const ASCII_RAMP = ['.', "'", ':', ';', 'o', 't', '+', 'S', 'X', '%', '8', '@', '#'];

    let width = 0;
    let height = 0;
    let cols = 0;
    let rows = 0;
    let dpr = 1;
    let isSimulationPaused = false;
    let simTime = 0;

    let mouseX = -1000;
    let mouseY = -1000;
    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function resizeCanvas() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cols = Math.ceil(width / CELL_SIZE);
      rows = Math.ceil(height / CELL_SIZE);
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function renderLoop(timestamp) {
      if (!isSimulationPaused) {
        simTime += 0.018;
      }

      ctx.fillStyle = '#06040a';
      ctx.fillRect(0, 0, width, height);

      // Grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let c = 0; c <= cols; c++) {
        const x = c * CELL_SIZE + 0.5;
        ctx.moveTo(x, 0); ctx.lineTo(x, height);
      }
      for (let r = 0; r <= rows; r++) {
        const y = r * CELL_SIZE + 0.5;
        ctx.moveTo(0, y); ctx.lineTo(width, y);
      }
      ctx.stroke();

      const cx = width * 0.52;
      const cy = height * 0.45;
      const R = 185; // Major radius
      const r_tube = 75; // Minor radius

      // 3D Rotation angles
      const rotX = simTime * 0.45 + (mouseY - height * 0.5) * 0.0006;
      const rotY = simTime * 0.65 + (mouseX - width * 0.5) * 0.0006;
      const rotZ = simTime * 0.28;

      const cosX = Math.cos(rotX), sinX = Math.sin(rotX);
      const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
      const cosZ = Math.cos(rotZ), sinZ = Math.sin(rotZ);

      // Pre-sample 160 points on 3D trefoil knot (p=2, q=3)
      const knotPoints = [];
      const SAMPLE_COUNT = 160;
      for (let i = 0; i < SAMPLE_COUNT; i++) {
        const u = (i / SAMPLE_COUNT) * Math.PI * 2;
        // Trefoil formulas
        const x0 = (R + r_tube * Math.cos(3 * u)) * Math.cos(2 * u);
        const y0 = (R + r_tube * Math.cos(3 * u)) * Math.sin(2 * u);
        const z0 = -r_tube * Math.sin(3 * u) * 1.4;

        // Apply 3D rotation
        // 1. Rotate Y
        const x1 = x0 * cosY + z0 * sinY;
        const z1 = -x0 * sinY + z0 * cosY;
        // 2. Rotate X
        const y2 = y0 * cosX - z1 * sinX;
        const z2 = y0 * sinX + z1 * cosX;
        // 3. Rotate Z
        const x3 = x1 * cosZ - y2 * sinZ;
        const y3 = x1 * sinZ + y2 * cosZ;

        knotPoints.push({
          sx: cx + x3,
          sy: cy + y3,
          depth: z2,
          u: u
        });
      }

      ctx.font = '500 10.5px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      for (let r = 0; r < rows; r++) {
        const wy = r * CELL_SIZE + CELL_SIZE * 0.5;

        for (let c = 0; c < cols; c++) {
          const wx = c * CELL_SIZE + CELL_SIZE * 0.5;

          // Find nearest knot point in 2D
          let min2DDistSq = 999999;
          let bestPt = null;

          for (let k = 0; k < SAMPLE_COUNT; k++) {
            const p = knotPoints[k];
            const d2 = (wx - p.sx) * (wx - p.sx) + (wy - p.sy) * (wy - p.sy);
            if (d2 < min2DDistSq) {
              min2DDistSq = d2;
              bestPt = p;
            }
          }

          const tubeRadius = 24;
          if (min2DDistSq < tubeRadius * tubeRadius && bestPt) {
            const d2D = Math.sqrt(min2DDistSq);
            const tubeFalloff = 1 - d2D / tubeRadius;
            
            // Depth factor (-220 to +220 mapped to 0..1)
            const depthNorm = Math.max(0, Math.min(1, (bestPt.depth + 180) / 360));
            // Soliton pulse wave speeding along u
            const pulse = Math.exp(-Math.pow((bestPt.u - (simTime * 2.8) % (Math.PI * 2)), 2) / 0.18);
            
            const density = Math.min(1, Math.pow(tubeFalloff, 0.75) * (0.45 + depthNorm * 0.55) + pulse * 0.35);

            if (density > 0.08) {
              // Color: Electric Fuchsia (#F472B6) at front, Cyber Violet (#C084FC) in mid, Deep Indigo (#4F46E5) in back
              let cr = Math.round(79 + depthNorm * 165);
              let cg = Math.round(70 + depthNorm * 44);
              let cb = Math.round(229 + depthNorm * -47);

              const cellX = c * CELL_SIZE;
              const cellY = r * CELL_SIZE;
              const cellHash = ((c * 374761393 + r * 668265263) ^ Math.floor(simTime * 4)) & 0xff;
              const jitter = ((cellHash / 255) - 0.5) * 0.12;
              const dJit = Math.max(0.05, Math.min(0.999, density + jitter));

              const bgAlpha = Math.min(0.42, density * 0.38);
              ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${bgAlpha.toFixed(3)})`;
              ctx.fillRect(cellX + 1, cellY + 1, CELL_SIZE - 1, CELL_SIZE - 1);

              if (dJit > 0.83) {
                ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, 0.82)`;
                ctx.fillRect(cellX + 2, cellY + 2, CELL_SIZE - 3, CELL_SIZE - 3);
                ctx.fillStyle = '#06040a';
                ctx.fillRect(cellX + 5, cellY + 5, CELL_SIZE - 9, CELL_SIZE - 9);
              } else {
                const charIndex = Math.min(ASCII_RAMP.length - 1, Math.floor(dJit * ASCII_RAMP.length));
                const glyph = ASCII_RAMP[charIndex];
                const textAlpha = Math.min(1, 0.38 + density * 0.75);
                ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${textAlpha.toFixed(3)})`;
                ctx.fillText(glyph, wx, wy + 0.5);
              }
            }
          }
        }
      }

      requestAnimationFrame(renderLoop);
    }
"""

# 4. CELESTIAL DRAGON CANVAS CODE
CANVAS_DRAGON = """
    /*************************************************************************
     * 2. PROCEDURAL ASCII CELESTIAL DRAGON (RYŪJIN) STREAM ENGINE
     *************************************************************************/
    const canvas = document.getElementById('kurage-canvas');
    const ctx = canvas.getContext('2d', { alpha: false });

    const CELL_SIZE = 13;
    const ASCII_RAMP = ['.', "'", ':', ';', 'o', 't', '+', 'S', 'X', '%', '8', '@', '#'];

    let width = 0;
    let height = 0;
    let cols = 0;
    let rows = 0;
    let dpr = 1;
    let isSimulationPaused = false;
    let simTime = 0;

    let mouseX = -1000;
    let mouseY = -1000;
    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function resizeCanvas() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cols = Math.ceil(width / CELL_SIZE);
      rows = Math.ceil(height / CELL_SIZE);
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    const SEGMENT_COUNT = 42;
    const dragonSpine = [];
    for (let i = 0; i < SEGMENT_COUNT; i++) {
      dragonSpine.push({ x: 0, y: 0, angle: 0 });
    }

    function renderLoop(timestamp) {
      if (!isSimulationPaused) {
        simTime += 0.016;
      }

      ctx.fillStyle = '#030807';
      ctx.fillRect(0, 0, width, height);

      // Grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let c = 0; c <= cols; c++) {
        const x = c * CELL_SIZE + 0.5;
        ctx.moveTo(x, 0); ctx.lineTo(x, height);
      }
      for (let r = 0; r <= rows; r++) {
        const y = r * CELL_SIZE + 0.5;
        ctx.moveTo(0, y); ctx.lineTo(width, y);
      }
      ctx.stroke();

      const cx = width * 0.52;
      const cy = height * 0.46;

      // Lissajous figure-8 trajectory for dragon head
      let targetHeadX = cx + Math.cos(simTime * 0.75) * 280 + Math.sin(simTime * 1.5) * 120;
      let targetHeadY = cy + Math.sin(simTime * 0.9) * 170;

      // Blend gently to mouse if on screen
      if (mouseX > 0 && mouseX < width && mouseY > 0 && mouseY < height) {
        targetHeadX = targetHeadX * 0.4 + mouseX * 0.6;
        targetHeadY = targetHeadY * 0.4 + mouseY * 0.6;
      }

      dragonSpine[0].x = targetHeadX;
      dragonSpine[0].y = targetHeadY;

      // Kinematic inverse chain for dragon vertebrae
      const SEG_DIST = 15;
      for (let i = 1; i < SEGMENT_COUNT; i++) {
        const prev = dragonSpine[i - 1];
        const curr = dragonSpine[i];
        const dx = curr.x - prev.x;
        const dy = curr.y - prev.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const angle = Math.atan2(dy, dx);
        curr.x = prev.x + (dx / dist) * SEG_DIST;
        curr.y = prev.y + (dy / dist) * SEG_DIST;
        curr.angle = angle;
      }

      ctx.font = '500 10.5px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      // 2 Sacred Orbs orbiting the dragon head
      const orb1x = targetHeadX + Math.cos(simTime * 2.8) * 65;
      const orb1y = targetHeadY + Math.sin(simTime * 2.8) * 65;
      const orb2x = targetHeadX + Math.cos(simTime * 2.8 + Math.PI) * 65;
      const orb2y = targetHeadY + Math.sin(simTime * 2.8 + Math.PI) * 65;

      for (let r = 0; r < rows; r++) {
        const wy = r * CELL_SIZE + CELL_SIZE * 0.5;

        for (let c = 0; c < cols; c++) {
          const wx = c * CELL_SIZE + CELL_SIZE * 0.5;

          let maxDensity = 0;
          let cr = 52, cg = 211, cb = 153; // Emerald Jade

          // Check distance to dragon vertebrae
          for (let i = 0; i < SEGMENT_COUNT; i++) {
            const seg = dragonSpine[i];
            const d = Math.sqrt((wx - seg.x) * (wx - seg.x) + (wy - seg.y) * (wy - seg.y));
            // Tapered radius: 26px at neck -> 6px at tail
            const segRadius = 25 * Math.pow(1 - i / SEGMENT_COUNT, 0.65) + 5;

            if (d < segRadius) {
              const segDensity = Math.pow(1 - d / segRadius, 0.65) * 0.95;
              if (segDensity > maxDensity) {
                maxDensity = segDensity;
                // Dorsal ridge fins alternate
                if (i % 3 === 0 && d > segRadius * 0.55) {
                  cr = 34; cg = 211; cb = 238; // Cyan fin spines
                } else {
                  cr = 52; cg = 211; cb = 153; // Jade scale
                }
              }
            }
          }

          // Whiskers from head
          const head = dragonSpine[0];
          for (let w = -1; w <= 1; w += 2) {
            for (let u = 0; u < 1; u += 0.1) {
              const whiskerX = head.x - u * 80 + Math.sin(u * 6 - simTime * 4) * (14 * u);
              const whiskerY = head.y + w * (16 + u * 30) + Math.cos(u * 5 - simTime * 3) * (10 * u);
              const wd = (wx - whiskerX) * (wx - whiskerX) + (wy - whiskerY) * (wy - whiskerY);
              if (wd < 50) {
                maxDensity = Math.max(maxDensity, (1 - wd / 50) * 0.82);
                cr = 254; cg = 240; cb = 138; // Gold whisker
              }
            }
          }

          // Sacred Orbs
          const od1 = (wx - orb1x) * (wx - orb1x) + (wy - orb1y) * (wy - orb1y);
          const od2 = (wx - orb2x) * (wx - orb2x) + (wy - orb2y) * (wy - orb2y);
          if (od1 < 160 || od2 < 160) {
            const od = Math.min(od1, od2);
            maxDensity = Math.max(maxDensity, (1 - od / 160) * 0.98);
            cr = 253; cg = 224; cb = 71; // Solar Pearl
          }

          if (maxDensity > 0.08) {
            const cellX = c * CELL_SIZE;
            const cellY = r * CELL_SIZE;
            const cellHash = ((c * 374761393 + r * 668265263) ^ Math.floor(simTime * 3.8)) & 0xff;
            const jitter = ((cellHash / 255) - 0.5) * 0.12;
            const dJit = Math.max(0.05, Math.min(0.999, maxDensity + jitter));

            const bgAlpha = Math.min(0.42, maxDensity * 0.36);
            ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${bgAlpha.toFixed(3)})`;
            ctx.fillRect(cellX + 1, cellY + 1, CELL_SIZE - 1, CELL_SIZE - 1);

            if (dJit > 0.83) {
              ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, 0.82)`;
              ctx.fillRect(cellX + 2, cellY + 2, CELL_SIZE - 3, CELL_SIZE - 3);
              ctx.fillStyle = '#030807';
              ctx.fillRect(cellX + 5, cellY + 5, CELL_SIZE - 9, CELL_SIZE - 9);
            } else {
              const charIndex = Math.min(ASCII_RAMP.length - 1, Math.floor(dJit * ASCII_RAMP.length));
              const glyph = ASCII_RAMP[charIndex];
              const textAlpha = Math.min(1, 0.4 + maxDensity * 0.72);
              ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${textAlpha.toFixed(3)})`;
              ctx.fillText(glyph, wx, wy + 0.5);
            }
          }
        }
      }

      requestAnimationFrame(renderLoop);
    }
"""

# 5. CYBER LOTUS MANDALA CANVAS CODE
CANVAS_LOTUS = """
    /*************************************************************************
     * 2. PROCEDURAL ASCII SACRED CYBER LOTUS (NIRVANA) MANDALA ENGINE
     *************************************************************************/
    const canvas = document.getElementById('kurage-canvas');
    const ctx = canvas.getContext('2d', { alpha: false });

    const CELL_SIZE = 13;
    const ASCII_RAMP = ['.', "'", ':', ';', 'o', 't', '+', 'S', 'X', '%', '8', '@', '#'];

    let width = 0;
    let height = 0;
    let cols = 0;
    let rows = 0;
    let dpr = 1;
    let isSimulationPaused = false;
    let simTime = 0;

    let mouseX = -1000;
    let mouseY = -1000;
    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function resizeCanvas() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cols = Math.ceil(width / CELL_SIZE);
      rows = Math.ceil(height / CELL_SIZE);
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function renderLoop(timestamp) {
      if (!isSimulationPaused) {
        simTime += 0.016;
      }

      ctx.fillStyle = '#080407';
      ctx.fillRect(0, 0, width, height);

      // Grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let c = 0; c <= cols; c++) {
        const x = c * CELL_SIZE + 0.5;
        ctx.moveTo(x, 0); ctx.lineTo(x, height);
      }
      for (let r = 0; r <= rows; r++) {
        const y = r * CELL_SIZE + 0.5;
        ctx.moveTo(0, y); ctx.lineTo(width, y);
      }
      ctx.stroke();

      const cx = width * 0.52;
      const cy = height * 0.44;

      // 4 Petal Tiers
      const tiers = [
        { petals: 16, radius: 290, rotSpeed: 0.12, cr: 251, cg: 113, cb: 133 }, // Outer Rose
        { petals: 12, radius: 215, rotSpeed: -0.16, cr: 244, cg: 114, cb: 182 }, // Mid Sakura
        { petals: 8,  radius: 145, rotSpeed: 0.22, cr: 192, cg: 132, cb: 252 }, // Inner Lilac
        { petals: 6,  radius: 80,  rotSpeed: -0.28, cr: 253, cg: 224, cb: 71 }   // Core Solar
      ];

      // Breathing expansion cycle
      const breathe = 1 + 0.08 * Math.sin(simTime * 1.5);
      // Concentric aura shockwave ripple
      const rippleR = (simTime * 65) % 360;

      ctx.font = '500 10.5px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      for (let r = 0; r < rows; r++) {
        const wy = r * CELL_SIZE + CELL_SIZE * 0.5;
        const dy = wy - cy;

        for (let c = 0; c < cols; c++) {
          const wx = c * CELL_SIZE + CELL_SIZE * 0.5;
          const dx = wx - cx;
          const distToCenter = Math.sqrt(dx * dx + dy * dy);

          let density = 0;
          let cr = 251, cg = 113, cb = 133;

          // Golden Sacred Seed Core at center
          if (distToCenter < 34) {
            density = Math.pow(1 - distToCenter / 34, 0.7) * 0.98;
            cr = 253; cg = 224; cb = 71;
          }

          // Evaluate each petal tier
          const theta = Math.atan2(dy, dx);
          for (let i = 0; i < tiers.length; i++) {
            const tr = tiers[i];
            const curR = tr.radius * breathe;
            if (distToCenter <= curR) {
              const rotAngle = theta - simTime * tr.rotSpeed;
              // Rose curve petal equation
              const petalMod = Math.abs(Math.cos((tr.petals * rotAngle) / 2));
              const petalMaxR = curR * Math.pow(petalMod, 1.55);

              if (distToCenter <= petalMaxR) {
                const petalDistNorm = distToCenter / petalMaxR;
                const petalDensity = Math.sin(petalDistNorm * Math.PI) * Math.pow(1 - petalDistNorm, 0.28);
                if (petalDensity > density) {
                  density = petalDensity;
                  cr = tr.cr; cg = tr.cg; cb = tr.cb;
                }
              }
            }
          }

          // Concentric Aura Ripple Wave
          const rippleDiff = Math.abs(distToCenter - rippleR);
          if (rippleDiff < 14) {
            const rippleDensity = (1 - rippleDiff / 14) * 0.65;
            if (rippleDensity > density) {
              density = rippleDensity;
              cr = 251; cg = 113, cb = 133;
            }
          }

          if (density > 0.08) {
            const cellX = c * CELL_SIZE;
            const cellY = r * CELL_SIZE;
            const cellHash = ((c * 374761393 + r * 668265263) ^ Math.floor(simTime * 3.5)) & 0xff;
            const jitter = ((cellHash / 255) - 0.5) * 0.12;
            const dJit = Math.max(0.05, Math.min(0.999, density + jitter));

            const bgAlpha = Math.min(0.42, density * 0.38);
            ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${bgAlpha.toFixed(3)})`;
            ctx.fillRect(cellX + 1, cellY + 1, CELL_SIZE - 1, CELL_SIZE - 1);

            if (dJit > 0.83) {
              ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, 0.82)`;
              ctx.fillRect(cellX + 2, cellY + 2, CELL_SIZE - 3, CELL_SIZE - 3);
              ctx.fillStyle = '#080407';
              ctx.fillRect(cellX + 5, cellY + 5, CELL_SIZE - 9, CELL_SIZE - 9);
            } else {
              const charIndex = Math.min(ASCII_RAMP.length - 1, Math.floor(dJit * ASCII_RAMP.length));
              const glyph = ASCII_RAMP[charIndex];
              const textAlpha = Math.min(1, 0.4 + density * 0.72);
              ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${textAlpha.toFixed(3)})`;
              ctx.fillText(glyph, wx, wy + 0.5);
            }
          }
        }
      }

      requestAnimationFrame(renderLoop);
    }
"""

CANVAS_ENGINES = {
    "blackhole": CANVAS_BLACKHOLE,
    "manta": CANVAS_MANTA,
    "torus": CANVAS_TORUS,
    "dragon": CANVAS_DRAGON,
    "lotus": CANVAS_LOTUS
}

def generate_theme_switcher_modal(current_id):
    cards_html = ""
    for t in THEMES:
        is_active = (t["id"] == current_id)
        active_badge = '<span class="text-[10px] font-mono-code font-bold px-1.5 py-0.5 rounded bg-teal-400/20 text-teal-300 border border-teal-400/40">Active</span>' if is_active else ''
        border_cls = "border-teal-400/60 bg-teal-500/15 ring-1 ring-teal-400/30" if is_active else "border-white/10 hover:border-white/25 hover:bg-white/[0.04]"
        
        cards_html += f"""
        <a href="{t['file']}" class="kurage-glass-pill p-3 rounded-xl flex items-start gap-3 border {border_cls} transition-all hover:scale-[1.02] block text-left group">
          <div class="w-8 h-8 rounded-lg {t['icon_bg']} flex items-center justify-center flex-shrink-0 mt-0.5 font-bold font-mono-code text-xs">
            {t['title'][:2]}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between gap-1 mb-0.5">
              <h4 class="text-[13px] font-semibold text-white group-hover:text-teal-200 transition-colors truncate">{t['title']} <span class="text-[11px] text-white/40 font-normal">({t['badge']})</span></h4>
              {active_badge}
            </div>
            <p class="text-[11px] text-white/55 line-clamp-2 leading-tight">{t['desc']}</p>
          </div>
        </a>"""

    modal_html = f"""
  <!-- ASCII Theme Variations Switcher Modal -->
  <div id="theme-switcher-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md hidden transition-opacity">
    <div class="kurage-glass-card w-[94%] max-w-[620px] p-5 sm:p-6 rounded-2xl relative border border-white/15 shadow-[0_25px_70px_rgba(0,0,0,0.85)] max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-3.5 mb-4 border-b border-white/10">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-teal-500/20 border border-teal-500/30 flex items-center justify-center text-teal-300">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1 1.275-1.275L12 3Z"/></svg>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-white">ASCII Subject Variations (6 Themes)</h3>
            <p class="text-[11px] text-white/50">Pilih simulasi latar belakang prosedural kanvas favorit Anda</p>
          </div>
        </div>
        <button onclick="toggleThemeSwitcherModal()" class="w-7 h-7 rounded-lg flex items-center justify-center text-white/50 hover:text-white hover:bg-white/10 transition-all">✕</button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
{cards_html}
      </div>

      <div class="mt-4 pt-3 border-t border-white/10 flex items-center justify-between text-[11px] text-white/45">
        <span>Tekan tombol di sidebar / topbar untuk membuka switcher kapan saja</span>
        <button onclick="toggleThemeSwitcherModal()" class="text-teal-300 hover:underline">Tutup</button>
      </div>
    </div>
  </div>
"""
    return modal_html

def build_file_content(theme_meta):
    t_id = theme_meta["id"]
    content = base_html

    # 1. Title tag
    content = re.sub(r"<title>.*?</title>", f"<title>{theme_meta['title']} — {theme_meta['tagline']}</title>", content)

    # 2. Sidebar logo
    logo_svg = LOGOS.get(t_id, LOGOS["jellyfish"])
    content = re.sub(
        r'<button id="logo-btn" title=".*?">.*?</button>',
        f'<button id="logo-btn" title="Trigger Cinematic Zoom (00:07)" class="w-9 h-9 flex items-center justify-center rounded-lg text-white/90 hover:text-white transition-transform hover:scale-105 focus:outline-none">{logo_svg}</button>',
        content,
        flags=re.DOTALL
    )

    # 3. Sidebar: Add Theme Switcher button
    theme_btn_sidebar = """
        <!-- Theme Switcher Icon -->
        <button onclick="toggleThemeSwitcherModal()" title="Switch ASCII Subject (6 Themes)" class="w-[34px] h-[34px] rounded-[9px] flex items-center justify-center text-teal-300 bg-teal-400/10 border border-teal-400/25 hover:bg-teal-400/20 transition-all hover:scale-105">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
          </svg>
        </button>"""
    if 'id="theme-switcher-btn"' not in content:
        content = content.replace('<!-- Activity / Waveform Pulse Icon -->', f'{theme_btn_sidebar}\n\n        <!-- Activity / Waveform Pulse Icon -->')

    # 4. Topbar: Add Theme Pill next to History button
    theme_pill_topbar = f"""      <!-- Theme Switcher Pill -->
      <button onclick="toggleThemeSwitcherModal()" class="kurage-glass-pill flex items-center gap-2 px-3 py-1.5 rounded-[10px] text-white/90 hover:text-white text-[12px] font-medium border border-teal-400/30 bg-teal-500/10 hover:bg-teal-500/20 transition-all">
        <span class="w-2 h-2 rounded-full {theme_meta['dot']} animate-pulse"></span>
        <span class="font-mono-code font-semibold">{theme_meta['title']}</span>
        <span class="text-white/40 text-[11px] hidden sm:inline">({theme_meta['badge']})</span>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="text-white/60"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
"""
    if '<!-- Theme Switcher Pill -->' not in content:
        content = content.replace('<!-- History Button (1:1 Match) -->', f'{theme_pill_topbar}\n      <!-- History Button (1:1 Match) -->')

    # 5. Hero phrases
    phrases_json = json.dumps(theme_meta["phrases"], indent=6)
    content = re.sub(
        r'const HERO_PHRASES = \[.*?\];',
        f'const HERO_PHRASES = {phrases_json};',
        content,
        flags=re.DOTALL
    )

    # 6. Replace Canvas Engine if not jellyfish
    if t_id in CANVAS_ENGINES:
        # Replace Section 2 completely
        pattern = r'/\*{70,}\s*\*\s*2\. PROCEDURAL ASCII.*?\n\s*/\*{70,}\s*\*\s*3\. UI INTERACTIONS'
        replacement = f"{CANVAS_ENGINES[t_id]}\n    /*************************************************************************\n     * 3. UI INTERACTIONS"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 7. Add Modal before toast
    modal_html = generate_theme_switcher_modal(t_id)
    if 'id="theme-switcher-modal"' not in content:
        content = content.replace('<!-- Subtle Notification Toast -->', f'{modal_html}\n  <!-- Subtle Notification Toast -->')

    # 8. Add JS handler for modal
    switcher_js = """
    function toggleThemeSwitcherModal() {
      const modal = document.getElementById('theme-switcher-modal');
      if (modal) modal.classList.toggle('hidden');
    }
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const modal = document.getElementById('theme-switcher-modal');
        if (modal && !modal.classList.contains('hidden')) {
          modal.classList.add('hidden');
        }
      }
    });
"""
    if 'function toggleThemeSwitcherModal()' not in content:
        content = content.replace('function toggleHistoryModal() {', f'{switcher_js}\n    function toggleHistoryModal() {{')

    return content

# Generate all 6 files
for t in THEMES:
    file_path = os.path.join(AI_DIR, t["file"])
    output_html = build_file_content(t)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(output_html)
    print(f"Generated: {t['file']} ({t['title']}) - {len(output_html)} bytes")

print("All 6 ASCII variant files generated successfully!")
