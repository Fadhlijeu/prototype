# Project Specification: Kurage & AI Singularity Core — Cyber-Organic AI Workspace

> Ruang kerja cerdas dan landing page interaktif berbasis Glass Dark Cyber-Organic dengan dua edisi visual latar belakang kanvas: **Kurage Original (ASCII Jellyfish)** dan **AI Singularity Core Edition (Non-ASCII Luminescent Quantum Core & Precision Dot Matrix)**.

---

## 1. Ikhtisar Proyek
- **Nama Proyek**: Kurage & AI Singularity Core Landing Page
- **File Utama**:
  - [`index.html`](index.html): **Kurage Original** (ASCII Jellyfish biological physics simulation)
  - [`index-fluid.html`](index-fluid.html): **AI Singularity Core Edition** (Non-ASCII Luminescent Core, harmonic flux boundary, 3D orbital rings, and precision spotlight dot matrix)
- **Tema Desain**: Glass Dark Premium & Cyber-Organic (`#030508`, cyan glow `#4fd1c5`, lavender accent `#c4b5fd`, indigo `#6366f1`)
- **Target Perangkat**: Responsif (Mobile 375px, Tablet 768px, Desktop 1280px+)
- **Status Produksi**: `[Interactive Prototype / Production Ready]`

---

## 2. Research & Perbandingan Dua Varian Visual

Berdasarkan benchmark standar industri terkini (Linear, Apple Intelligence, Vercel, Raycast, Stripe):
- Menghindari pendekatan arcade retro 80s (*goofy terrain wireframe*) dan partikel pelangi berlebih (*too much / alay*).
- Menghadirkan pusat gravitasi visual berupa **Luminescent Singularity Core** yang berdenyut tenang di balik kartu kaca frosted, memberikan refraksi optik fisik nyata melalui `backdrop-filter: blur(16px)`.

| Karakteristik | Kurage Original (`index.html`) | Singularity Core Edition (`index-fluid.html`) |
|---|---|---|
| **Paradigma Render** | Procedural ASCII Character Ramp (`.` `'` `:` `;` `o` `t` `+` `S` `X` `%` `8` `@` `#`) | High-Precision Canvas 2D Vector & Radial Photonic Gradients (Pure Non-ASCII) |
| **Elemen Visual Latar Belakang** | 4 ubur-ubur biologis dengan kubah & tentakel sinusoidal ASCII | Luminescent Quantum Core + Atmospheric Corona + Harmonic Flux Ring + 3D Orbital Rings dengan energy beads |
| **Grid Latar Belakang** | Grid titik samar dasar | Precision Dot Matrix 28px dengan Dynamic Cursor Spotlight & Click Shockwave Ripples |
| **Reaktivitas Interaktif** | Reaksi sentuhan kursor riak gelombang | Tracking mouse lerp halus, gravitasi elastis ke arah kursor, dan eksitasi luminescence saat user mengetik |
| **Palet Warna** | Mint Cyan & Indigo Lavender | Obsidian Void Pekat (`#030508`), Pure White Core, Electric Teal (`#2dd4bf`), dan Deep Indigo (`#6366f1`) |
| **Tombol Glass & Teks UI** | Kartu kaca, pil aksi, greeting, prompt, shortcuts | **100% Identik & Sama Persis** dengan versi Kurage asli |

---

## 3. Komponen Antarmuka Terintegrasi

| Komponen | Level | Peran & Penempatan | Detail Desain & Interaksi |
|---|---|---|---|
| **Screen Switcher Pill** | Atomic | Bar atas (`header`) | Tombol alih instan antara Kurage (ASCII) dan Singularity Core (Non-ASCII) |
| **Singularity Canvas Engine** | Organism | Latar belakang panggung (`#kurage-canvas`) | Mesin render 60 FPS dengan peredaman lerp, refraksi kaca optik, dan gelombang shockwave |
| **Morphing Hero Title** | Molecule | Bagian atas tengah (`.hero-title-wrapper`) | Animasi pergantian frasa dinamis huruf demi huruf dengan efek motion blur |
| **Kurage Glass Prompt Box** | Molecule | Pusat interaksi input (`.kurage-glass-card`) | Kartu kaca berkilau dengan textarea adaptif, pemilih model, toggle web grounding, dan eksitasi visual inti AI |
| **Suggestion Action Pills** | Molecule | Baris prompt instan (`.kurage-glass-pill`) | Pil aksi berkilau untuk injeksi prompt sekali sentuh |
| **Streaming Response Tray** | Organism | Area respon agen (`#response-preview`) | Animasi typewriter token demi token, sintesis status agen, bubble penalaran, dan badge referensi |
| **Cinematic Zoom Tour** | Organism | Panggung viewport (`#viewport-stage`) | Panning kamera dan zoom dinamis (00:07 - 00:10 style) untuk eksplorasi mikro-detail visual |
| **History & Shortcuts Modal** | Molecule | Dialog pop-up (`#history-modal`) | Command palette pencarian riwayat prompt dengan integrasi pintasan `Ctrl+K` |

---

## 4. Cara Menjalankan & Eksplorasi
1. Buka salah satu file di browser secara langsung atau jalankan `npm run dev` lalu akses:
   - **Kurage Original (ASCII)**: [`http://localhost:3000/ui/web/apps/ai-landing-page/index.html`](http://localhost:3000/ui/web/apps/ai-landing-page/index.html)
   - **Singularity Core Edition (Non-ASCII)**: [`http://localhost:3000/ui/web/apps/ai-landing-page/index-fluid.html`](http://localhost:3000/ui/web/apps/ai-landing-page/index-fluid.html)
2. Klik tombol pill **AI Core Edition** / **Switch to Kurage** di bar kanan atas untuk beralih seketika antara versi original dan eksperimen non-ASCII.
