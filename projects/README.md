# Web Applications & Projects Directory

Direktori ini berisi seluruh **aplikasi web utuh (*frontend composite projects*)** yang mengintegrasikan puluhan komponen antarmuka menjadi satu ekosistem aplikasi fungsional yang siap pakai.

---

## 🏛️ Arsitektur Direktori Proyek

```text
projects/
├── README.md                  # Manifest & panduan direktori proyek
├── TEMPLATE.md                # Cetak biru standar spesifikasi proyek baru
│
├── file-manager/              # Proyek: Cloud File Manager
│   ├── index.html             # Aplikasi web utuh mandiri (Single-File Architecture)
│   └── PROJECT_SPEC.md        # Spesifikasi arsitektur & komponen terintegrasi
│
└── ai-studio/                 # Proyek: AI Agent Studio Workspace
    ├── index.html             # Ruang kerja agentik AI interaktif
    └── PROJECT_SPEC.md        # Spesifikasi arsitektur AI studio
```

---

## 🚀 Daftar Proyek Aktif

| Nama Proyek | Versi | Status | Direktori | Live Showroom |
|---|---|---|---|---|
| **Cloud File Manager** | v2.4 | `[production-ready]` | [`projects/file-manager/`](file-manager/) | [`web-apps.html#project-file-manager`](../web-apps.html#project-file-manager) |
| **AI Agent Studio** | v1.0 | `[production-ready]` | [`projects/ai-studio/`](ai-studio/) | [`web-apps.html#project-ai-studio`](../web-apps.html#project-ai-studio) |

---

## 📐 Panduan Menambahkan Proyek Baru

Setiap kali Anda membuat atau menambahkan proyek aplikasi baru:
1. Buat folder baru di bawah `projects/` dengan nama format *kebab-case*:
   ```text
   projects/<nama-aplikasi>/
   ├── index.html              # Entry point aplikasi
   └── PROJECT_SPEC.md         # Spesifikasi arsitektur (salin dari TEMPLATE.md)
   ```
2. Pastikan aplikasi mengimpor dan merakit komponen dari `ui/components/glass/` atau menyematkan token desain dari `ui/components/glass/css.css`.
3. Daftarkan proyek ke dalam [`web-apps.html`](../web-apps.html) dan [`projects/README.md`](README.md).
