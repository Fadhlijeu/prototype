# Agent Skill: Component Engineering & Decomposition

Panduan standar dekomposisi berkas, isolasi gaya, pencegahan pemotongan tampilan (*anti-cropping*), dan semantik aksesibilitas untuk pembuatan komponen di direktori `ui/components/`.

---

## 📁 1. Pola Berkas Wajib per Komponen (The 4-File Pattern)

Setiap subfolder komponen baru di `ui/components/glass/<nama-komponen>/` **wajib** memiliki 4 berkas berikut:

```text
ui/components/glass/<nama-komponen>/
├── index.html            # Markup semantik bersih
├── index.css             # Gaya spesifik komponen yang terisolasi
├── index.js              # Logika interaksi, audio feedback, event listener
└── <nama-komponen>.html  # Versi mandiri (self-contained) untuk uji langsung
```

### Rincian Isi Berkas:
1. **`index.html`**:
   - Memuat file CSS bersama: `<link rel="stylesheet" href="../css.css">`.
   - Memuat CSS lokal: `<link rel="stylesheet" href="./index.css">`.
   - Memuat skrip lokal: `<script src="./index.js" defer></script>`.
   - Menggunakan markup semantik HTML5 bersih tanpa tag `<style>` besar di dalam body.
2. **`index.css`**:
   - Menyertakan `@import url('../css.css');` di baris pertama.
   - Menggunakan scoped class names (contoh: `.glass-pills-row`, `.frosted-card`).
3. **`index.js`**:
   - Berisi event listener modern (`addEventListener`).
   - Hindari manipulasi `onclick="..."` inline di HTML.
   - Menggunakan Web Audio native jika memerlukan feedback audio.
4. **`<nama-komponen>.html`**:
   - File mandiri all-in-one yang menyematkan seluruh CSS dan JS di dalam satu file untuk kemudahan preview cepat dan copy-paste pengguna.

---

## 🛡️ 2. Aturan Isolasi Class (Scoped CSS)

Untuk mencegah style collision saat beberapa komponen digabungkan dalam satu dashboard:
- Gunakan penamaan berbasis namespace: `.g-<komponen>-<elemen>` atau `.<komponen-kebab>-<elemen>`.
- Contoh Benar: `.glass-chat-bar`, `.glass-chat-input`, `.glass-chat-send-btn`.
- DILARANG menggunakan selektor universal berbahaya seperti:
  ```css
  /* JANGAN LAKUKAN INI DI index.css KOMPONEN */
  button { padding: 10px; }
  input { background: red; }
  * { box-sizing: border-box; }
  ```

---

## 🚫 3. Aturan Bebas Terpotong (Zero Cropping & Anti-Overflow)

Pada layar sempit (320px–375px), flex layout sering mengalami pemotongan teks atau tombol terhimpit. Patuhi aturan CSS berikut:

### 1. Untuk Elemen Input & Teks di Dalam Flexbox
Tambahkan selalu `min-width: 0` agar elemen dapat menyusut sesuai ruang yang tersedia:
```css
.input-container {
    display: flex;
    align-items: center;
    width: 100%;
    min-width: 0;
}

.input-field {
    flex: 1;
    min-width: 0;
    width: 0; /* Memaksa flexbox menghitung ulang lebar sebenarnya */
}
```

### 2. Untuk Baris Horizontal Scroller (Pills / Tabs)
Item pil tidak boleh mengecil atau teksnya terpotong:
```css
.horizontal-pills-container {
    display: flex;
    overflow-x: auto;
    overflow-y: hidden;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}

.pill-item {
    flex-shrink: 0; /* Wajib agar pil tidak gepeng */
    white-space: nowrap;
}
```

---

## ♿ 4. Semantik & Aksesibilitas Baku (A11y Baseline)

1. **Tombol Interaktif**: Wajib menggunakan elemen `<button type="button">`, DILARANG menggunakan `<div onclick="...">`.
2. **Pilihan Eksklusif (Radio / Selector Card)**:
   - Gunakan `role="radiogroup"` pada kontainer pembungkus.
   - Gunakan `role="radio"` dan `aria-checked="true|false"` pada masing-masing kartu pilihan.
3. **Indikator Fokus Keyboard**:
   - Selalu berikan gaya `:focus-visible` dengan outline cyan lembut:
   ```css
   :focus-visible {
       outline: 2px solid var(--accent-cyan, #00f2fe);
       outline-offset: 2px;
       box-shadow: 0 0 12px rgba(0, 242, 254, 0.4);
   }
   ```
4. **Modal & Sheet**:
   - Wajib menyertakan tombol tutup yang dapat diakses dengan tombol `Escape`.
   - Gunakan `aria-modal="true"` dan `role="dialog"`.
