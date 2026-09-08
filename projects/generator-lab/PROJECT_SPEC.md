# Project Specification: GlassOS Autonomous Generator Lab & Curation Studio

## 1. Identitas Proyek
- **Nama Aplikasi**: GlassOS Autonomous Generator Lab & Curation Studio
- **Versi**: v1.0.0
- **Status**: Production Ready / Interactive Studio
- **Lokasi Berkas**: `projects/generator-lab/index.html`
- **Tujuan**: Ruang kerja visual berbasis web untuk mengawasi siklus generasi otonom, menguji prompt on-demand, meninjau antrean kandidat UI (Review Queue), mengeksekusi keputusan kurasi manusia (Accept/Reject), dan memantau status cascade model AI (Gemini, TokenRouter, 9Router).

---

## 2. Fitur Utama & Antarmuka

### A. Model Cascade Telemetry Monitor
- Menampilkan kartu telemetri real-time:
  1. **Google Gemini Flash Lite**: Prioritas #1 (1.000 req/hari gratis)
  2. **TokenRouter GLM-5.3**: Prioritas #2 (Cloud Workhorse Unlimited)
  3. **9Router Local Gateway**: Prioritas #3 (Localhost desktop mode)
  4. **Curator Review Queue**: Jumlah antrean pending dan total komponen approved.

### B. Direct Synthesis Control Panel
- Input prompt directive mandiri dengan rekomendasi *seed chips* satu klik.
- Pemilihan taksonomi kategori dan selector model aktif.
- Sintesis instan dengan haptic feedback dan animasi loading.

### C. Review Queue & Decision Stream
- Tab navigasi tiga status:
  - **Pending Review (N)**: Menampilkan kartu kandidat dengan skor kualitas, model pembuat, tag variasi, dan **Live Interactive Preview Iframe**.
  - **Approved Showroom**: Arsip komponen yang telah disetujui.
  - **Rejected Archive**: Arsip komponen yang ditolak.
- **Tombol Keputusan (Human Decision)**:
  - Tombol hijau kaca **Setujui & Deploy**: Memindahkan ke showroom, memperbarui store, dan memicu notifikasi toast.
  - Tombol merah kaca **Tolak (Reject)**: Menolak komponen dan mengarsipkan.

### D. Dynamic Empty State UI
- Saat antrean pending berjumlah 0:
  - Menampilkan kartu kaca obsidian elegan dengan ikon sparkles berpendar (*pulsing ambient glow*).
  - Judul: *"Review Queue is Clear"*.
  - Deskripsi: *"0 kandidat dalam antrean review. Seluruh artefak UI yang digenerate oleh AI telah dikurasi ke dalam GlassOS design system."*
  - Tombol aksi cepat: *"Generate Sample Candidate"* (menambahkan sampel instan untuk mencoba kurasi) dan *"Tulis Prompt Sendiri"*.

### E. State Persistence
- Menyimpan seluruh status antrean secara atomik di `localStorage` (`glassos_generator_lab_v1`).
