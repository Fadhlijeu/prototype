# Prototype Agent Skills & Execution SOPs

Direktori `skills/` adalah repositori pengetahuan operasional (*Standard Operating Procedures*) yang dirancang khusus sebagai **panduan eksekusi untuk AI Agent** yang bertugas di repositori ini.

Setiap file dalam direktori ini mendefinisikan aturan ketat (*hard constraints*), panduan penamaan (*conventions*), standar CSS token, serta pola arsitektur kode yang **wajib dipatuhi** oleh AI Agent.

---

## 🛠️ Daftar Panduan Keterampilan (Agent Skills)

| Skill File | Topik & Tanggung Jawab Utama |
|---|---|
| [**`glass-ui.md`**](file:///d:/PROJECT/prototype/skills/glass-ui.md) | **Aturan Desain Kaca Glass Dark Premium**: Token CSS, pencahayaan border asimetris, level blur, opasitas permukaan, layer noise SVG, dan palet warna neon. |
| [**`component.md`**](file:///d:/PROJECT/prototype/skills/component.md) | **Standar Dekomposisi Komponen**: Konvensi 4 berkas (`index.html`, `index.css`, `index.js`, `<name>.html`), isolasi class CSS, pencegahan overflow, dan semantik HTML. |
| [**`motion.md`**](file:///d:/PROJECT/prototype/skills/motion.md) | **Fisika Gerak & Interaksi**: Kurva spring `cubic-bezier`, timing micro-interaction, kontinuitas spasial, dan kepatuhan `@media (prefers-reduced-motion)`. |
| [**`workflow.md`**](file:///d:/PROJECT/prototype/skills/workflow.md) | **SOP Kerja Agent**: Alur kerja langkah demi langkah, eksekusi script pengujian non-interaktif, sinkronisasi showcase otomatis, dan aturan komit. |

---

## ⚡ Aturan Emas bagi AI Agent

1. **Konsumsi Token Bersama**: Dilarang membuat variabel warna atau gaya acak secara lokal jika token sudah tersedia di `ui/components/glass/css.css`.
2. **Dekomposisi Wajib**: Setiap komponen baru wajib dibuat dalam subfoldernya sendiri dengan memisahkan HTML, CSS, dan JS.
3. **Uji Sebelum Melapor**: Setiap penambahan atau perubahan berkas wajib diuji menggunakan script verifikasi (`python scripts/verify_links.py` dan `python scripts/verify_docs.py`) sebelum sesi dinyatakan selesai.
4. **Bebas Placeholder**: Dilarang keras meninggalkan komentar placeholder seperti `<!-- TODO -->`, `/* styling here */`, atau teks dummy yang tidak memiliki implementasi nyata.
