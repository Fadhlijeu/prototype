# UI Workspace & Component Architecture Manifest

Direktori `ui/` adalah pusat repositori desain antarmuka, aset komponen modular, dan spesifikasi tema dalam ekosistem prototype ini.

---

## 🏛️ Filosofi & Mindset Desain UI

> **"Satu Komponen, Beragam Rupa, Bebas Berganti Tanpa Merusak Fungsi."**

1. **Semantic Layer (component.md & ui/components/raw/)**:
   Mendefinisikan peran elemen (*role*), masukan (*inputs*), status (*states: hover, active, focus, disabled*), dan aksesibilitas (ARIA).
2. **Styling Layer (ui/components/<style>/)**:
   Menerapkan token visual (warna, blur, shadow, border, spring physics) di bawah direktori spesifik style.

---

## 🏷️ Konvensi Penamaan (Naming Convention Standard)

Untuk menjaga kerapian dan konsistensi di seluruh direktori komponen:
1. **Nama Folder Komponen**: Menggunakan format `kebab-case` deskriptif (contoh: `chat-input-bar`, `button-glass`, `ai-model-selector`).
2. **Suffix Style**:
   - Jika berada di dalam folder style (misal `ui/components/glass/`), nama folder komponen dasar boleh menggunakan suffix `-glass` (misal `button-glass/`, `checkbox-glass/`) untuk kejelasan tipe visual.
3. **Pola Berkas Wajib per Folder Komponen**:
   Setiap subfolder komponen **wajib** memiliki 4 berkas berikut:
   ```text
   ui/components/<style>/<nama-komponen>/
   ├── index.html            # Markup bersih, memuat ../css.css dan ./index.css
   ├── index.css             # Gaya spesifik komponen (@import url('../css.css'))
   ├── index.js              # Logika interaksi/animasi (opsional jika ada JS)
   └── <nama-komponen>.html  # Versi all-in-one mandiri untuk copy-paste cepat
   ```
4. **Master Style CSS**: Setiap folder style wajib memiliki file referensi bersama `css.css` di root style-nya (contoh: `ui/components/glass/css.css`).

---

## 📐 Standar Kualitas Komponen (Quality Checklist)

- [x] **Dekomposisi Penuh**: Terbagi ke dalam `index.html`, `index.css`, `index.js`, dan all-in-one HTML.
- [x] **Zero Overflow / Zero Cropping**: Menggunakan `width: 0; min-width: 0; flex: 1;` pada flex input, serta `white-space: nowrap; flex-shrink: 0;` pada horizontal scrollers agar tidak pernah terpotong pada layar 320px–375px.
- [x] **Responsif (320px – 1440px)**: Tampil sempurna dalam mode Mobile (375px), Tablet (640px), dan Desktop (100%).
- [x] **Ikon Outlined**: Menggunakan ikon stroke `1.5px` (Lucide Icons).
- [x] **Noise Texture Included (Glass)**: Permukaan kaca wajib menyertakan overlay tekstur noise SVG mikro (`opacity: 0.038`).
