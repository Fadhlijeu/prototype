# Agent Skill: Development Workflow & Quality Gates

Panduan alur kerja standar (*Standard Operating Procedure*) untuk AI Agent saat memodifikasi, menguji, atau merawat repositori **GlassOS Prototype**.

---

## 📋 1. Alur Kerja Siklus Eksekusi (The 5-Step Execution Cycle)

Setiap tugas pengembangan yang dilakukan oleh AI Agent wajib mengikuti 5 tahapan berikut:

```text
1. Research & Inspect
   └── Teliti berkas yang relevan, pahami dependensi dan aturan token.
2. Incremental Implementation
   └── Terapkan perubahan secara bertahap pada berkas target.
3. Automated Verification
   └── Jalankan skrip verifikasi otomatis (verify_links.py, verify_docs.py).
4. Synchronize Ecosystem
   └── Jika ada komponen baru/berubah, jalankan rebuild_all.py.
5. Record Changelog
   └── Catat pembaruan arsitektural secara ringkas di CHANGELOG.md.
```

---

## 🧪 2. Gerbang Kualitas Otomatis (Quality Gates & Verification Commands)

Sebelum melaporkan pekerjaan selesai kepada pengguna, AI Agent **wajib mengeksekusi perintah berikut di terminal**:

### 1. Verifikasi Integritas Tautan Internal & Iframe HTML
```bash
python scripts/verify_links.py
```
*Kriteria Lulus: 100% tautan internal, file CSS, script JS, dan iframe pada seluruh halaman HTML utama terbukti ada di disk.*

### 2. Verifikasi Integritas Dokumentasi & Markdown Links
```bash
python scripts/verify_docs.py
```
*Kriteria Lulus: Semua link markdown internal di `docs/`, `skills/`, `projects/`, dan `README.md` terbukti valid.*

### 3. Sinkronisasi Showroom & Web Apps
Jika ada perubahan pada komponen di `ui/components/`:
```bash
python scripts/rebuild_all.py
```
*Hasil: File `ui/components/glass/showcase.html`, `ui/components/raw/showcase.html`, dan `web-apps.html` akan diperbarui secara otomatis dengan kode terbaru.*

---

## 🚫 3. Aturan Larangan Keras (Strict Constraints)

1. **Dilarang Menjalankan Perintah Interaktif**: Semua perintah terminal harus bersifat mandiri dan otomatis selesai tanpa menunggu input keyboard dari pengguna (misal: gunakan `npx -y` atau skrip Python non-interaktif).
2. **Dilarang Menghapus Komponen yang Berfungsi**: Jangan menghapus file atau merestrukturisasi folder tanpa instruksi eksplisit.
3. **Dilarang Menggunakan Placeholder Dummy**: Jangan meninggalkan kode stub seperti `<!-- TODO: Tambahkan tombol -->`, `// implement later`, atau komponen palsu yang tidak berfungsi.
4. **Dilarang Melanggar Single Source of Truth Token**: Jika token warna, blur, atau bayangan sudah didefinisikan di `ui/components/glass/css.css`, jangan membuat token baru dengan nama berbeda di level aplikasi.

---

## 📝 4. Standar Pencatatan `CHANGELOG.md`

Gunakan format standar Keep a Changelog (format Markdown):
- Sertakan versi dan tanggal pembaruan (misal: `## [3.3.0] - 2026-09-08`).
- Kelompokkan perubahan ke dalam:
  - `Added`: Fitur atau dokumen baru.
  - `Changed`: Restrukturisasi atau modifikasi kode lama.
  - `Fixed`: Perbaikan bug, perbaikan link rusak, atau perbaikan overflow.
- Catat hanya perubahan bernilai arsitektural, hindari mencatat typo kecil satu per satu.
