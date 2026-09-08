# Changelog — GlassOS UI/UX Component System

Seluruh perubahan penting, restrukturisasi direktori, dan dekomposisi komponen dalam repositori ini dicatat dalam berkas ini.

---

## [Version 3.1.0] — 2026-09-08

### 💎 Showcase Standalone Restoration & Dedicated Web Applications Page

#### 1. Perbaikan Preview Iframe Standalone (Bebas Hilang Style)
- Seluruh kartu showcase (`ui/components/glass/showcase.html` dan `ui/components/raw/showcase.html`) kini memuat file **All-in-One Standalone** (`<nama>.html`) ke dalam `<iframe>`.
- Mengeliminasi masalah hilangnya styling yang diakibatkan oleh pemblokiran lintas berkas `@import url('../css.css')` oleh browser saat dibuka di mode `file:///` atau server statis.
- Tampilan 21 komponen Glass dan 9 komponen Raw HTML kini 100% konsisten, tajam, dan memancarkan efek kaca gelap aurora tanpa celah unstyled default browser.

#### 2. Tab Bar Multi-Berkas di Modal Kode ("chat.html, index.html, index.css, ..")
- Ketika pengguna menekan tombol **Kode** pada komponen mana pun, modal kini menampilkan **Top Bar File Tabs**:
  - `[komponen].html` (Versi mandiri All-in-One)
  - `index.html` (Struktur markup semantik)
  - `index.css` (Gaya spesifik komponen)
  - `index.js` (Skrip interaksi/animasi, jika ada)
  - `css.css` (Koleksi token master Glass Dark)
- Pengguna dapat beralih antar tab secara instan (0ms) dengan preview sintaks dan jumlah baris.
- Tombol **Salin File Ini** menyalin berkas yang sedang aktif di tab tersebut.
- Data di-embed menggunakan JSON data island aman (RFC 8259 solidus escape) sehingga berfungsi 100% offline dan siap pakai di lingkungan `file:///`.

#### 3. Pemisahan Aplikasi Web ke Halaman Khusus (`web-apps.html`)
- Proyek **Cloud File Manager OS** (`ui/file-manager_project/index.html`) kini dipisahkan dari tingkatan komponen atom/molekul, dan memiliki halaman showroom tersendiri: [`web-apps.html`](web-apps.html).
- Dilengkapi dengan:
  - Simulator viewport responsif: **Desktop (100% / 1280px)**, **Tablet (768px)**, dan **Mobile (375px)**.
  - Peta integrasi 12+ komponen Glass yang dirakit di dalam aplikasi.
  - Ringkasan arsitektur teknis (Web Audio Synthesizer, Canvas 2D swirl refraction, dsb.).
  - Penampil kode sumber dan dokumen spesifikasi teknis (`PROJECT_SPEC.md`).
#### 4. Pembersihan Placeholder Dummy & Gaya yang Belum Dibuat
- Menghapus seluruh opsi/teks dummy (`Neumorphism Soft`, `Cyberpunk Neon`) dari komponen dropdown (`dropdown-select-glass` dan `raw/select-dropdown`), komponen accordion (`details-accordion`), dan catatan arsitektur di `index.html`, `component.md`, dan `ui/components/raw/README.md`.
- Menggantinya dengan data realistis yang relevan dengan konteks proyek saat ini (`Personal Workspace`, `Design System Lab`, `Cloud File Manager`, `Production Archive`).

---

## [Version 3.0.0] — 2026-09-08

### 🚀 Major Architectural Overhaul & Component Decomposition

#### 1. Dekomposisi Komponen Penuh (HTML / CSS / JS / All-in-One)
- Seluruh komponen tidak lagi berupa file monolitik tunggal. Setiap komponen kini memiliki subfolder mandiri:
  - `index.html`: Markup semantik murni.
  - `index.css`: Gaya spesifik komponen yang merujuk/mengimpor `../css.css`.
  - `index.js`: Logika interaktivitas dan animasi.
  - `<nama-komponen>.html`: Versi all-in-one portabel untuk kemudahan copy-paste cepat.

#### 2. Master CSS Bersama (`ui/components/glass/css.css`)
- Diciptakan file CSS terpusat sebagai *single source of truth* untuk seluruh token desain Glass Dark Premium:
  - Variabel warna, asymmetric specular borders (`top`, `side`, `bottom`).
  - Overlay noise texture mikro SVG (`.glass-noise`).
  - Spring easing physics (`--ease-spring`).
  - Resets dan utilitas permukaan kaca (`.glass-surface`).

#### 3. Penambahan 10 Komponen Dasar Baru (Glass Design System)
Berdasarkan audit gap design system, 10 komponen dasar berikut telah dibuat lengkap secara terdekomposisi:
- `button-glass/` (Primary, Secondary, Danger, Ghost)
- `input-field-glass/` (Search, Email, Password dengan icon prefix)
- `toggle-switch-glass/` (iOS/macOS glass toggle dengan spring physics)
- `checkbox-glass/` (Glass checkbox dengan animasi centang)
- `dropdown-select-glass/` (Floating dropdown menu dengan backdrop blur)
- `modal-dialog-glass/` (Modal dialog tengah layar dengan tombol konfirmasi)
- `toast-notification-glass/` (Floating alert toast dengan status success & info)
- `tooltip-glass/` (Micro-tooltip dengan panah arah)
- `avatar-badge-glass/` (Avatar pengguna dengan indikator status online/busy)
- `progress-bar-glass/` (Progress bar linier bercahaya aurora)

Total komponen Glass kini menjadi **21 Komponen**.

#### 4. Dekomposisi Komponen Raw Unstyled (`ui/components/raw/`)
Katalog komponen murni didekomposisi ke dalam 9 subfolder terpisah:
- `button/`, `input/`, `checkbox-radio/`, `toggle-switch/`, `select-dropdown/`, `modal-dialog/`, `table/`, `progress-meter/`, `details-accordion/`.
- Dilengkapi `showcase.html` interaktif untuk mempelajari nama baku dan anatomi HTML5.

#### 5. Transformasi Showcase
- **Root `showcase.html`**: Dirombak menjadi **Master Hub & Index** yang bersih dan cepat, mengarahkan ke masing-masing showroom style.
- **`ui/components/glass/showcase.html`**: Menampilkan 21 komponen Glass dengan toolbar resize (375px/640px/Full), penampil kode sumber, dan tombol salin 1-klik.

#### 6. Resolusi Server Lokal
- Menambahkan root `index.html` (Master Gateway Hub) untuk menyelesaikan error 404 saat menjalankan `npx serve .` atau `npm start`.
