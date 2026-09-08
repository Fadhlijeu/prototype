# GlassOS UI/UX Component Ecosystem & Design Laboratory

Selamat datang di repositori laboratorium pengujian, standarisasi, dan inkubasi komponen antarmuka pengguna (UI/UX) modern.

---

## 🌟 Moto & Mindset Arsitektur

> **"Bentuk Mengikuti Fungsi, Gaya Mengikuti Identitas."**  
> *(Form follows function, style follows identity).*

Ekosistem ini memisahkan secara tegas antara **Anatomi Komponen Web Murni** (*Component Taxonomy*) dan **Lapisan Sistem Desain** (*Design System Implementation*).

---

## ⚠️ Aturan Update Dokumentasi (Wajib untuk Sesi Selanjutnya)

> **ATURAN MUTLAK BAGI AI AGENT / DEVELOPER:**  
> Setiap kali terjadi perubahan struktur folder, penambahan komponen baru, atau modifikasi style:  
> 1. **Dokumentasi Wajib Diperbarui di Langkah yang Sama**: Dilarang menunda atau memisahkan pembaruan dokumentasi ke sesi berikutnya.
> 2. **Berkas yang Wajib Diperbarui Serentak**:
>    - [component.md](file:///d:/PROJECT/prototype/component.md): Perbarui tabel pemetaan status `[stable]`, `[experimental]`, atau `[planned]`.
>    - [README.md](file:///d:/PROJECT/prototype/README.md): Perbarui struktur pohon direktori dan daftar fitur.
>    - [CHANGELOG.md](file:///d:/PROJECT/prototype/CHANGELOG.md): Catat versi dan detail perubahan.
>    - `STYLE_SPEC.md` di folder style terkait: Perbarui jika ada token CSS baru di `css.css`.

---

## 📂 Struktur Direktori Proyek (V3 Decomposed Architecture)

```text
d:\PROJECT\prototype/
├── index.html                         # Master Gateway Portal (Bebas 404 saat akses / di server lokal)
├── showcase.html                      # Master Hub / Index yang memisahkan Web Apps & Komponen
├── web-apps.html                      # Halaman Khusus Showroom Aplikasi Web Utuh (Cloud File Manager OS)
├── component.md                       # Kamus Master Taksonomi 120+ Komponen Web (100% Design-Agnostic)
├── README.md                          # Dokumentasi visi, moto, aturan update, dan arsitektur repositori
├── CHANGELOG.md                       # Catatan riwayat restrukturisasi & versi ekosistem
├── package.json                       # Script `npm start` -> `serve .`
│
└── ui/
    ├── README.md                      # UI Manifest: Konvensi penamaan & standar kualitas
    │
    ├── components/
    │   ├── raw/                       # Gaya 0: Komponen Murni Tanpa CSS (Pure Semantic HTML)
    │   │   ├── README.md              # Panduan edukasi anatomi web
    │   │   ├── showcase.html          # Showroom komponen murni
    │   │   ├── button/                # index.html, index.css, button.html
    │   │   ├── input/                 # index.html, index.css, input.html
    │   │   ├── checkbox-radio/        # index.html, index.css, checkbox-radio.html
    │   │   ├── toggle-switch/         # index.html, index.css, toggle-switch.html
    │   │   ├── select-dropdown/       # index.html, index.css, select-dropdown.html
    │   │   ├── modal-dialog/          # index.html, index.css, modal-dialog.html
    │   │   ├── table/                 # index.html, index.css, table.html
    │   │   ├── progress-meter/        # index.html, index.css, progress-meter.html
    │   │   └── details-accordion/     # index.html, index.css, details-accordion.html
    │   │
    │   └── glass/                     # Gaya 1: Glass Dark Premium
    │       ├── STYLE_SPEC.md          # Spesifikasi teknis Glass Dark Premium
    │       ├── css.css                # Master Shared CSS: Single source of truth token Glass
    │       ├── showcase.html          # Showroom 21 komponen Glass (Resize, Code, Salin)
    │       │
    │       ├── button-glass/          # [NEW] Primary, Secondary, Danger, Ghost, FAB
    │       ├── input-field-glass/     # [NEW] Text field, Password, Search, Status
    │       ├── toggle-switch-glass/   # [NEW] Glass switch dengan spring physics
    │       ├── checkbox-glass/        # [NEW] Glass checkbox interaktif
    │       ├── dropdown-select-glass/ # [NEW] Floating dropdown select menu
    │       ├── modal-dialog-glass/    # [NEW] Modal dialog pop-up tengah layar
    │       ├── toast-notification-glass/ # [NEW] Floating status toast alerts
    │       ├── tooltip-glass/         # [NEW] Micro-tooltip dengan panah
    │       ├── avatar-badge-glass/    # [NEW] Glass avatar dengan status online/busy
    │       ├── progress-bar-glass/    # [NEW] Linear glowing progress bar
    │       │
    │       ├── ai-model-selector/     # Kartu pemilih model AI (K3, Swarm, Instant)
    │       ├── thinking-effort-selector/ # Segmented control tingkat penalaran AI
    │       ├── chat-input-bar/        # Input chat bar kaca responsif
    │       ├── prompt-pills-row/      # Baris pil aksi cepat anti-potong
    │       ├── frosted-folder-card/   # Kartu folder kaca dengan siluet tab
    │       ├── aurora-storage-card/   # Kartu telemetry storage aurora mesh
    │       ├── swirl-bottom-sheet/    # Modal bottom sheet Canvas 2D swirl refraction
    │       ├── telemetry-activity-chart/ # Histogram aktivitas 12 jam interaktif
    │       ├── glass-dock-navigation/ # Dock navigasi bawah dengan spring active pill
    │       ├── glass-sidepanel/       # Panel samping produktivitas desktop
    │       └── ai-agent-scenery/      # Scenery lengkap antarmuka AI Assistant
    │
    └── file-manager_project/          # Proyek Aplikasi Komposit Utuh
        ├── index.html                 # Aplikasi Cloud File Manager mandiri
        └── PROJECT_SPEC.md            # Spesifikasi integrasi
```

---

## 🚀 Panduan Menjalankan Preview Lokal (Bebas 404)

Web server lokal **wajib dijalankan dari root direktori** (`d:\PROJECT\prototype`), BUKAN dengan menunjuk file HTML tertentu:

```bash
# Jalankan dari folder root:
npx serve .
# ATAU:
npm start
```
Buka browser di **`http://localhost:3000/`**. Halaman Gateway akan langsung terbuka dan seluruh link komponen berfungsi sempurna.
