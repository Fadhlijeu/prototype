# Design System Specification: "Glass Dark Premium"

> **Skill Blueprint / Style Specification** untuk pembuatan komponen web dark-mode glassmorphism premium dengan kedalaman multi-layer, gradien aurora dinamis, tekstur noise halus, dan efek pembiasan lensa (*swirl refraction*).

---

## 1. Parametric Color Palettes (Sistem Palet Rentang Dinamis)

> [!IMPORTANT]
> **PANDUAN PEMBUATAN KOMPONEN UI**: Nilai hex di bawah adalah **CONTOH ARTIKULASI MOOD**, BUKAN nilai statis untuk disalin persis (*copy-paste*). Pilih salah satu dari 8 keluarga palet warna di bawah atau racik kombinasi hex segar yang harmonis. Jangan pernah menghasilkan komponen dengan skema biru-ungu yang itu-itu saja!

```css
:root {
    /* Background Canvas (Deep Void Dark Mode) */
    --bg-page: #0A0A0A;                  /* Pure deep black canvas */
    --bg-void: #030712;                  /* Ultra-deep void container */

    /* Glass Surfaces (Standard Opacities) */
    --glass-base: rgba(255, 255, 255, 0.04);
    --glass-card: rgba(255, 255, 255, 0.06);
    --glass-elevated: rgba(255, 255, 255, 0.09);

    /* Asymmetric Glass Borders (Simulasi Cahaya dari Atas) */
    --glass-border-top: rgba(255, 255, 255, 0.20);    /* Rentang 0.18 - 0.26 (Paling Terang / Specular) */
    --glass-border-side: rgba(255, 255, 255, 0.09);   /* Rentang 0.07 - 0.12 (Pencahayaan Samping) */
    --glass-border-bottom: rgba(255, 255, 255, 0.03); /* Rentang 0.02 - 0.05 (Paling Gelap / Shadowed) */

    /* Typography */
    --text-primary: #FFFFFF;
    --text-secondary: rgba(255, 255, 255, 0.65);
    --text-muted: rgba(255, 255, 255, 0.38);

    /* Springs & Easings */
    --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
    --ease-spring: cubic-bezier(0.32, 0.72, 0, 1);
    --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### 8 Pilihan Spektrum Palet Aksen (Pilih 1 secara acak per generation):
1. **Neon Cyan & Emerald** (Telemetry, Sensors, Data Matrix):
   - Primary: `#22D3EE` | Secondary: `#10B981` | Glow: `rgba(6, 182, 212, 0.65)`
   - Aurora Blobs: `rgba(6, 182, 212, 0.70)`, `rgba(16, 185, 129, 0.55)`, `rgba(14, 116, 144, 0.40)`
2. **Electric Amber & Solar Gold** (Feedback, Gauges, Warnings, Metrics):
   - Primary: `#FBBF24` | Secondary: `#F59E0B` | Glow: `rgba(245, 158, 11, 0.65)`
   - Aurora Blobs: `rgba(245, 158, 11, 0.70)`, `rgba(217, 119, 6, 0.55)`, `rgba(251, 191, 36, 0.40)`
3. **Hot Pink & Violet** (Action Buttons, FABs, Speed Dials, Triggers):
   - Primary: `#F472B6` | Secondary: `#8B5CF6` | Glow: `rgba(244, 114, 182, 0.65)`
   - Aurora Blobs: `rgba(244, 114, 182, 0.70)`, `rgba(139, 92, 246, 0.60)`, `rgba(236, 72, 153, 0.45)`
4. **Mint Green & Electric Teal** (Switches, Segmented Controls, Health Nodes):
   - Primary: `#34D399` | Secondary: `#14B8A6` | Glow: `rgba(52, 211, 153, 0.65)`
   - Aurora Blobs: `rgba(52, 211, 153, 0.70)`, `rgba(20, 184, 166, 0.55)`, `rgba(6, 182, 212, 0.40)`
5. **Sapphire Blue & Sky** (Form Inputs, Prompt Bars, Search Clusters):
   - Primary: `#60A5FA` | Secondary: `#38BDF8` | Glow: `rgba(59, 130, 246, 0.65)`
   - Aurora Blobs: `rgba(59, 130, 246, 0.70)`, `rgba(56, 189, 248, 0.55)`, `rgba(99, 102, 241, 0.45)`
6. **Amethyst & Deep Indigo** (Navigation Docks, Breadcrumbs, Rails):
   - Primary: `#A78BFA` | Secondary: `#6366F1` | Glow: `rgba(167, 139, 250, 0.65)`
   - Aurora Blobs: `rgba(167, 139, 250, 0.70)`, `rgba(99, 102, 241, 0.60)`, `rgba(129, 140, 248, 0.40)`
7. **Solar Ruby & Coral** (Security Nodes, Alerts, Status Badges):
   - Primary: `#FB7185` | Secondary: `#EF4444` | Glow: `rgba(239, 68, 68, 0.65)`
   - Aurora Blobs: `rgba(251, 113, 133, 0.70)`, `rgba(239, 68, 68, 0.55)`, `rgba(244, 63, 94, 0.40)`
8. **Spectral Prismatic** (Composite Workstations, Dashboards, Scenery):
   - Primary: `#38BDF8` | Secondary: `#C084FC` | Glow: `rgba(192, 132, 252, 0.65)`
   - Aurora Blobs: `rgba(56, 189, 248, 0.65)`, `rgba(192, 132, 252, 0.60)`, `rgba(244, 114, 182, 0.45)`

---

## 2. Multi-Layer Glass Card Architecture

Setiap kartu kaca **WAJIB** mengikuti arsitektur tumpukan 5 layer:

```text
Layer 5: Page Background (#0A0A0A)
Layer 4: 3D Shadow Card (gelap, scale 0.96, translateY 12px, blur 30px, colored shadow)
Layer 3: Aurora/Mesh Gradient (radial gradients dinamis, 10s infinite morph)
Layer 2: Main Glass Card (bg rgba(255,255,255,0.06), backdrop-filter: blur(30px) saturate(160%))
Layer 1: Noise Texture Overlay (SVG feTurbulence, opacity 0.04, blend-mode: overlay)
Layer 0: Content Layout & Typography
```

### Implementasi CSS:
```css
/* Container Utama */
.glass-card-wrapper {
    position: relative;
    width: 100%;
}

/* Layer 4: 3D Shadow Card */
.layer-4-shadow {
    position: absolute;
    top: 12px;
    left: 0; right: 0; bottom: -12px;
    background: rgba(25, 45, 110, 0.5);
    border-radius: 32px;
    filter: blur(30px);
    transform: scale(0.96) translateY(12px);
    z-index: -2;
    transition: all 0.4s var(--ease-spring);
}

/* Layer 3: Aurora Mesh Gradient */
.layer-3-aurora {
    position: absolute;
    inset: 0;
    border-radius: 28px;
    overflow: hidden;
    z-index: -1;
}

/* Layer 2: Main Glass Card */
.layer-2-glass {
    position: relative;
    width: 100%;
    padding: 24px 28px;
    background: var(--glass-card);
    backdrop-filter: blur(30px) saturate(160%);
    -webkit-backdrop-filter: blur(30px) saturate(160%);
    border-radius: 28px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.08);
    
    /* Asymmetric Border Lighting */
    border: 1px solid transparent;
    border-top-color: var(--glass-border-top);
    border-left-color: var(--glass-border-side);
    border-right-color: var(--glass-border-side);
    border-bottom-color: var(--glass-border-bottom);
    overflow: hidden;
    z-index: 1;
}

/* Layer 1: Noise Texture Overlay */
.layer-2-glass::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    opacity: 0.04;
    mix-blend-mode: overlay;
    pointer-events: none;
    z-index: 0;
}
```

---

## 3. Noise Texture Rule (Critical & Non-Negotiable)

Tanpa tekstur noise, kaca terlihat seperti plastik digital murahan.
- Filter SVG: `<feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" />`
- Opacity: `0.03` hingga `0.05`.
- Blend Mode: `overlay` atau `soft-light`.

---

## 4. Aurora Mesh Gradient Specification (Formula Rentang Dinamis)

DILARANG menggunakan gradien linier sederhana. Gunakan multi-blob radial gradient yang diposisikan dan dianimasikan secara unik:
- **Formula Penempatan Blob (WAJIB acak per komponen, BUKAN menyalin koordinat contoh)**:
  - Blob 1 (Utama): `radial-gradient(circle at [X: 15%–45%] [Y: 30%–65%], var(--aurora-1, rgba(...)), transparent 60%–70%)`
  - Blob 2 (Sekunder): `radial-gradient(circle at [X: 55%–85%] [Y: 50%–85%], var(--aurora-2, rgba(...)), transparent 50%–65%)`
  - Blob 3 (Aksen Sorot): `radial-gradient(circle at [X: 25%–75%] [Y: 10%–40%], var(--aurora-3, rgba(...)), transparent 40%–55%)`
  - Opasitas Blob: Rentang `0.35` hingga `0.75` (disesuaikan dengan kontras teks di atasnya).

> [!TIP]
> Nilai koordinat `30% 50%` atau `80% 80%` di atas adalah contoh acuan mood. Saat membuat komponen, berikan angka koordinat unik di dalam rentang tersebut agar bentuk pencahayaan setiap komponen berbeda.

### Keyframes Animasi:
```css
@keyframes auroraMorph {
    0% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; transform: translate(0, 0) scale(1); }
    50% { transform: translate(5%, 8%) scale(1.05); }
    100% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; transform: translate(-5%, -5%) scale(0.95); }
}
```

---

## 5. Swirl Refraction Filter (Lensa Pembias Organik)

Saat modal atau bottom sheet muncul di atas konten, latar belakang tidak sekadar di-blur, melainkan dibiaskan seperti melihat melalui kaca cembung tebal.

### SVG Filter Chain:
```html
<svg width="0" height="0" style="position:absolute;">
    <filter id="swirlBlur">
        <feTurbulence type="fractalNoise" baseFrequency="0.008 0.015" numOctaves="3" result="noise"/>
        <feDisplacementMap in="SourceGraphic" in2="noise" scale="25" xChannelSelector="R" yChannelSelector="G" result="displaced"/>
        <feGaussianBlur in="displaced" stdDeviation="10" result="blurred"/>
        <feComposite in="blurred" in2="SourceGraphic" operator="over"/>
    </filter>
</svg>
```
Atau melalui engine Canvas 2D per-pixel displacement untuk rendering 60fps yang dinamis.

---

## 6. Iconography Rules

- **Gaya**: OUTLINE / STROKE ONLY. DILARANG menggunakan ikon berisi penuh (*filled*).
- **Ketebalan Garis (Stroke Width)**: `1.5px` seragam.
- **Ukuran**: `20-24px` standar, `28-32px` untuk ikon featured.
- **Warna Aktif**: `#FFFFFF`, **Warna Pasif**: `rgba(255, 255, 255, 0.50)`.
- **Pustaka**: Lucide Icons atau Phosphor Icons (regular/thin).

---

## 7. Aturan Tombol (Buttons)

### Primary Action Button:
- Background: `linear-gradient(135deg, #4A7BF7 0%, #2E5FD9 50%, #1E3A8A 100%)`.
- Border Top: `1px solid rgba(255, 255, 255, 0.25)`.
- Border Bottom: `1px solid rgba(0, 0, 0, 0.20)` (menghasilkan kedalaman fisik 3D).
- Box Shadow: `0 4px 16px rgba(59, 130, 246, 0.30), inset 0 1px 1px rgba(255, 255, 255, 0.15)`.
- Hover: `transform: translateY(-2px)`, bayangan dipertegas.
- Active: `transform: scale(0.96)`.

### Secondary / Ghost Button:
- Background: `rgba(255, 255, 255, 0.05)`.
- Border: `1px solid rgba(255, 255, 255, 0.10)`.
- Hover: `background: rgba(255, 255, 255, 0.10)`, `transform: translateY(-1px)`.

---

## 8. Anti-Patterns (DILARANG KERAS)

- ❌ DILARANG menggunakan gradien linier sederhana untuk latar belakang kaca — selalu gunakan multi-blob aurora mesh.
- ❌ DILARANG melewatkan tekstur noise — tanpa noise kaca tampak flat.
- ❌ DILARANG membuat border dengan kecerahan seragam — tepi atas harus selalu lebih terang dari tepi bawah.
- ❌ DILARANG menggunakan ikon berisi penuh (*filled*) — selalu gunakan ikon outline stroke 1.5px.
- ❌ DILARANG menggunakan bayangan hitam pekat murni — gunakan bayangan gelap dengan rona biru/ungu/indigo.
- ❌ DILARANG melupakan border 1px pada permukaan kaca — kaca tanpa garis tepi terlihat mati.
- ❌ DILARANG menaruh tombol FAB di dalam baris navigasi dok — FAB harus berdiri terpisah.
