# Changelog — GlassOS UI/UX Component System

Seluruh perubahan penting, restrukturisasi direktori, dan dekomposisi komponen dalam repositori ini dicatat dalam berkas ini.

---

## [Version 3.4.0] — 2026-09-08

### 🎚️ Interactive Horizontal Sliders & Seamless Anti-Clipping Resolution

#### 1. Slider Horizontal Interaktif pada Toolbar Kartu & Header
- **Slider Lebar Per-Kartu**: Menambahkan kontrol slider horizontal (`<input type="range" class="card-slider-range">`) pada toolbar setiap kartu showroom ([Glass Showcase](file:///d:/PROJECT/prototype/ui/components/glass/showcase.html) dan [Raw Showcase](file:///d:/PROJECT/prototype/ui/components/raw/showcase.html)). Pengguna dapat menggeser lebar preview secara bebas dari 320px hingga 1000px dengan indikator badge pixel real-time (`Full`, `800px`, `640px`, `375px`).
- **Slider Lebar Global**: Menambahkan slider horizontal terpusat di bar kontrol atas untuk menyesuaikan lebar seluruh kartu secara serentak, lengkap dengan tombol reset instan.
- **Slider Viewport Web Apps**: Menambahkan slider horizontal pada simulator Stage View di [`web-apps.html`](file:///d:/PROJECT/prototype/web-apps.html) (skala 360px - 1440px).

#### 2. Slider Scrollbar Horizontal Terintegrasi (Bebas Konten Terpotong)
- Mengganti `overflow: hidden` pada `.card-preview-zone`, `.comp-preview-zone`, dan `.app-live-stage` menjadi `overflow-x: auto; overflow-y: hidden;` dengan styling scrollbar slider kaca gelap modern (tinggi 8px, track transparan, thumb gradien cyan-purple dengan efek glow saat hover).
- Mengatur wrapper preview dengan `flex-shrink: 0`, sehingga ketika kartu disetel ke lebar lebih besar dari kolom grid (misal 640px di kolom 380px), slider scrollbar horizontal otomatis aktif dan konten dapat digeser mulus tanpa terpotong (*zero clipping*).

#### 3. Perbaikan Total Komponen yang Sebelumnya Terpotong
- **`prompt-pills-row/`**:
  - Menghilangkan `scrollbar-width: none` dan `display: none` pada scrollbar.
  - Mengintegrasikan slider scrollbar horizontal glowing dan tombol navigasi panah geser interaktif (`<` dan `>`) untuk menggeser deretan pills dengan 1-klik.
- **`raw/table/`**:
  - Membungkus tabel dalam `.table-responsive-container` dengan scroll slider horizontal, memastikan seluruh 4 kolom (`ID`, `Component`, `Category`, `Status`) dapat diakses penuh di semua ukuran layar.
- **`glass-dock-navigation/`**:
  - Menghapus `overflow-x: hidden` dan menambahkan media query responsif (`@media (max-width: 440px)`), menjaga seluruh 4 tombol navigasi dan tombol FAB `+` tetap utuh.
- **`telemetry-activity-chart/`**, **`chat-input-bar/`**, & **`thinking-effort-selector/`**:
  - Mengoptimalkan padding pada layar kecil dan mengaktifkan horizontal scrollbar slider agar tidak ada teks, tombol kirim, atau baris metrik yang terpotong.

---

## [Version 3.3.0] — 2026-09-08

### 🛠️ Showcase Bugfixes, Grid Layout Selector, Multi-Project Web Apps Studio & Hub Deduplication

#### 1. Perbaikan Bug Layout Kartu (Gambar 1 & Gambar 2)
- **Gambar 1 (Glass Card Memanjang Kosong)**:
  - *Penyebab*: Kartu `glass-sidepanel` memiliki tinggi eksplisit 560px, sedangkan kartu lain 380px. Ketika dirender dalam CSS grid dengan `align-items: stretch`, kartu lain ditarik ke bawah menghasilkan ruang gelap kosong yang tidak terisi preview.
  - *Solusi*: Mengubah struktur pembungkus kartu menjadi flex column terpadu dengan `.card-preview-zone { flex: 1; min-height: 400px; display: flex; align-items: center; justify-content: center; background: #050508; }`. Seluruh kartu kini mengisi grid secara seragam tanpa celah kosong.
- **Gambar 2 (Raw Showcase Unstyled & Blank Terdistorsi)**:
  - *Penyebab*: Badge tag teknis pada kartu Raw merender string mentah seperti `<select> & <option>` dan `<table>, <thead>, <tbody>`. Parser HTML browser mengeksekusi tag `<select>` yang tidak tertutup, sehingga menelan sisa kartu berikutnya ke dalam dropdown, serta memicu *table foster parenting*.
  - *Solusi*: Menerapkan sanitasi `html.escape(tag)` pada generator `scripts/rebuild_all.py` dan `ui/components/raw/showcase.html`. Semua badge tag dirender aman (`&lt;select&gt;`, `&lt;table&gt;`), memulihkan tampilan 9 komponen Raw dengan sempurna.

#### 2. Fitur Pengatur Tampilan Grid (1, 2, 3, 4 Kolom & Auto)
- Menambahkan toolbar pengatur kolom interaktif pada `ui/components/glass/showcase.html` dan `ui/components/raw/showcase.html`:
  - `[ 1 ]` : Single Column View (cocok untuk inspeksi detail per komponen)
  - `[ 2 ]` : Two Column View (seimbang dan leluasa)
  - `[ 3 ]` : Three Column View (optimal pada layar widescreen)
  - `[ 4 ]` : Four Column View (tinjauan cepat padat)
  - `[ Auto ]` : Responsif fluid (`repeat(auto-fill, minmax(420px, 1fr))`)
- Pilihan pengguna disimpan secara persisten di `localStorage` per showcase.

#### 3. Eliminasi Redundansi Master Hub (`showcase.html`)
- Menghilangkan link redundan menuju `showcase.html` dari navigasi header di seluruh halaman (`index.html`, `web-apps.html`, `ui/components/glass/showcase.html`, `ui/components/raw/showcase.html`, `404.html`).
- Menjadikan `index.html` sebagai satu-satunya Master Gateway utama.
- `showcase.html` dikonfigurasi dengan pengalihan otomatis instan (0ms client-side redirect) ke `index.html`.

#### 4. Transformasi Web Applications Menjadi Multi-Project Portfolio Dinamis
- `web-apps.html` diubah dari sekadar satu spotlight demo menjadi studio multi-proyek yang merepresentasikan seluruh folder di `projects/`:
  - **Dua Aplikasi Produksi Aktif**:
    1. `Cloud File Manager OS` (v2.4) di [`projects/file-manager/`](projects/file-manager/)
    2. `AI Agent Studio` (v1.0) di [`projects/ai-studio/`](projects/ai-studio/) — interactive AI workspace lengkap dengan model switching, reasoning trace stepper, chat stream, dan Web Audio synthesizer haptik.
  - **Dua Mode Tampilan**:
    - **Stage View**: Simulator interaktif viewport Desktop, Tablet, dan Mobile dengan audio controller dan switch aplikasi.
    - **Gallery View**: Tampilan kartu portofolio berdampingan dengan live iframe preview, metadata arsitektur, dan tombol peluncur instan.
  - **Blueprint Penambahan Proyek Baru**:
    - Kartu panduan khusus `+ Tambah Proyek Web App Baru` yang menjelaskan alur pembuatan folder di `projects/<nama-proyek>/` dan pendaftaran otomatis via `scripts/rebuild_all.py`.

---

## [Version 3.2.0] — 2026-09-08

### 🚀 Elevated Root Projects Directory, CI/CD Automation & Anti-404 Resiliency

#### 1. Pemindahan Proyek Aplikasi ke Root (`projects/`)
- Memindahkan seluruh folder aplikasi web dari `ui/file-manager_project/` ke level root: [`projects/file-manager/`](file:///d:/PROJECT/prototype/projects/file-manager/).
- Menetapkan batasan arsitektur yang bersih:
  - `ui/`: Khusus untuk spesifikasi desain, token (`css.css`), dan katalog komponen modular (`ui/components/glass/`, `ui/components/raw/`).
  - `projects/`: Didedikasikan untuk aplikasi web komposit utuh yang siap pakai di tingkat produksi.
- Menambahkan [`projects/README.md`](file:///d:/PROJECT/prototype/projects/README.md) sebagai katalog portofolio aplikasi web.
- Menambahkan [`projects/TEMPLATE.md`](file:///d:/PROJECT/prototype/projects/TEMPLATE.md) sebagai blueprint cetak biru standar arsitektur untuk proyek aplikasi web baru di masa depan.

#### 2. Pencegahan 404 & Integrasi Global Favicon
- Membuat [`favicon.svg`](file:///d:/PROJECT/prototype/favicon.svg) berkualitas tinggi berbasis SVG dengan pencahayaan neon kaca gelap dan mengintegrasikannya ke seluruh berkas portal (`index.html`, `showcase.html`, `web-apps.html`, `projects/file-manager/index.html`, serta showcase komponen). Mengeliminasi request error 404 pada browser untuk `/favicon.ico`.
- Membuat [`404.html`](file:///d:/PROJECT/prototype/404.html) dengan visual glassmorphism gelap, ambient aurora blur, dan kluster navigasi satu klik ke seluruh ruang kerja penting.

#### 3. Otomatisasi GitHub Actions Deployment
- Menambahkan workflow [`.github/workflows/deploy.yml`](file:///d:/PROJECT/prototype/.github/workflows/deploy.yml) untuk melakukan auto-deploy static prototype langsung ke GitHub Pages setiap kali branch `main` diperbarui.

#### 4. Perkakas Perawatan & Sinkronisasi Repositori (`scripts/`)
- [`scripts/verify_links.py`](file:///d:/PROJECT/prototype/scripts/verify_links.py): Otomatisasi pengujian integritas 100% tautan relatif, iframe, skrip, dan style pada seluruh halaman web (82 tautan terverifikasi 0 broken link).
- [`scripts/rebuild_all.py`](file:///d:/PROJECT/prototype/scripts/rebuild_all.py): Generator master satu perintah untuk menyinkronkan seluruh database kode embedded dan tampilan showroom.
- Penambahan npm scripts di `package.json` (`npm start`, `npm run project`, `npm run showcase`, `npm run verify`, `npm run rebuild`).

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
