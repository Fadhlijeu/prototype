# Project Specification: Kurage — Cyber-Organic AI Workspace & Landing Page

> Ruang kerja cerdas dan landing page interaktif berbasis Glass Dark Cyber-Organic dengan simulasi partikel ASCII ubur-ubur prosedural, pergantian judul dinamis bernuansa motion blur, dan respons streaming AI mandiri.

---

## 1. Ikhtisar Proyek
- **Nama Proyek**: Kurage AI Landing Page & Cyber-Organic Workspace
- **File Utama**: `index.html`
- **Tema Desain**: Glass Dark Premium & Cyber-Organic (`#05070a`, cyan glow `#4fd1c5`, lavender accent `#c4b5fd`)
- **Target Perangkat**: Responsif (Mobile 375px, Tablet 768px, Desktop 1280px+)
- **Status Produksi**: `[Interactive Prototype / Production Ready]`

---

## 2. Komponen yang Digunakan

Daftar modul antarmuka dan komponen kaca yang diintegrasikan dalam aplikasi ini:

| Komponen | Level | Peran & Penempatan | Detail Desain & Interaksi |
|---|---|---|---|
| **Procedural ASCII Canvas** | Organism | Latar belakang panggung (`#kurage-canvas`) | Fisika ubur-ubur biologis otonom dengan tentakel sinusiodal, partikel apung, dan respons mouse |
| **Morphing Hero Title** | Molecule | Bagian atas tengah (`.hero-title-wrapper`) | Animasi pergantian frasa dinamis huruf demi huruf dengan efek motion blur dan specular gradient |
| **Kurage Glass Prompt Box** | Molecule | Pusat interaksi input (`.kurage-glass-card`) | Kartu kaca berkilau dengan textarea adaptif, pemilih model, toggle web grounding, dan haptic audio |
| **Suggestion Action Pills** | Molecule | Baris prompt instan (`.kurage-glass-pill`) | Pil aksi berkilau untuk injeksi prompt sekali sentuh |
| **Streaming Response Tray** | Organism | Area respon agen (`#response-preview`) | Animasi typewriter token demi token, sintesis status agen, bubble penalaran, dan badge referensi |
| **Cinematic Zoom Tour** | Organism | Panggung viewport (`#viewport-stage`) | Panning kamera dan zoom dinamis untuk eksplorasi mikro-detail visual |
| **History & Shortcuts Modal** | Molecule | Dialog pop-up (`#history-modal`) | Command palette pencarian riwayat prompt dengan integrasi pintasan `Ctrl+K` |

---

## 3. Fitur Utama & Model Data
- **Zero-Dependency Architecture**: Tidak memerlukan bundler atau server backend, berjalan langsung di peramban modern.
- **Procedural Canvas Animation**: Simulasi gelombang ubur-ubur 60 FPS murni menggunakan HTML5 Canvas 2D API.
- **Interactive State Machine**: Mendukung pemilihan model (Kurage 2.5 Flash, DeepThink Pro, CodeWave), toggle grounding web real-time, dan reset sesi obrolan.
- **Cinematic Stage Controller**: Transformasi CSS untuk showcase close-up visual panggung.
- **Audio & Haptic Feedback**: Feedback respons audio haptik saat model berpindah dan respon selesai.

---

## 4. Cara Menjalankan
Buka file `index.html` secara langsung di browser atau jalankan melalui Web Applications Studio di [`apps.html#project-ai-landing-page`](../../apps.html#project-ai-landing-page).
