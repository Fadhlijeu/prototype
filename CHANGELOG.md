# Changelog — GlassOS UI/UX Component System

Seluruh perubahan penting, restrukturisasi direktori, dan dekomposisi komponen dalam repositori ini dicatat dalam berkas ini.

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
