# Arsitektur Sistem GlassOS (Architecture)

Dokumen ini mendefinisikan struktur teknis repositori, hierarki token desain, batas-batas dependensi antar direktori (*layer boundaries*), dan standar integrasi kode dalam ekosistem **GlassOS Prototype**.

---

## 🏗️ 1. Hierarki 5 Lapisan Sistem (5-Tier Architecture)

Ekosistem GlassOS dibangun di atas struktur dependensi satu arah (*unidirectional dependency*):

```text
┌─────────────────────────────────────────────────────────────┐
│ Tier 4: Applications & Sceneries (projects/*)              │
│         GlassOS File Manager, AI Studio Workspace           │
└──────────────────────────────┬──────────────────────────────┘
                               │ mengonsumsi
┌──────────────────────────────▼──────────────────────────────┐
│ Tier 3: State & Runtime Layer                               │
│         GlassOSStore, persistence (localStorage), audio     │
└──────────────────────────────┬──────────────────────────────┘
                               │ mengikat
┌──────────────────────────────▼──────────────────────────────┐
│ Tier 2: Styled Components (ui/components/glass/*)           │
│         21 komponen terisolasi (Button, Modal, Card, dll.)  │
└──────────────────────────────┬──────────────────────────────┘
                               │ membungkus
┌──────────────────────────────▼──────────────────────────────┐
│ Tier 1: Semantic Primitives (ui/components/raw/*)           │
│         9 komponen murni tanpa style (Pure HTML5 & ARIA)    │
└──────────────────────────────┬──────────────────────────────┘
                               │ dibentuk oleh
┌──────────────────────────────▼──────────────────────────────┐
│ Tier 0: Design Tokens & Material System                     │
│         ui/components/glass/css.css                         │
└─────────────────────────────────────────────────────────────┘
```

### Aturan Ketergantungan (Dependency Constraints):
- **Tier bawah tidak boleh mengimpor Tier di atasnya**: `Tier 0` dan `Tier 1` dilarang mereferensikan file dari `Tier 4`.
- **Single Source of Truth untuk Token**: Semua token visual (warna aksen, radius, blur, bayangan, border) wajib bersumber dari Tier 0 (`ui/components/glass/css.css`). Proyek aplikasi tidak diperbolehkan mendefinisikan ulang variabel token yang sama.

---

## 📂 2. Batas Tanggung Jawab Direktori (Directory Boundaries)

Repositori ini menerapkan pembagian tugas yang tegas untuk setiap folder:

| Direktori | Tanggung Jawab & Target Pembaca | Aturan Konten |
|---|---|---|
| **`docs/`** | **Dokumentasi Global untuk Manusia**. Visi, prinsip, arsitektur, dan keputusan teknis. | Jangan masukkan instruksi langkah demi langkah agentik atau cuplikan kode ad-hoc di sini. |
| **`skills/`** | **SOP Operasional untuk AI Agent**. Aturan teknis pembuatan komponen, motion, glass styling, dan workflow. | Ditulis dalam bentuk constraint ketat, checklist, dan panduan eksekusi yang langsung dapat dibaca AI. |
| **`generator/`** | **Subsistem Generator Otonom & Kurasi**. Mesin generasi UI berbasis model cascade (Gemini/9Router/Mock), decompiler, dan antrean kurasi manusia. | Tidak boleh menyimpan API keys; wajib validasi token glass; mengalirkan komponen baru ke `ui/components/glass/`. |
| **`ui/`** | **Pusat Desain & Komponen**. Berisi token CSS global dan paket komponen modular (`raw/` & `glass/`). | Setiap komponen wajib memiliki folder mandiri yang didekomposisi. |
| **`projects/`** | **Aplikasi Web Utuh & Ruang Kerja**. Implementasi nyata yang memadukan komponen menjadi produk. | Mengonsumsi komponen dan token bersama; memiliki `PROJECT_SPEC.md` sendiri. |
| **`scripts/`** | **Otomatisasi & Pengujian**. Script verifikasi tautan, sinkronisasi showcase, dan audit kualitas. | Wajib dapat dijalankan secara non-interaktif (`python scripts/...`). |
| **Root (`/`)** | **Entry Point & Gateways**. `index.html`, `web-apps.html`, `showcase.html`, `README.md`, `CHANGELOG.md`. | Harus tetap bersih; jangan letakkan komponen individual langsung di root. |

---

## 📦 3. Standar Dekomposisi Komponen (Component Packaging)

Setiap komponen di `ui/components/<style>/` dikemas dalam subdirektori tersendiri dengan struktur 4 berkas baku:

```text
ui/components/glass/<nama-komponen>/
├── index.html            # Markup semantik bersih (memuat ../css.css dan ./index.css)
├── index.css             # Gaya spesifik komponen (scoped classes)
├── index.js              # Logika interaktif / event handlers / Web Audio
└── <nama-komponen>.html  # Versi mandiri (self-contained) untuk integrasi cepat
```

### Manfaat Struktur Ini:
1. **Showroom Otomatis**: Generator [`scripts/rebuild_all.py`](file:///d:/PROJECT/prototype/scripts/rebuild_all.py) dapat membaca `index.html`, `index.css`, dan `index.js` secara terpisah untuk merender tab kode live (*HTML / CSS / JS*).
2. **Modularitas Tinggi**: Pengembang atau agen AI dapat mengambil satu file CSS komponen tanpa harus menyalin seluruh stylesheet aplikasi.
3. **Pemisahan Logika**: Logika interaksi di `index.js` tidak bercampur dengan deklarasi style di `index.css`.

---

## 🔄 4. Siklus Integrasi & Otomatisasi (Showcase Sync)

Ketika ada komponen baru yang ditambahkan atau diubah:
1. Berkas komponen dibuat/diperbarui di subfoldernya masing-masing.
2. Script otomatis [`scripts/rebuild_all.py`](file:///d:/PROJECT/prototype/scripts/rebuild_all.py) dijalankan untuk membaca seluruh berkas komponen, memperbarui basis data showcase di `showcase.html`, `ui/components/glass/showcase.html`, dan `web-apps.html`.
3. Script verifikasi integritas [`scripts/verify_links.py`](file:///d:/PROJECT/prototype/scripts/verify_links.py) dan [`scripts/verify_docs.py`](file:///d:/PROJECT/prototype/scripts/verify_docs.py) dijalankan untuk memastikan seluruh tautan, iframe, dan dependensi valid 100%.
