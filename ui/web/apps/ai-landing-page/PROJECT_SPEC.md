# Project Specification: Kurage & Terrain Grid Matrix — Cyber-Organic AI Workspace

> Ruang kerja cerdas dan landing page interaktif berbasis Glass Dark Cyber-Organic dengan dua edisi visual latar belakang kanvas: **Kurage Original (ASCII Jellyfish)** dan **Grid Matrix Edition (Non-ASCII 3D Topographic Perspective Terrain & LiDAR Scan)**.

---

## 1. Ikhtisar Proyek
- **Nama Proyek**: Kurage & Grid Matrix AI Landing Page
- **File Utama**:
  - [`index.html`](index.html): **Kurage Original** (ASCII Jellyfish biological physics simulation)
  - [`index-fluid.html`](index-fluid.html): **Grid Matrix Edition** (Non-ASCII 3D Topographic Perspective Terrain wireframe, vector crosshairs, and horizontal LiDAR sweep)
- **Tema Desain**: Glass Dark Premium & Cyber-Organic (`#05070a`, cyan glow `#4fd1c5`, lavender accent `#c4b5fd`, slate `#94a3b8`)
- **Target Perangkat**: Responsif (Mobile 375px, Tablet 768px, Desktop 1280px+)
- **Status Produksi**: `[Interactive Prototype / Production Ready]`

---

## 2. Perbandingan Dua Varian Visual

| Karakteristik | Kurage Original (`index.html`) | Grid Matrix Edition (`index-fluid.html`) |
|---|---|---|
| **Paradigma Render** | Procedural ASCII Character Ramp (`.` `'` `:` `;` `o` `t` `+` `S` `X` `%` `8` `@` `#`) | Smooth 3D Perspective Vector Geometry (Pure Non-ASCII) |
| **Elemen Visual Latar Belakang** | 4 ubur-ubur biologis dengan kubah & tentakel sinusoidal | 3D Topographic Perspective Terrain Wireframe (perbukitan lembah di samping, horizon glow, koordinat telemetry langit) |
| **Interaksi Mouse** | Ripple riak lembut saat mouse mendekat | Deformasi elastis gravitasi terrain saat kursor melintas |
| **Palet Warna** | Mint Cyan & Indigo Lavender | Monokromatik Obsidian Pekat (`#05070a`), Tech Cyan (`#4fd1c5`), dan Slate Gray |
| **Tombol Glass & Teks UI** | Kartu kaca, pil aksi, greeting, prompt, shortcuts | **100% Identik & Sama Persis** dengan versi Kurage asli |

---

## 3. Komponen Antarmuka Terintegrasi

| Komponen | Level | Peran & Penempatan | Detail Desain & Interaksi |
|---|---|---|---|
| **Screen Grid Switcher Pill** | Atomic | Bar atas (`header`) | Tombol alih instan antara Kurage (ASCII) dan Grid Matrix (Non-ASCII) |
| **Procedural Canvas Engine** | Organism | Latar belakang panggung (`#kurage-canvas`) | Mesin render kanvas 2D vektor presisi 60 FPS dengan horizon LiDAR sweep |
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
   - **Grid Matrix Edition (Non-ASCII)**: [`http://localhost:3000/ui/web/apps/ai-landing-page/index-fluid.html`](http://localhost:3000/ui/web/apps/ai-landing-page/index-fluid.html)
2. Klik tombol pill **Grid Matrix Edition** / **Switch to Kurage** di bar kanan atas untuk beralih seketika antara versi original dan eksperimen non-ASCII.
