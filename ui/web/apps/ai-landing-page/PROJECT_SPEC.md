# Project Specification: Kurage & ASCII Subject Variations — Cyber-Organic AI Workspace

> Ruang kerja cerdas dan landing page interaktif berbasis Glass Dark Cyber-Organic dengan 6 variasi simulasi latar belakang kanvas ASCII prosedural (Ubur-ubur, Lubang Hitam, Ikan Pari Manta, 3D Torus Knot, Naga Kosmik, dan Teratai Sakral), pergantian judul dinamis bernuansa motion blur, dan respons streaming AI mandiri.

---

## 1. Ikhtisar Proyek
- **Nama Proyek**: Kurage & ASCII Variants AI Landing Page Collection
- **File Utama**: `index.html` (Jellyfish / Kurage)
- **Tema Desain**: Glass Dark Premium & Cyber-Organic (`#05070a`, cyan glow `#4fd1c5`, lavender accent `#c4b5fd`)
- **Target Perangkat**: Responsif (Mobile 375px, Tablet 768px, Desktop 1280px+)
- **Status Produksi**: `[Interactive Prototype / Production Ready]`

---

## 2. 6 Variasi Subjek Kanvas ASCII

Setiap variasi file memiliki mesin fisika prosedural, palet warna, ikon logo pixel art, dan frasa headline dinamis yang unik:

| File Variasi | Subjek ASCII | Mesin Fisika & Matematika | Karakter Visual & Palet |
|---|---|---|---|
| [`index.html`](index.html) | **Kurage (Jellyfish)** | 4 ubur-ubur otonom dengan tentakel sinusoidal dan gelombang apung | Mint Cyan (`#5eead4`) & Lavender Indigo (`#c4b5fd`) |
| [`index-blackhole.html`](index-blackhole.html) | **Singularity (Black Hole)** | Event horizon pitch-black, cincin foton kuantum, piringan akresi Doppler beaming, & polar relativistic jets | Solar Gold (`#fde047`), Plasma Orange & Crimson Violet |
| [`index-manta.html`](index-manta.html) | **Aqualis (Manta Ray)** | Sayap pari mengepak fluida sinusoidal, tanduk sefalik, ekor bercahaya, dan kawanan 18 nanobot boids | Aqua Mint (`#2dd4bf`) & Oceanic Sapphire (`#38bdf8`) |
| [`index-torus.html`](index-torus.html) | **Tesseract (3D Torus Knot)** | Knot trefoil 3D $(p=2, q=3)$ berputar pada sumbu Pitch/Yaw/Roll dengan bayangan kedalaman voxel & pulsa soliton | Neon Fuchsia (`#f472b6`) & Cyberpunk Violet (`#c084fc`) |
| [`index-dragon.html`](index-dragon.html) | **Ryūjin (Celestial Dragon)** | Rantai kinematika terbalik 42 vertebra, kumis sutra bergelombang, dan 2 mutiara energi sakral mengorbit kepala | Mythic Jade (`#34d399`), Cyan (`#22d3ee`) & Pearl Gold |
| [`index-lotus.html`](index-lotus.html) | **Nirvana (Cyber Lotus)** | Mandala teratai 4 lapis kelopak mekar berdenyut (persamaan polar rose curve) dengan gelombang aura riak resonansi | Sakura Rose (`#fb7185`), Solar Gold & Aurora Lilac |

---

## 3. Komponen Antarmuka yang Digunakan

| Komponen | Level | Peran & Penempatan | Detail Desain & Interaksi |
|---|---|---|---|
| **Theme Switcher Modal** | Molecule | Modal pop-up (`#theme-switcher-modal`) | Grid 6 kartu variasi dengan status aktif, preview warna, dan navigasi 1-klik instan |
| **Theme Switcher Pill** | Atomic | Bar atas (`header`) | Pill status indikator variasi aktif dengan dot berkedip dan trigger modal |
| **Procedural ASCII Canvas** | Organism | Latar belakang panggung (`#kurage-canvas`) | Mesin render kanvas 2D grid 60 FPS dengan respons gravitasi kursor |
| **Morphing Hero Title** | Molecule | Bagian atas tengah (`.hero-title-wrapper`) | Animasi pergantian frasa dinamis huruf demi huruf dengan efek motion blur |
| **Kurage Glass Prompt Box** | Molecule | Pusat interaksi input (`.kurage-glass-card`) | Kartu kaca berkilau dengan textarea adaptif, pemilih model, toggle web grounding, dan haptic audio |
| **Suggestion Action Pills** | Molecule | Baris prompt instan (`.kurage-glass-pill`) | Pil aksi berkilau untuk injeksi prompt sekali sentuh |
| **Streaming Response Tray** | Organism | Area respon agen (`#response-preview`) | Animasi typewriter token demi token, sintesis status agen, bubble penalaran, dan badge referensi |
| **Cinematic Zoom Tour** | Organism | Panggung viewport (`#viewport-stage`) | Panning kamera dan zoom dinamis (00:07 - 00:10 style) untuk eksplorasi mikro-detail visual |
| **History & Shortcuts Modal** | Molecule | Dialog pop-up (`#history-modal`) | Command palette pencarian riwayat prompt dengan integrasi pintasan `Ctrl+K` |

---

## 4. Cara Menjalankan & Berganti Tema
1. Buka salah satu file (misal `index.html`) di browser secara langsung atau jalankan `npm run dev` lalu akses `http://localhost:3000/ui/web/apps/ai-landing-page/index.html`.
2. Klik tombol **Theme Switcher** di sidebar atau tombol pill **Theme** di pojok kanan atas untuk berganti subjek ASCII kapan saja.
3. Semua variasi juga dapat diakses langsung dari Web Applications Studio di [`apps.html#project-ai-landing-page`](../../apps.html#project-ai-landing-page).
