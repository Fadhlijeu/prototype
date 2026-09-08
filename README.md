# GlassOS Prototype & UI/UX Component Ecosystem

Laboratorium pengujian, standarisasi, dan inkubasi komponen antarmuka pengguna (UI/UX) modern berbasis material optik kaca (*optical glass*) dan fisika pergerakan (*motion physics*).

---

## ⚡ Akses Cepat & Preview Lokal

Jalankan preview web server lokal langsung dari root direktori (port 3000):

```bash
npm start
# atau: npx serve . -p 3000
```

Buka **`http://localhost:3000/`** di peramban. Seluruh modul dan navigasi siap digunakan:
- 🌐 [**Master Gateway Portal**](file:///d:/PROJECT/prototype/index.html) (`/index.html`)
- 🚀 [**Web Applications Showcase**](file:///d:/PROJECT/prototype/web-apps.html) (`/web-apps.html`)
- 💎 [**Glass Component Showroom**](file:///d:/PROJECT/prototype/ui/components/glass/showcase.html) (`/ui/components/glass/showcase.html`)
- 🔲 [**Raw Semantic Component Showroom**](file:///d:/PROJECT/prototype/ui/components/raw/showcase.html) (`/ui/components/raw/showcase.html`)

---

## 📂 Struktur Utama Repositori

```text
prototype/
├── docs/                 # Pusat dokumentasi pemahaman manusia (prinsip, arsitektur)
├── skills/               # SOP & aturan teknis operasional untuk AI Agent
├── projects/             # Implementasi aplikasi web utuh (File Manager, AI Studio)
├── ui/                   # Token desain & paket komponen modular (raw & glass)
├── scripts/              # Perkakas verifikasi integritas, testing, & generator
├── index.html            # Portal gerbang utama
└── package.json          # Manajemen script preview & pengujian
```

---

## 📚 Pusat Dokumentasi & Agent Skills

Untuk menjaga kerapian dan mencegah duplikasi informasi, dokumentasi dipisahkan secara tegas:

| Direktori | Sasaran & Fungsi Utama | Dokumen Kunci |
|---|---|---|
| [**`docs/`**](file:///d:/PROJECT/prototype/docs/README.md) | **Pemahaman Manusia**: Visi produk, filosofi optik & fisika gerak, serta 5-layer arsitektur sistem. | [`principles.md`](file:///d:/PROJECT/prototype/docs/principles.md), [`architecture.md`](file:///d:/PROJECT/prototype/docs/architecture.md) |
| [**`skills/`**](file:///d:/PROJECT/prototype/skills/README.md) | **Eksekusi AI Agent**: SOP pembuatan glass UI, standar dekomposisi berkas, kurva gerak, dan workflow. | [`glass-ui.md`](file:///d:/PROJECT/prototype/skills/glass-ui.md), [`component.md`](file:///d:/PROJECT/prototype/skills/component.md), [`motion.md`](file:///d:/PROJECT/prototype/skills/motion.md), [`workflow.md`](file:///d:/PROJECT/prototype/skills/workflow.md) |
| [**`component.md`**](file:///d:/PROJECT/prototype/component.md) | **Kamus Master Komponen**: Taksonomi 120+ komponen universal dan inventarisasi berkas aktual di disk. | [`component.md`](file:///d:/PROJECT/prototype/component.md) |
| [**`projects/`**](file:///d:/PROJECT/prototype/projects/README.md) | **Portofolio Aplikasi Web**: Manifest dan cetak biru aplikasi terintegrasi. | [`README.md`](file:///d:/PROJECT/prototype/projects/README.md), [`TEMPLATE.md`](file:///d:/PROJECT/prototype/projects/TEMPLATE.md) |

---

## 🧪 Perintah Pengujian & Kualitas

```bash
npm run verify                # Verifikasi 100% tautan internal HTML, iframe & aset
python scripts/verify_docs.py # Verifikasi integritas tautan Markdown
npm run rebuild               # Sinkronisasi ulang database showcase & web-apps
```
