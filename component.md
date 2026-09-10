# Master Directory & Taxonomy: Web UI/UX Components

> **Dokumen Master Audit Komponen Web Universal (Design-Agnostic)**  
> Direktori komprehensif seluruh komponen antarmuka pengguna web (dari level primitif atomik hingga scenery komposit), independen dari gaya visual atau tema tertentu. Dokumen ini menjadi acuan tunggal fungsi, anatomi, dan taksonomi komponen sebelum gaya desain spesifik (seperti Glass Dark atau tema visual lainnya) diterapkan di subfolder gaya masing-masing (misal: `ui/components/<style>/`).

---

## Daftar Isi
1. [Taksonomi Hierarki (Atomic Design)](#1-taksonomi-hierarki-komponen)
2. [Kategori 1: Actions & Triggers (Tombol & Pemicu)](#kategori-1-actions--triggers)
3. [Kategori 2: Text Inputs & Editors (Masukan Teks & Editor)](#kategori-2-text-inputs--editors)
4. [Kategori 3: Selection & Value Controls (Kontrol Pilihan & Nilai)](#kategori-3-selection--value-controls)
5. [Kategori 4: Pickers & Droppers (Pemilih & Pengunggah)](#kategori-4-pickers--droppers)
6. [Kategori 5: Navigation & Hierarchy (Navigasi & Struktur)](#kategori-5-navigation--hierarchy)
7. [Kategori 6: Data Display & Containers (Kontainer & Tampilan Data)](#kategori-6-data-display--containers)
8. [Kategori 7: Tables, Lists & Trees (Tabel, Daftar & Hirarki)](#kategori-7-tables-lists--trees)
9. [Kategori 8: Telemetry, Charts & Gauges (Analitik & Indikator Ukur)](#kategori-8-telemetry-charts--gauges)
10. [Kategori 9: Feedback & Status Indicators (Umpan Balik & Status)](#kategori-9-feedback--status-indicators)
11. [Kategori 10: Overlays, Sheets & Modals (Lapisan Melayang & Modal)](#kategori-10-overlays-sheets--modals)
12. [Kategori 11: Layout Primitives & Utilities (Primitif Tata Letak)](#kategori-11-layout-primitives--utilities)
13. [Kategori 12: Sceneries & Composite Patterns (Ruang Kerja Komposit)](#kategori-12-sceneries--composite-patterns)

---


---

## 🏷️ Inventarisasi Komponen: Taksonomi vs Implementasi Aktual

Untuk membedakan secara tegas antara **peta perancangan konseptual** dan **komponen yang sudah benar-benar selesai diimplementasikan di disk**:

| Kategori Inventarisasi | Jumlah Komponen | Status & Lokasi Berkas |
|---|---|---|
| **Master Component Taxonomy** | **120+ Komponen** | Cetak biru arsitektur universal web (daftar lengkap di Kategori 1–12). |
| **Implemented Glass Components** | **21 Komponen** | Selesai didekomposisi (4 berkas: `index.html`, `index.css`, `index.js`, `<name>.html`) di [`ui/components/glass/`](file:///d:/PROJECT/prototype/ui/web/components/glass/). |
| **Implemented Raw Semantic** | **9 Komponen** | Selesai didekomposisi (HTML murni tanpa CSS) di [`ui/components/raw/`](file:///d:/PROJECT/prototype/ui/web/components/raw/). |
| **Integrated Web Applications** | **2 Aplikasi** | Terintegrasi penuh di [`ui/web/apps/file-manager/`](file:///d:/PROJECT/prototype/ui/web/apps/file-manager/) & [`ui/web/apps/ai-studio/`](file:///d:/PROJECT/prototype/ui/web/apps/ai-studio/). |

---

### Tabel Komponen yang Telah Diimplementasikan:

| ID | Nama Komponen | Style Glass (`ui/components/glass/`) | Style Raw (`ui/components/raw/`) | Status |
|---|---|---|---|---|
| ACT-01 | Primary Action Button | `button-glass/` | `button/` | `[stable]` |
| ACT-02 | Secondary / Ghost Button | `button-glass/` | `button/` | `[stable]` |
| ACT-03 | Floating Action Button (FAB) | `button-glass/` | `button/` | `[stable]` |
| ACT-04 | Icon Button | `button-glass/` | `button/` | `[stable]` |
| ACT-07 | Destructive Button | `button-glass/` | `button/` | `[stable]` |
| ACT-09 | Segmented Action Trigger | `thinking-effort-selector/` | `button/` | `[stable]` |
| INP-01 | Single-Line Text Input | `input-field-glass/` | `input/` | `[stable]` |
| INP-02 | Chat / Prompt Input Bar | `chat-input-bar/` | `input/` | `[stable]` |
| INP-04 | Search Input with Action | `input-field-glass/` | `input/` | `[stable]` |
| INP-05 | Password Input with Toggle | `input-field-glass/` | `input/` | `[stable]` |
| SEL-01 | Single & Multi Checkbox | `checkbox-glass/` | `checkbox-radio/` | `[stable]` |
| SEL-02 | Radio Selection Group | `checkbox-glass/` | `checkbox-radio/` | `[stable]` |
| SEL-03 | Toggle Switch Control | `toggle-switch-glass/` | `toggle-switch/` | `[stable]` |
| SEL-04 | Dropdown Select Menu | `dropdown-select-glass/` | `select-dropdown/` | `[stable]` |
| SEL-06 | Radio Selection Card | `ai-model-selector/` | `checkbox-radio/` | `[stable]` |
| DIS-01 | Frosted Folder Card | `frosted-folder-card/` | `details-accordion/` | `[stable]` |
| DIS-02 | Telemetry Metric Card | `aurora-storage-card/` | `progress-meter/` | `[stable]` |
| DIS-06 | Avatar with Status Badge | `avatar-badge-glass/` | - | `[stable]` |
| NAV-01 | Desktop Sidepanel Drawer | `glass-sidepanel/` | - | `[stable]` |
| NAV-08 | Horizontal Action Pills | `prompt-pills-row/` | - | `[stable]` |
| NAV-09 | Floating Navigation Dock | `glass-dock-navigation/` | - | `[stable]` |
| TAB-01 | Data Table | - | `table/` | `[stable]` |
| TEL-01 | Bar Activity Histogram | `telemetry-activity-chart/` | - | `[stable]` |
| TEL-03 | Linear Progress Bar | `progress-bar-glass/` | `progress-meter/` | `[stable]` |
| FDB-01 | Status Toast Notification | `toast-notification-glass/` | - | `[stable]` |
| FDB-03 | Micro Tooltip Indicator | `tooltip-glass/` | - | `[stable]` |
| OVL-01 | Centered Modal Dialog | `modal-dialog-glass/` | `modal-dialog/` | `[stable]` |
| OVL-02 | Bottom Sheet Drawer | `swirl-bottom-sheet/` | `modal-dialog/` | `[stable]` |
| SCE-01 | AI Agent Studio Scenery | `ai-agent-scenery/` | - | `[stable]` |
| SCE-02 | Cloud File Manager App | `ui/web/apps/file-manager/` | - | `[stable]` |

## 1. Taksonomi Hierarki Komponen

Komponen dikelompokkan berdasarkan metodologi desain hierarkis:
- **Atomic Primitives (Tunggal / Primitif)**: Komponen blok bangunan dasar yang tidak dapat dipecah lagi (Button, Input, Checkbox, Badge, Tooltip).
- **Molecules & Organisms (Molekul & Organisme)**: Kombinasi beberapa komponen primitif yang membentuk satu unit fungsional spesifik (Search Bar, Chat Input Bar, Model Selector Card, Telemetry Activity Chart, Sidepanel).
- **Sceneries (Komposit / Ruang Kerja Utuh)**: Tata letak pemandangan kerja lengkap siap pakai yang mengintegrasikan berbagai organisme dan alur UX (AI Assistant Studio, Cloud File Manager Workspace, Analytics Hub).

---

## Kategori 1: Actions & Triggers

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| ACT-01 | **Primary Action Button** | Atomic | Tombol pemicu aksi utama prioritas tertinggi pada layar. | Label teks, kontainer tombol, status focus/hover/active. | Submit form, Save, Create New, Checkout. |
| ACT-02 | **Secondary / Ghost Button** | Atomic | Tombol pendukung untuk aksi alternatif dengan bobot visual lebih ringan. | Label teks, outline atau latar belakang transparan. | Cancel, Dismiss, Back, Secondary actions. |
| ACT-03 | **Floating Action Button (FAB)** | Atomic | Tombol aksi cepat melayang di atas konten viewport. | Lingkaran/pill melayang, ikon tunggal, elevasi/bayangan. | Quick Compose, Add New, Quick Filter. |
| ACT-04 | **Icon Button** | Atomic | Tombol ringkas hanya berupa ikon tanpa label teks langsung. | Kontainer lingkaran/persegi, ikon vektor tunggal. | Toggle audio, close dialog, menu toggle, reload. |
| ACT-05 | **Split / Dropdown Button** | Molecule | Tombol aksi utama berdampingan dengan chevron pemilih opsi lanjutan. | Tombol aksi kiri + divider + tombol panah bawah kanan. | "Save" dengan opsi dropdown "Save as Draft". |
| ACT-06 | **Loading / Progress Button** | Atomic | Tombol yang menampilkan status tunggu/spinner saat proses asinkron berjalan. | Label yang berganti menjadi spinner atau progress bar mikro. | Async fetch, file upload submit, authentication. |
| ACT-07 | **Destructive / Danger Button** | Atomic | Tombol penegas aksi berisiko tinggi yang tidak dapat dibatalkan. | Aksen warna peringatan/merah, label tegas. | Delete account, Purge database, Format drive. |
| ACT-08 | **Copy to Clipboard Trigger** | Molecule | Tombol salin konten dengan feedback perubahan status seketika. | Ikon copy, label teks opsional, tooltip feedback konfirmasi. | Copy API key, copy code snippet, share link. |
| ACT-09 | **Segmented Action Trigger** | Molecule | Sekelompok tombol aksi terhubung horizontal untuk mode eksklusif. | Kontainer pembungkus, tombol-tombol bersebelahan, status aktif. | View mode (Grid vs List), format switcher. |
| ACT-10 | **Back to Top Trigger** | Atomic | Tombol melayang navigasi kembali ke puncak halaman panjang. | Ikon panah atas, sensor posisi scroll halaman. | Halaman dokumentasi panjang, feed berita. |

---

## Kategori 2: Text Inputs & Editors

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| INP-01 | **Single-Line Text Input** | Atomic | Bidang pengisian teks alfanumerik satu baris standar. | Kotak input, placeholder, status fokus, border feedback. | Input nama, judul proyek, kode pos. |
| INP-02 | **Chat / Prompt Input Bar** | Molecule | Baris komposer pesan percakapan cerdas dengan lampiran dan aksi kirim. | Input fleksibel, tombol attachment (+), tombol dikte (mic), tombol kirim. | Chat AI agent, komentar instan, messenger. |
| INP-03 | **Floating Label Input** | Molecule | Input dengan label yang bertransformasi ke atas saat bidang terisi/fokus. | Teks label dinamis, field input, border penegas. | Form registrasi modern, mobile design system. |
| INP-04 | **Search Input with Clear Action**| Molecule | Input pencarian dengan ikon kaca pembesar dan tombol reset cepat (x). | Ikon search di prefix, input teks, tombol clear di suffix. | Pencarian data, filter berkas, live catalog query. |
| INP-05 | **Password Input with Visibility Toggle** | Molecule | Input kata sandi terlindungi dengan opsi menampilkan karakter. | Input bertipe password, ikon mata toggle (reveal/hide). | Login akun, pengaturan keamanan kredensial. |
| INP-06 | **Auto-Growing Textarea** | Molecule | Area masukan teks multi-baris yang tingginya memanjang otomatis. | Kontainer teks multi-baris, penghitung karakter opsional. | Input deskripsi, feedback pengguna, postingan artikel. |
| INP-07 | **Formatted Masked Input** | Molecule | Input yang secara otomatis memformat pola karakter (telepon, kartu kredit). | Field input, regex pola masker, validasi live. | Input nomor telepon `(08xx)`, kartu pembayaran. |
| INP-08 | **OTP / Verification Pin Code**| Molecule | Kotak-kotak digit tunggal terpisah untuk verifikasi 2FA. | 4-6 kotak terpisah, auto-jump kursor, penanganan paste otomatis. | Verifikasi SMS OTP, otentikasi login email. |
| INP-09 | **Rich Text / Markdown Editor** | Organism | Area penulisan dengan toolbar formatting (Bold, Italic, Code, Link). | Toolbar aksi formatting, area editable, preview panel. | Penulisan catatan, editor dokumentasi, blog. |
| INP-10 | **Inline Editable Text** | Molecule | Teks biasa yang berubah menjadi input field saat diklik dua kali atau dihover. | Elemen teks statis, ikon pensil edit, input mode switch. | Rename nama folder, edit judul inline. |

---

## Kategori 3: Selection & Value Controls

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| SEL-01 | **Checkbox** | Atomic | Kotak centang pilihan majemuk independen (bisa pilih banyak). | Kotak pembungkus, ikon centang, label teks deskripsi. | Pilihan filter, seleksi berkas massal, persetujuan ToS. |
| SEL-02 | **Radio Button** | Atomic | Pemilih opsi tunggal eksklusif dalam satu kelompok pertanyaan. | Lingkaran konsentris, titik indikator aktif, label teks. | Pilihan metode pengiriman, jenis lisensi. |
| SEL-03 | **Radio Option Card (Selector Card)** | Molecule | Kartu pilihan besar interaktif dengan judul, subjudul, dan centang aktif. | Kontainer kartu, teks judul, deskripsi ringkas, checkmark indicator. | Pemilihan model AI (K3, Swarm, Instant), paket harga. |
| SEL-04 | **Toggle Switch** | Atomic | Saklar dua posisi geser untuk aktivasi/non-aktivasi fitur seketika. | Track jalur, knob bundar geser, status on/off. | Pengaktifan suara haptik, dark mode, auto-save. |
| SEL-05 | **Segmented Control** | Molecule | Tab pil terhubung horizontal untuk beralih mode secara eksklusif. | Kontainer pill pembungkus, opsi teks, slider latar aktif. | Thinking effort selector (Low/Medium/High), time range (1D/1W/1M). |
| SEL-06 | **Pill / Chip Filter Scroller** | Molecule | Kumpulan tag kapsul yang dapat di-scroll horizontal untuk penyaringan cepat. | Baris scrollable, chip kapsul, ikon prefix, status terpilih. | Kategori prompt cepat (Slides, Swarm, Code, Research). |
| SEL-07 | **Single Slider** | Atomic | Batang pengatur nilai numerik linier berkelanjutan. | Track garis dasar, fill nilai terisi, handle jempol (thumb). | Pengatur volume, zoom level, opacity percentage. |
| SEL-08 | **Dual-Handle Range Slider** | Molecule | Pengatur nilai rentang batas minimum dan maksimum secara bersamaan. | Track, fill di antara dua handle, dua handle thumb independen. | Filter rentang harga, ukuran file (0 MB s/d 100 GB). |
| SEL-09 | **Dropdown Select** | Molecule | Menu popover pemilihan item dari daftar vertikal tersembunyi. | Field pemicu, chevron panah, daftar item melayang. | Pilihan negara, kategori data, filter status. |
| SEL-10 | **Number Stepper** | Molecule | Input nilai angka dengan tombol penambah (+) dan pengurang (-) berdampingan. | Tombol minus di kiri, display angka, tombol plus di kanan. | Kuantitas item, pengatur timeout delay. |

---

## Kategori 4: Pickers & Droppers

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| PCK-01 | **File Drag-and-Drop Zone** | Molecule | Area penyeretan berkas dari sistem operasi ke dalam peramban web. | Kontainer dengan border putus-putus, ikon upload, teks panduan. | Pengunggahan file massal, lampiran dokumen. |
| PCK-02 | **Color Picker** | Molecule | Pemilih palet warna dengan visual roda spektrum, slider alpha, dan input hex. | Kanvas spektrum warna, slider hue/alpha, swatch preview, hex field. | Pengaturan tema personal, desain aset visual. |
| PCK-03 | **Date Picker** | Molecule | Kalender melayang interaktif untuk memilih hari, bulan, dan tahun. | Header navigasi bulan/tahun, grid 7 hari, penanda hari ini. | Tanggal tenggat tugas, filter rentang laporan. |
| PCK-04 | **Time Picker** | Molecule | Pemilih jam, menit, dan detik dengan dial lingkaran atau kolom scroll. | Dial jam atau list kolom jam:menit:detik, toggle AM/PM. | Penjadwalan reminder, booking meeting. |
| PCK-05 | **Font Picker** | Molecule | Dropdown pemilih tipografi dengan pratinjau langsung bentuk tulisan. | Daftar nama font, preview render teks asli, kategori sans/serif. | Pengaturan preferensi editor. |

---

## Kategori 5: Navigation & Hierarchy

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| NAV-01 | **Floating Dock Navigation** | Molecule | Bilah navigasi melayang horizontal dengan indikator posisi pegas. | Kontainer dock membulat, item navigasi berikon, indikator aktif geser. | Navigasi utama mobile & web app modern. |
| NAV-02 | **Sidepanel / Sidebar Navigation** | Organism | Panel vertikal tepi kiri/kanan untuk navigasi hierarki modul aplikasi. | Brand cluster, search input, grup menu navigasi, storage meter, profil. | Workspace dashboard desktop, console admin, file explorer. |
| NAV-03 | **Collapsible Rail Navigation** | Molecule | Sidebar mini ramping hanya memuat ikon vertikal yang bisa diperlebar. | Kolom ramping, ikon navigasi terpusat, tooltip nama saat hover. | Desktop layout hemat ruang, IDE interface. |
| NAV-04 | **Top App Bar / Header** | Molecule | Baris navigasi puncak aplikasi yang selalu tampak (sticky/fixed). | Identitas logo/brand, indikator status, tombol tindakan global. | Header website, navigation bar atas. |
| NAV-05 | **Breadcrumbs Bar** | Molecule | Penunjuk hierarki kedalaman lokasi halaman atau path folder saat ini. | Rantai tautan teks path, ikon separator pemisah (chevron/slash). | Navigasi struktur folder: Root > Documents > Projects. |
| NAV-06 | **Tabs Bar (Underline / Pill)** | Molecule | Pembagi tampilan konten dalam satu konteks halaman tanpa reload. | Daftar label tab sejajar, garis indikator aktif atau kapsul aktif. | Tabulasi halaman rincian (Overview, Details, Activity). |
| NAV-07 | **Numbered Pagination** | Molecule | Kontrol navigasi lembar halaman data banyak. | Tombol Previous/Next, nomor halaman aktif, tombol loncat halaman. | Hasil pencarian berlembar, galeri berkas panjang. |
| NAV-08 | **Context / Right-Click Menu** | Molecule | Menu aksi kontekstual yang muncul pada koordinat klik mouse. | Popover vertikal melayang, item opsi dengan ikon dan label shortcut. | Klik kanan pada file (Rename, Download, Delete). |
| NAV-09 | **Navigation Drawer (Slide-in)** | Organism | Laci menu navigasi yang meluncur keluar dari tepi viewport layar. | Overlay gelap latar belakang, panel geser, struktur menu hierarki. | Navigasi menu hamburger pada layar seluler. |
| NAV-10 | **Steps / Multi-Step Wizard** | Molecule | Penunjuk tahapan alur proses bertingkat linear. | Urutan node nomor tahapan, garis penghubung progresif, label judul. | Alur checkout, form registrasi bertahap, onboarding. |

---

## Kategori 6: Data Display & Containers

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| DSP-01 | **Folder Card (Container)** | Molecule | Kartu visual representasi folder direktori berkas dengan tab siluet. | Bentuk kontainer bertab, ikon jenis folder, label judul, kuota ukuran. | Grid file manager, galeri spaces. |
| DSP-02 | **Metric / KPI Stat Card** | Molecule | Kartu pemantau ringkas menampilkan metrik kunci, tren, dan perbandingan. | Angka statistik primer, label deskripsi kapital, tren persentase. | Total files, bandwidth terpakai, jumlah pengguna aktif. |
| DSP-03 | **Content Card** | Molecule | Kontainer kartu generik pembungkus konten modular. | Kontainer dengan border radius, header, body konten, footer aksi. | Kartu artikel, kartu produk, widget dashboard. |
| DSP-04 | **Avatar & Profile Cluster** | Molecule | Representasi visual identitas pengguna berupa foto atau inisial. | Gambar avatar melingkar, ring status online, label nama & peran. | Header profil, penanda kepemilikan berkas. |
| DSP-05 | **Accordion / Expandable Card**| Molecule | Kontainer lipat yang dapat diperluas atau disembunyikan per item. | Header pemicu, ikon chevron rotasi, panel konten yang melipat. | FAQ accordion, konfigurasi opsi lanjutan. |
| DSP-06 | **Carousel / Slide Viewer** | Organism | Komponen penampil geser horizontal dengan kontrol navigasi. | Track viewport, kartu-kartu konten berjejer, dot navigator. | Showcase portofolio, galeri screenshot. |
| DSP-07 | **Empty State Container** | Molecule | Komponen ramah yang ditampilkan saat suatu ruang atau daftar kosong. | Ilustrasi/ikon besar, pesan penjelas, tombol ajakan bertindak (CTA). | Folder kosong, hasil filter nol, belum ada notifikasi. |
| DSP-08 | **Key-Value Pair List** | Molecule | Daftar baris dua kolom menampilkan properti metadata dan nilainya. | Kolom kiri label redup, kolom kanan nilai data kontras. | Rincian properti berkas (Format, Dimensi, Dibuat pada). |
| DSP-09 | **Callout / Feature Banner** | Molecule | Kotak sorotan informasi penting dengan penanda garis aksen di tepi. | Aksen penanda tepi, ikon informasi, teks instruksi. | Catatan rilis versi, peringatan kebijakan sistem. |
| DSP-10 | **Badge / Tag Pill** | Atomic | Lencana mikro penanda status, kategori, atau kuantitas. | Kontainer kapsul mini, teks label ukuran kecil (10-12px). | Badge kategori "Beta", "Pro", jumlah revisi "v2.4". |

---

## Kategori 7: Tables, Lists & Trees

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| LST-01 | **Data Table with Sticky Header** | Organism | Tabel data multi-kolom dengan baris kepala tabel yang tetap membeku saat scroll. | Header kolom terurut, baris data zebra, sel data, checkbox multi-seleksi. | Daftar inventaris berkas, log transaksi. |
| LST-02 | **Divided Data List Item** | Molecule | Baris daftar berkas tunggal yang disusun vertikal dengan garis pemisah tipis. | Ikon tipe berkas, nama file, tanggal revisi, ukuran file, menu titik tiga. | Tampilan mode baris (List View) file manager. |
| LST-03 | **Hierarchical File Tree View** | Molecule | Penjelajah direktori bercabang dengan kemampuan ekspansi subfolder. | Indentasi bertingkat, ikon panah buka/tutup, nama node direktori. | Pohon berkas repositori kode, sidebar folder explorer. |
| LST-04 | **Activity Timeline** | Molecule | Linimasa vertikal kronologis kejadian peristiwa atau riwayat log. | Garis vertikal sumbu waktu, bulatan node kejadian, timestamp, deskripsi log. | Riwayat revisi dokumen, log audit aktivitas sistem. |
| LST-05 | **Comment & Chat Stream Thread** | Organism | Aliran percakapan pesan bersarang antara pengguna dan sistem/agen. | Gelembung pesan pengguna, gelembung respon sistem, avatar, timestamp. | Stream percakapan AI Assistant, kolom komentar tim. |

---

## Kategori 8: Telemetry, Charts & Gauges

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| CHT-01 | **Bar Activity Telemetry Chart** | Molecule | Diagram batang mini visualisasi volume beban komputasi per interval waktu. | Sekumpulan batang vertikal proporsional, hover tooltip, label interval. | Aktivitas lalu lintas data 12 jam terakhir, beban CPU. |
| CHT-02 | **Linear Gauge Progress Meter** | Atomic | Batang horizontal pengukur persentase kapasitas penyimpanan atau progres. | Track dasar gelap, fill indikator persentase, batas ambang kuota. | Pengukur kuota storage (cth: 70.1 GB dari 128 TB). |
| CHT-03 | **Radial Donut Gauge** | Molecule | Indikator lingkaran donat visualisasi pemakaian sumber daya. | Lingkaran busur SVG dinamis, nilai persentase di titik pusat. | Pengukur pemakaian memori RAM, baterai tersisa. |
| CHT-04 | **Sparkline Trend Graph** | Molecule | Garis grafik mini tanpa sumbu untuk melihat pola tren naik/turun sekilas. | Garis vektor SVG halus, area gradien pudar di bawah garis. | Fluktuasi kecepatan transfer data jaringan. |
| CHT-05 | **Multi-Segment Stacked Bar** | Molecule | Batang progres terbagi warna untuk membedakan porsi kategori data. | Segmen-segmen warna berbeda, legend keterangan jenis data. | Pembagian jenis file (Media, Gambar, Dokumen, Lainnya). |

---

## Kategori 9: Feedback & Status Indicators

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| FDB-01 | **Status Indicator Dot** | Atomic | Bulatan kecil warna penanda ketersediaan koneksi atau server. | Lingkaran 6-8px, warna hijau/kuning/merah, efek denyut (pulse). | Status online AI swarm, server heartbeat status. |
| FDB-02 | **Counter Badge** | Atomic | Lencana angka notifikasi yang melekat di sudut elemen lain. | Kontainer lingkaran/pill mikro, angka kuantitas belum dibaca. | Unread notifications, item di dalam keranjang/folder. |
| FDB-03 | **Floating Toast Notification** | Molecule | Pesan konfirmasi mengambang sementara di atas layar yang menghilang otomatis. | Kontainer melayang, ikon hasil aksi, pesan singkat, tombol tutup/aksi. | Konfirmasi "Folder berhasil dibuat", "Koneksi terputus". |
| FDB-04 | **Inline Banner Alert** | Molecule | Spanduk informasi atau peringatan yang tertanam permanen di dokumen. | Kontainer dengan aksen warna status (Info, Warning, Error), teks penjelas. | Peringatan kapasitas hampir penuh, pengumuman pemeliharaan. |
| FDB-05 | **Skeleton Shimmer Loading** | Atomic | Kotak tiruan beranimasi denyut sebelum data sebenarnya selesai dimuat. | Bentuk geometris abu-abu, animasi gelombang kilau cahaya horizontal. | Placeholder saat loading kartu folder, daftar berkas. |
| FDB-06 | **Tooltip** | Atomic | Kotak keterangan mikro yang muncul sesaat saat kursor melayang di atas elemen. | Kontainer kecil, teks instruksi 1 baris, panah penunjuk target. | Menjelaskan arti tombol ikon yang tidak berlabel. |
| FDB-07 | **Circular Loading Spinner** | Atomic | Indikator putaran melingkar penanda proses tunggu. | Busur lingkaran SVG yang berputar tanpa henti secara kontinu. | Menunggu respon analitik AI, proses komputasi lokal. |

---

## Kategori 10: Overlays, Sheets & Modals

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| OVL-01 | **Bottom Sheet Modal** | Organism | Panel modal yang meluncur naik dari tepi bawah layar menutupi sebagian viewport. | Handle geser atas, lencana header, form isian, tombol aksi ganda. | Form buat folder baru, filter popup di perangkat bergerak. |
| OVL-02 | **Center Dialog Modal** | Molecule | Kotak modal melayang di tengah viewport dengan latar belakang gelap. | Header modal, tombol close (x), area konten, baris tombol konfirmasi. | Dialog konfirmasi hapus data, modal otentikasi. |
| OVL-03 | **Slide-Over Side Drawer** | Organism | Panel lembar inspeksi yang meluncur dari tepi samping kanan layar penuh. | Header judul, panel pratinjau konten, tab metadata rincian, aksi unduh. | Detail inspeksi properti berkas, panel pengaturan akun. |
| OVL-04 | **Interactive Popover Menu** | Molecule | Panel menu melayang yang muncul terikat langsung pada elemen pemicunya. | Titik tumpu pemicu, kontainer popover, daftar pilihan aksi. | Menu opsi dropdown, pemilih filter kustom. |
| OVL-05 | **Backdrop / Scrim** | Atomic | Lapisan tirai peredup di seluruh viewport saat overlay modal aktif. | Lapisan penutup layar penuh, transparansi gelap, pemicu klik tutup. | Latar belakang modal untuk memfokuskan atensi pengguna. |
| OVL-06 | **Media Lightbox Modal** | Organism | Penampil berkas media (gambar, video) ukuran penuh layar dengan latar redup. | Viewport gambar terpusat, kontrol zoom, tombol navigasi prev/next. | Pratinjau fullscreen hasil gambar AI. |

---

## Kategori 11: Layout Primitives & Utilities

| ID | Nama Komponen | Level | Deskripsi & Fungsi | Anatomi / Elemen Penyusun | Kasus Penggunaan Utama |
|---|---|---|---|---|---|
| LAY-01 | **Divider / Separator** | Atomic | Garis tipis pembatas visual pemisah antar seksi atau item daftar. | Garis linier horizontal atau vertikal dengan ketebalan 1px. | Pemisah grup menu, pemisah baris tabel. |
| LAY-02 | **Resizable Split Panel** | Molecule | Pembagi layar dua kolom yang batas tengahnya dapat digeser kursor mouse. | Panel kiri, divider pegangan geser (drag handle), panel kanan. | Tampilan editor kode & live preview berdampingan. |
| LAY-03 | **Custom Scroll Area** | Molecule | Kontainer pembungkus konten panjang dengan scrollbar kustom halus. | Viewport overflow, track scrollbar, thumb pegangan scroll. | Area daftar menu panjang, log terminal output. |
| LAY-04 | **Aspect Ratio Box** | Atomic | Kontainer yang mempertahankan rasio lebar dan tinggi secara proporsional. | Wrapper kontainer dengan perhitungan padding-top atau CSS aspect-ratio. | Thumbnail video 16:9, folder card 1:1, kartu pratinjau. |

---

## Kategori 12: Sceneries & Composite Patterns

*Scenery adalah kesatuan utuh berbagai organisme menjadi satu ruang kerja fungsional:*

| ID | Nama Scenery | Organisme Penyusun Utama | Alur & Tujuan Pengalaman Pengguna (UX) |
|---|---|---|---|
| SCN-01 | **AI Agent Studio Scenery** | Top Nav Bar + Model Selector Card + Thinking Effort Row + Greeting + Quick Prompt Pills + Chat Input Bar. | Pengguna dapat memilih model AI yang diinginkan, mengatur kedalaman penalaran, memilih aksi cepat, dan berinteraksi via teks/suara dalam satu tampilan percakapan terpadu. |
| SCN-02 | **Cloud File Manager Scenery** | Top Nav Bar + Storage Telemetry Card + Recent Spaces Header + Frosted Folder Grid + Quick FAB Action + Floating Dock Navigation. | Pengguna dapat memantau kapasitas penyimpanan awan, menjelajahi folder ruang kerja, membuat direktori baru dengan cepat, dan bernavigasi antar modul. |
| SCN-03 | **System Telemetry & Optimizer Scenery** | KPI Stat Cards + 12-Hour Activity Bar Chart + One-Tap Deep Clean Action + Telemetry Timestamp Tooltips. | Pengguna dapat menginspeksi beban aktivitas komputasi berkas, mendeteksi penumpukan cache, dan melakukan pembersihan memori sistem dengan satu ketukan. |
| SCN-04 | **Productivity Desktop Workspace Scenery** | Glass Sidepanel (Brand, Search, Navigation List, Storage Meter) + Main Grid Workspace Content + Breadcrumb Bar. | Pengguna pada layar lebar desktop mendapatkan navigasi sisi komprehensif untuk berpindah direktori, memfilter berkas, dan memantau status sistem secara paralel. |
| SCN-05 | **Preferences & System Settings Scenery** | Header Back Navigation + Card Kategori Pengaturan + Baris Toggle Switch + Slider Preferensi + Info Versi Sistem. | Pengguna dapat mengatur preferensi audio haptik, kualitas efek grafis sistem, tema visual, dan melihat informasi versi build aplikasi. |

---

## 📌 Catatan Implementasi Desain

Dokumen ini sengaja disusun **bebas dari keterikatan tema gaya spesifik**.
- Untuk spesifikasi token warna, efek kaca, multi-layer blur, dan shader noise dari tema **Glass Dark Premium**, lihat file panduan desain di: [ui/components/glass/STYLE_SPEC.md](file:///d:/PROJECT/prototype/ui/web/components/glass/STYLE_SPEC.md).
- Untuk mencoba dan menguji setiap komponen secara interaktif dalam bentuk nyata, buka dashboard showcase terpadu di: [showcase.html](file:///d:/PROJECT/prototype/showcase.html).
