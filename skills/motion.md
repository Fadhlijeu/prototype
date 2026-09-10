# Agent Skill: Motion Physics & Interactive Dynamics

Panduan standar pembuatan animasi, transisi fisika, kontinuitas spasial, dan kepatuhan aksesibilitas gerak (*motion sensitivity*) dalam ekosistem **Prototype Workspace**.

---

## ⚡ 1. Kurva Spring & Timing Standar

Dilarang menggunakan pergerakan linear tanpa bobot (`transition: all 0.3s ease`). Selalu gunakan kurva fisika terkalibrasi:

| Tipe Interaksi | Kurva Cubic-Bezier | Durasi Rekomendasi | Karakter Gerak |
|---|---|---|---|
| **Micro Hover & Press** | `cubic-bezier(0.34, 1.1, 0.64, 1)` | `160ms – 220ms` | Sedikit overshoot elastis (springy) yang responsif terhadap sentuhan/klik. |
| **Pill & Toggle Slide** | `cubic-bezier(0.25, 1, 0.5, 1)` | `220ms – 300ms` | Geseran halus tanpa jeda, meniru pergerakan bantalan magnetik. |
| **Drawer & Sidepanel** | `cubic-bezier(0.16, 1, 0.3, 1)` | `320ms – 400ms` | Dekselerasi tegas bervolume berat (pintu hidrolik halus). |
| **Modal Scale & Blur** | `cubic-bezier(0.19, 1, 0.22, 1)` | `280ms – 350ms` | Pop-up membesar dari skala `0.94` ke `1.0` bersamaan dengan transisi blur. |

---

## 📐 2. Pola Kontinuitas Spasial (Spatial Continuity)

Antarmuka Prototype mengutamakan hubungan ruang antar komponen:

1. **Titik Asal Transformasi (Transform Origin)**:
   - Tooltip dan popover wajib memiliki `transform-origin` yang mengarah tepat ke tombol pemicunya.
   - Contoh: Tooltip di atas tombol harus memiliki `transform-origin: bottom center`.
2. **Staggered Animation untuk List / Cards**:
   - Saat memunculkan serangkaian kartu (seperti folder grid atau daftar pesan chat), terapkan sedikit keterlambatan bertingkat (*stagger delay*):
   ```css
   .card:nth-child(1) { animation-delay: 0.04s; }
   .card:nth-child(2) { animation-delay: 0.08s; }
   .card:nth-child(3) { animation-delay: 0.12s; }
   ```
3. **Efek 3D Tilt Responsif Kursor**:
   - Untuk kartu interaktif (seperti `frosted-folder-card`), implementasikan efek tilt halus berdasarkan posisi pointer (`perspective(800px) rotateX(...) rotateY(...)`) dengan batas maksimal 6–8 derajat agar tidak berlebihan.

---

## 🛑 3. Kepatuhan Aksesibilitas Gerak (`prefers-reduced-motion`)

Setiap animasi di repositori ini **wajib aman** bagi pengguna yang memiliki gangguan vestibular atau sensitivitas gerak.

Sertakan selalu aturan reduksi gerak pada CSS komponen:

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
    
    /* Ganti efek gerak dengan transisi opasitas instan */
    .glass-modal,
    .glass-bottom-sheet,
    .glass-sidepanel {
        transform: none !important;
    }
    
    /* Nonaktifkan efek kanvas berputar atau partikel */
    canvas.swirl-refraction {
        display: none !important;
    }
}
```

---

## 🔊 4. Interaksi Haptic Web Audio (Procedural Feedback)

Untuk meningkatkan rasa rabaan fisik (*tactile feel*), gunakan native Web Audio API untuk menghasilkan bunyi sintetis mikro:
- **Button Tap**: Nada frekuensi tinggi pendek (800Hz turun ke 400Hz selama 25ms, gain 0.05).
- **Toggle On**: Nada naik ganda (440Hz -> 660Hz).
- **Toggle Off**: Nada turun ganda (660Hz -> 440Hz).
- **Destructive Tap**: Frekuensi rendah tumpul (120Hz selama 60ms).
- **Aturan Privasi Audio**: Selalu sediakan tombol mute/unmute di header aplikasi dan hormati status mute tersebut.
