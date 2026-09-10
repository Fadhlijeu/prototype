# Prinsip & Filosofi Desain (Principles)

Dokumen ini memuat visi inti, moto arsitektur, filosofi material kaca (*optical material*), dan prinsip pergerakan (*motion physics*) yang menjadi acuan pengujian antarmuka dalam **Prototype Workspace**.

---

## 🌟 1. Visi & Moto Arsitektur

> **"Bentuk Mengikuti Fungsi, Gaya Mengikuti Identitas."**  
> *(Form follows function, style follows identity).*

### Visi Utama
Prototype adalah sebuah **laboratorium eksplorasi dan testing antarmuka modern** di mana:
1. **Semantik Web Bersih**: Komponen memiliki fungsi dan aksesibilitas murni yang kokoh sebelum diberi polesan visual.
2. **Material Optik Nyata**: Efek kaca melampaui transparansi dan blur sederhana—mengintegrasikan refraksi, highlight specular asimetris, dan tekstur mikro organik.
3. **Fisika Pergerakan Organik**: Animasi tidak terasa kaku atau sekadar dekoratif, melainkan memiliki bobot, inersia (*spring physics*), dan kontinuitas spasial (*spatial continuity*).

---

## 🏛️ 2. Pemisahan Tiga Lapis (Separation of Concerns)

Untuk mencegah kekacauan dalam pengembangan antarmuka, setiap elemen UI dalam Prototype dipisahkan ke dalam 3 lapisan independen:

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Lapisan Semantik (Semantic / Raw Anatomy)                │
│    Fungsi, ARIA role, input/output, keyboard navigation      │
└──────────────────────────────┬──────────────────────────────┘
                               │ dibungkus oleh
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Lapisan Sistem Desain (Design System / Glass Material)   │
│    Token warna, translusensi, blur, border asimetris, noise  │
└──────────────────────────────┬──────────────────────────────┘
                               │ dikonsumsi oleh
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Lapisan Aplikasi / Skenario (Application / Sceneries)     │
│    Alur kerja produktivitas, state runtime, persistensi data│
└─────────────────────────────────────────────────────────────┘
```

Dengan arsitektur ini, gaya visual dapat diubah atau diganti secara menyeluruh tanpa merusak logika interaksi atau aksesibilitas aplikasi.

---

## 🔮 3. Filosofi Material Kaca (Optical Glass Architecture)

Banyak desain "glassmorphism" di web hanya mengandalkan satu lapisan CSS `backdrop-filter: blur()`. Dalam Prototype UI, permukaan kaca dirancang sebagai **sistem optik multi-lapis**:

1. **Scene Background**: Latar belakang bertingkat gelap pekat (`#08090C` hingga `#0D0E12`) yang diperkaya dengan ambient atmospheric blobs yang halus.
2. **Translucency & Dispersion**: Nilai transparansi seimbang (`0.03` hingga `0.08` untuk kontainer besar, `0.12` hingga `0.20` untuk elemen aksi) dengan saturasi warna latar (`saturate(160%)`).
3. **Asymmetric Specular Lighting**: Cahaya datang dari atas-kiri. Oleh karena itu:
   - `border-top`: Menangkap pantulan cahaya paling terang (`rgba(255, 255, 255, 0.20 - 0.35)`).
   - `border-left`: Pantulan sekunder (`rgba(255, 255, 255, 0.15 - 0.22)`).
   - `border-right & border-bottom`: Menghadap bayangan / oklusi (`rgba(255, 255, 255, 0.04 - 0.08)`).
4. **Organic Noise Overlay**: Permukaan kaca digital murni cenderung terlihat "plastik". Prototype menyematkan layer tekstur noise SVG mikro berfrekuensi tinggi (`opacity: 0.038`) untuk memberikan tekstur rabaan fisik.
5. **Refraction & Caustics**: Untuk interaksi khusus (seperti bottom sheet dan modal), canvas 2D digunakan untuk menghitung refraksi cahaya secara real-time.

---

## 🌊 4. Prinsip Pergerakan & Fisika (Motion Physics)

Motion dalam antarmuka adalah bahasa komunikasi, bukan sekadar riasan.

### 1. Spring Physics & Inersia
Hindari kurva gerak linear standar peramban (`ease`, `linear`). Gunakan kurva spring fisika:
- Aksi Interaktif & Tombol: `cubic-bezier(0.34, 1.1, 0.64, 1)` (efek overshoot ringan yang responsif).
- Panel & Drawer Transisi: `cubic-bezier(0.16, 1, 0.3, 1)` (dekselerasi halus yang tegas).
- Durasi mikro: 150ms – 250ms untuk hover/tap; 300ms – 400ms untuk ekspansi kontainer.

### 2. Kontinuitas Spasial (Spatial Continuity)
Ketika pengguna mengklik elemen (misalnya kartu folder atau avatar), modal atau detail yang terbuka harus terasa berekspansi dari elemen pemicu tersebut, bukan muncul secara acak dari sudut pandang yang terputus.

### 3. Aksesibilitas Gerak (Motion Sensitivity)
Sistem wajib menghormati preferensi pengguna yang sensitif terhadap pergerakan:
- Setiap animasi wajib tunduk pada query `@media (prefers-reduced-motion: reduce)`.
- Pada mode reduced motion, animasi transformasi diganti dengan transisi opasitas instan tanpa pergeseran koordinat.

---

## 📐 5. Standar Kualitas Eksekusi (Quality Baseline)

1. **Zero Cropping / Zero Overflow**: Semua kontainer fleksibel wajib menggunakan `min-width: 0`, dan baris horizontal (seperti quick prompt pills) wajib menggunakan `flex-shrink: 0` dengan `white-space: nowrap` dan overflow terkendali.
2. **Ketahanan Viewport (320px – 1440px+)**: Setiap tata letak harus teruji di layar sempit ponsel (320px–375px), tablet (640px–768px), hingga monitor desktop lebar.
3. **Independensi Tanpa Bundler**: Kode didesain berjalan langsung di browser modern secara native menggunakan Vanilla HTML5, CSS Custom Properties, dan Modern ES6+ JavaScript.
