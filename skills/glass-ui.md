# Agent Skill: Glass Dark Premium UI Creation

Panduan standar operasional untuk AI Agent saat merancang, membuat, atau memodifikasi komponen dengan gaya **Glass Dark Premium** di direktori `ui/components/glass/`.

---

## 🎨 1. Aturan Warna & Opasitas Permukaan (Surface Hierarchy)

Gunakan variabel dari `ui/components/glass/css.css`. Jika perlu nilai rgba langsung, patuhi rentang berikut:

| Lapisan Permukaan | Nilai / Kode Warna | Opasitas & Fungsi |
|---|---|---|
| **Deep Void Backdrop** | `#08090C` atau `#060709` | Latar kanvas utama aplikasi. Gelap pekat bertekstur, bukan abu-abu terang. |
| **Ambient Glow Blobs** | Cyan (`#00F2FE`), Blue (`#4FACFE`), Purple (`#8E2DE2`) | Blobs melayang di latar belakang dengan `filter: blur(80px)` dan opasitas `0.15–0.25`. |
| **Surface Level 1 (Kontainer Luar)** | `rgba(255, 255, 255, 0.03)` – `0.05` | Card besar, sidepanel, atau background panel utama. |
| **Surface Level 2 (Kartu / Item)** | `rgba(255, 255, 255, 0.06)` – `0.09` | Item list, folder card, input field background. |
| **Surface Level 3 (Interaktif / Hover)**| `rgba(255, 255, 255, 0.12)` – `0.18` | Tombol aksi, active pills, pill switch, floating badge. |

---

## 💡 2. Aturan Pencahayaan Border Asimetris (Specular Edge)

Karakteristik utama Glass Dark Premium adalah **pantulan tepi cahaya asimetris** dari sudut atas-kiri.

```css
/* Contoh Standar Specular Border */
.glass-element {
    border-top: 1px solid rgba(255, 255, 255, 0.28);
    border-left: 1px solid rgba(255, 255, 255, 0.16);
    border-right: 1px solid rgba(255, 255, 255, 0.06);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
```

> **DILARANG**: Memberikan border simetris polos seperti `border: 1px solid rgba(255,255,255,0.1)` pada elemen kaca utama karena akan terlihat seperti kotak plastik datar, bukan kaca berkedalaman.

---

## 🌫️ 3. Aturan Blur & Efek Optik

- **Backdrop Blur Standar**:
  ```css
  backdrop-filter: blur(24px) saturate(160%);
  -webkit-backdrop-filter: blur(24px) saturate(160%);
  ```
- **Bayangan Bertingkat (Elevation Shadow)**:
  Kombinasikan ambient dark shadow dengan inset top specular:
  ```css
  box-shadow: 
      0 12px 40px rgba(0, 0, 0, 0.45),
      inset 0 1px 0 rgba(255, 255, 255, 0.15);
  ```
- **Tekstur Mikro Organik (Noise Layer)**:
  Wajib menyertakan layer noise SVG transparan (`opacity: 0.038`) agar material kaca memiliki tekstur rabaan mikro:
  ```html
  <div class="glass-noise-overlay" aria-hidden="true"></div>
  ```

---

## 🌈 4. Palet Aksen Neon & Status

| Kategori | Hex Code | Penggunaan |
|---|---|---|
| **Primary Cyan Glow** | `#00F2FE` | Indikator aktif, glow aksen, link sorotan, cursor, reasoning high. |
| **Electric Blue** | `#4FACFE` | Tombol CTA utama, status sinkronisasi, FAB container. |
| **Cyber Purple** | `#8E2DE2` | Aksen AI reasoning, model selector K3 Pro, avatar badge. |
| **Emerald Green** | `#10B981` | Status online, kapasitas storage aman, badge sukses. |
| **Amber Warning** | `#F59E0B` | Kapasitas storage hampir penuh, status pending, warning alert. |
| **Coral Destructive** | `#EF4444` | Tombol hapus file/folder, alert error, disk purge. |

---

## 🖋️ 5. Standar Tipografi & Ikonografi

- **Font Family**: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif.
- **Icon Style**: 100% **Outline Stroke 1.5px** (Lucide Icons atau Phosphor Outlined). Dilarang menggunakan ikon solid atau emoji kartun di antarmuka produksi.
- **Ketajaman Teks**: Selalu tambahkan:
  ```css
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  ```
- **Kontras Teks**:
  - Judul / Label Utama: `#FFFFFF` (100% opasitas).
  - Teks Sekunder / Deskripsi: `rgba(255, 255, 255, 0.65)`.
  - Teks Placeholder / Dimmed: `rgba(255, 255, 255, 0.38)`.
