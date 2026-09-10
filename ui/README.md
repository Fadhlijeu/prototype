# UI Workspace & Component Architecture Manifest

Direktori `ui/` adalah pusat repositori desain antarmuka, aset komponen modular, dan spesifikasi tema dalam ekosistem prototype — **dipisahkan per platform** (`web`, `android`, dst).

---

## 🗄️ Struktur Multi-Platform

```text
ui/
├── web/                 # Semua UI yang berjalan di browser
│   ├── components/      # Komponen UI (glass/, raw/)
│   └── apps/            # Aplikasi web utuh (File Manager, AI Studio)
└── android/            # UI aplikasi Android (Kotlin / Compose / APK)
    ├── components/      # Komponen UI Compose/Android
    └── apps/            # Proyek APK utuh
```

_Terbaca sebagai poros: setiap platform memiliki subfolder `components/` (komponen reusable) dan `apps/` (aplikasi utuh)._

> **Platform Web (aktif):** `ui/web/`  
> **Platform Android/Kotlin (struktur siap diisi):** `ui/android/`

---

## 💎 Filosofi & Mindset Desain UI

> **"Satu Komponen, Beragam Rupa, Bebas Berganti Tanpa Merusak Fungsi."**

1. **Semantic Layer (`component.md` & `ui/web/components/raw/`)**: Mendefinisikan peran elemen, masukan, status, dan aksesibilitas (ARIA).
2. **Styling Layer (`ui/web/components/<style>/`)**: Menerapkan token visual di bawah direktori spesifik style.

---

## 🏷️ Konvensi Penamaan (Naming Convention Standard)

1. **Nama Folder Komponen**: `kebab-case` deskriptif (cth `chat-input-bar`, `button-glass`).
2. **Pola Berkas Wajib per Komponen** (di `ui/web/components/<style>/<nama>/`):
   ```text
   index.html            # Markup, memuat ../css.css dan ./index.css
   index.css             # Gaya spesifik (@import url('../css.css'))
   index.js              # Logika (opsional)
   <nama>.html           # Versi all-in-one mandiri untuk copy-paste
   ```
3. **Master Style CSS**: `ui/web/components/<style>/css.css` sebagai SSOT token.