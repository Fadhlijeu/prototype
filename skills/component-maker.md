# Agent Skill: Component Maker (Anti-Dummy & Mass Creation Framework)

> **Standard Operating Procedure (SOP) Pembuatan Komponen Kaca Glass Dark Premium**  
> Panduan wajib bagi AI Agent dan developer saat merancang, memproduksi, atau menambahkan batch komponen UI baru (misalnya 20–40 komponen) tanpa kontrol dummy artifisial, tanpa placeholder tidak jelas, dan tanpa AI slop.

---

## 🚫 1. Anti-Dummy Creed (Deklarasi Anti-AI-Slop)

Kesalahan paling umum dari generasi AI adalah menambahkan elemen kontrol buatan (*artificial dummy controls*) atau dekorasi mubazir di luar batas komponen utama hanya untuk memicu animasi. **Hal ini dilarang keras.**

### Katalog Elemen Terlarang (*Hard Ban List*):

| Jenis Elemen Terlarang | Contoh Nyata yang Dihapus | Alasan Dilarang | Solusi Benar yang Diwajibkan |
|---|---|---|---|
| **Slider Simulasi Eksternal** | Baris `Simulate Battery Level: [---O---]` di bawah widget baterai. | Merusak kemurnian komponen, memperlihatkan tanda "prototype mainan/AI slop". | Komponen baterai beroperasi otonom via telemetry update realistis di background. |
| **Tombol Stepper Artifisial** | Tombol `[-10%]`, `[Auto Pulse]`, `[+10%]` di bawah circular progress. | Membebani UI dengan kontrol yang tidak ada di dashboard nyata. | Gauge radial hidup secara mandiri atau merespons drag/klik langsung. |
| **Hint Pills / Teks Melayang** | Teks `Click center button to bloom radial actions` atau `ACTIVE WORKSPACE NAVIGATION`. | Clutter visual. UI modern menggunakan affordance visual, bukan instruksi teks melayang. | Gunakan icon plus berputar, cursor pointer, dan hover glow natural. |
| **Pill Telemetri Tidak Relevan** | Baris `[Latency: 21ms] [Enclave: Active] [Mode: Berpikir]` di bawah avatar card. | Menempelkan badge yang tidak relevan dengan identitas profil pengguna. | Fokus pada identitas profil, online dot, role tag, dan avatar stack swarm. |
| **Tombol Proxy untuk 3D Object** | Tombol `[Flip Card (CVV)]` terpisah di bawah kartu kredit 3D. | Redundan. Objek 3D harus intuitif dapat diklik langsung untuk membalik. | Jadikan kartu itu sendiri interaktif (`scene.addEventListener('click')`). |
| **Tombol Gimmick Navigasi** | Tombol `[🔀 Acak]` di filter tab showcase. | Mengganggu hierarki kategori dan tata letak grid. | Biarkan pengguna memilih kategori dengan bersih tanpa tombol acak. |
| **Placeholder Teks Generik** | Teks `Lorem Ipsum`, `Card Title`, `Description goes here...`. | Terkesan malas dan tidak mencerminkan kasus penggunaan nyata. | Gunakan copy kontekstual produksi: "Nexus Platinum", "4.28 V", "99.98% Uptime". |

---

## 🎨 2. Batch Creation Framework (Prosedur 20–40 Komponen Baru)

Ketika pengguna meminta:
> *"Sekarang saya minta kamu tambahkan 20-40 komponen baru terserah apa saja, randomize, design bervariasi dan kreatif, animasi, transisi baik, tapi tetap glass. Dan ingat, tidak ada dummy, tidak ada placeholder tidak jelas, tidak AI slop... Kali ini saya minta tidak serupa..."*

Patuhi alur kerja terstruktur ini:

### A. Matriks Diferensiasi Radikal (Anti-Repetisi)
Jika diminta membuat komponen dari kategori yang sudah ada, **DILARANG** membuat variasi minor (misal: dropdown hanya diganti warna atau teksnya). Ubah arsitektur dan model interaksinya:

1. **Kategori Dropdown & Selectors**:
   - Bukan dropdown list biasa lagi, melainkan:
     - **Command Palette (Ctrl+K Modal Select)** dengan fuzzy search & shortcut chip.
     - **Hierarchical Tree-View Select** dengan expandable nested folders.
     - **Floating Orbital Segmented Wheel** untuk pemilihan mode radial.
2. **Kategori Cards**:
   - Bukan sekadar stat card biasa, melainkan:
     - **Interactive Audio Waveform Card** dengan scrubber dan time-code.
     - **Live Terminal Log Stream Card** dengan auto-scroll dan level badge.
     - **Dual-Pane Comparison Glass Card** dengan sliding divider.
3. **Kategori Form & Inputs**:
   - Bukan form input teks biasa, melainkan:
     - **Token / Tag Multi-Pill Input** dengan autokomplit dan chip dismiss.
     - **Syntax-Highlighted Markdown Textarea** dengan glass quick-toolbar.
     - **Biometric FaceID / Passkey Authentication Pad**.
4. **Kategori Gauges & Loaders**:
   - Bukan progress bar datar, melainkan:
     - **Multi-Thread CPU Core Grid Gauge** (8-core telemetry display).
     - **Biometric Fingerprint Scanner** dengan laser scanning line animasi.

---

## 🏗️ 3. Arsitektur Berkas Wajib (The 4-File Pattern)

Setiap komponen baru dibuat di `ui/web/components/glass/<kebab-name>/` dan wajib memiliki 4 berkas:

```text
ui/web/components/glass/<kebab-name>/
├── index.html            # Markup semantik bersih (memuat css.css, index.css, index.js)
├── index.css             # Stylesheet khusus komponen (scoped classes, zero leak)
├── index.js              # Logika interaksi murni & autonomous state
└── <kebab-name>.html     # Versi All-in-One mandiri (self-contained untuk preview)
```

### Standar Teknis Tiap Berkas:
1. **`index.html`**:
   - Memuat token global: `<link rel="stylesheet" href="../css.css">`.
   - Memuat style lokal: `<link rel="stylesheet" href="index.css">`.
   - Menggunakan Lucide icons: `<script src="https://unpkg.com/lucide@latest"></script>`.
   - Memuat script lokal di akhir body: `<script src="index.js"></script>`.
2. **`index.css`**:
   - Baris pertama: `@import url('../css.css');`.
   - Nama class ter-namespace: `.<kebab-name>-*`.
   - Specular border asimetris:
     ```css
     border: 1px solid transparent;
     border-top-color: var(--glass-border-top, rgba(255, 255, 255, 0.28));
     border-left-color: var(--glass-border-side, rgba(255, 255, 255, 0.12));
     border-right-color: var(--glass-border-side, rgba(255, 255, 255, 0.12));
     border-bottom-color: var(--glass-border-bottom, rgba(255, 255, 255, 0.04));
     ```
   - Backdrop blur standar: `backdrop-filter: blur(24px) saturate(160%);`.
3. **`index.js`**:
   - Gunakan `addEventListener`, dukung keyboard aksesibilitas (`Enter`, `Space`, `Escape`).
   - Jika visual telemetry, gunakan `setInterval` halus dengan fluktuasi data realistis.
4. **`<kebab-name>.html`**:
   - Versi All-in-One mandiri yang menggabungkan seluruh CSS dan JS untuk iframe preview di showcase.

---

## 🔍 4. Protokol Quality Assurance (QA) Wajib

Sebelum menyatakan pekerjaan selesai kepada pengguna, AI Agent **wajib** melakukan verifikasi berikut:

1. **Audit Visual & Kode Anti-Dummy**:
   - Periksa apakah ada tombol "Simulate", slider simulator, atau tombol trigger eksternal. Jika ada, **hapus segera**.
   - Periksa apakah ada teks instruksi melayang ("Click here..."). Jika ada, **hapus segera**.
2. **Registrasi ke Showcase**:
   - Daftarkan komponen baru ke `glass_components_metadata` di `scripts/rebuild_all.py`.
   - Tentukan rasio aspek yang tepat (`1:1`, `4:5`, atau `span-tall` untuk `9:16`).
3. **Kompilasi & Build Showcase**:
   - Jalankan `python scripts/rebuild_all.py` dan pastikan script selesai dengan kode keluar 0.
4. **Validasi Responsivitas**:
   - Pastikan komponen tidak terpotong pada lebar minimum 320px (`min-width: 0` pada elemen flex).
   - Pastikan tidak ada horizontal scrollbar liar pada body.
