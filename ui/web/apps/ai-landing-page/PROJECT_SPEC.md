# Project Specification: Kurage & Aetheris Fluid — Cyber-Organic AI Workspace

> Ruang kerja cerdas dan landing page interaktif berbasis Glass Dark Cyber-Organic dengan dua edisi visual latar belakang kanvas: **Kurage Original (ASCII Jellyfish)** dan **Aetheris Fluid (Non-ASCII Chromatic Aurora & Quantum Particle Mesh)**.

---

## 1. Ikhtisar Proyek
- **Nama Proyek**: Kurage & Aetheris Fluid AI Landing Page
- **File Utama**:
  - [`index.html`](index.html): **Kurage Original** (ASCII Jellyfish biological physics simulation)
  - [`index-fluid.html`](index-fluid.html): **Aetheris Fluid** (Non-ASCII volumetric liquid plasma, Bézier aurora ribbons & interactive particle mesh)
- **Tema Desain**: Glass Dark Premium & Cyber-Organic (`#04060a`, cyan glow `#4fd1c5`, lavender accent `#c4b5fd`, neon magenta `#ec4899`)
- **Target Perangkat**: Responsif (Mobile 375px, Tablet 768px, Desktop 1280px+)
- **Status Produksi**: `[Interactive Prototype / Production Ready]`

---

## 2. Perbandingan Dua Varian Visual

| Karakteristik | Kurage Original (`index.html`) | Aetheris Fluid (`index-fluid.html`) |
|---|---|---|
| **Paradigma Render** | Procedural ASCII Character Ramp (`.` `'` `:` `;` `o` `t` `+` `S` `X` `%` `8` `@` `#`) | Smooth Graphical Canvas 2D (Pure Non-ASCII) |
| **Elemen Visual** | 4 ubur-ubur biologis dengan kubah & tentakel sinusoidal | 4 gumpalan plasma cair volumetrik, 3 pita gelombang aurora Bézier, & 180 partikel kuantum |
| **Interaksi Mouse** | Ripple riak lembut saat mouse mendekat | Vortex pusaran gravitasi interaktif & lenturan gelombang aurora |
| **Palet Warna** | Mint Cyan & Indigo Lavender | Prismatic Cyan, Neon Mint, Electric Violet, Rose & Amber |
| **Gaya Logo Brand** | Pixel Jellyfish Dome & Tentacles (11x11) | Quantum Orbital Rings & Cyan Core (24x24) |

---

## 3. Komponen Antarmuka Terintegrasi

| Komponen | Level | Peran & Penempatan | Detail Desain & Interaksi |
|---|---|---|---|
| **Fluid / ASCII Toggle Pill** | Atomic | Bar atas (`header`) | Tombol alih cepat antara edisi Kurage (ASCII) dan Aetheris Fluid (Non-ASCII) |
| **Procedural Canvas Engine** | Organism | Latar belakang panggung (`#kurage-canvas`) | Mesin render kanvas 2D grid 60 FPS dengan respons gravitasi kursor |
| **Morphing Hero Title** | Molecule | Bagian atas tengah (`.hero-title-wrapper`) | Animasi pergantian frasa dinamis huruf demi huruf dengan efek motion blur |
| **Kurage Glass Prompt Box** | Molecule | Pusat interaksi input (`.kurage-glass-card`) | Kartu kaca berkilau dengan textarea adaptif, pemilih model, toggle web grounding, dan haptic audio |
| **Suggestion Action Pills** | Molecule | Baris prompt instan (`.kurage-glass-pill`) | Pil aksi berkilau untuk injeksi prompt sekali sentuh |
| **Streaming Response Tray** | Organism | Area respon agen (`#response-preview`) | Animasi typewriter token demi token, sintesis status agen, bubble penalaran, dan badge referensi |
| **Cinematic Zoom Tour** | Organism | Panggung viewport (`#viewport-stage`) | Panning kamera dan zoom dinamis (00:07 - 00:10 style) untuk eksplorasi mikro-detail visual |
| **History & Shortcuts Modal** | Molecule | Dialog pop-up (`#history-modal`) | Command palette pencarian riwayat prompt dengan integrasi pintasan `Ctrl+K` |

---

## 4. Cara Menjalankan & Eksplorasi
1. Buka salah satu file di browser secara langsung atau jalankan `npm run dev` lalu akses:
   - **Kurage Original (ASCII)**: [`http://localhost:3000/ui/web/apps/ai-landing-page/index.html`](http://localhost:3000/ui/web/apps/ai-landing-page/index.html)
   - **Aetheris Fluid (Non-ASCII)**: [`http://localhost:3000/ui/web/apps/ai-landing-page/index-fluid.html`](http://localhost:3000/ui/web/apps/ai-landing-page/index-fluid.html)
2. Klik tombol pill **Fluid Edition** / **Switch to Kurage** di bar kanan atas untuk beralih seketika antara versi original dan eksperimen non-ASCII.
