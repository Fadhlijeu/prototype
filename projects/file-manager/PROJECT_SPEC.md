# Project Specification: Cloud File Manager

> Proyek aplikasi terintegrasi berbasis tema **Glass Dark Premium** untuk manajemen berkas awan (*Cloud File Manager*) dan asisten produktivitas AI.

---

## 1. Ikhtisar Proyek
- **Nama Proyek**: Cloud File Manager
- **File Utama**: [`index.html`](file:///d:/PROJECT/prototype/projects/file-manager/index.html)
- **Tema Desain**: Glass Dark Premium (Multi-layered Glass, Symmetrical Lighting, Aurora Mesh, Noise Textures)
- **Target Perangkat**: Responsif (Mobile-first 375px–480px, Tablet & Desktop Widescreen)

---

## 2. Komponen yang Digunakan

Proyek ini menggabungkan komponen-komponen berikut dari katalog sistem:

| Komponen | Level | Peran & Penempatan | Detail Desain & Interaksi |
|---|---|---|---|
| **Symmetrical Top Bar** | Molecule | Header aplikasi | Menampilkan logo brand, live status indicator, audio synthesizer mute toggle, dan menu pemicu settings. |
| **AI Model Selector** | Molecule | Tab Home | Kartu selector interaktif untuk memilih antara model `K3`, `K3 Swarm`, dan `Instant` dengan checkmark aktif beranimasi spring. |
| **Thinking Effort Row** | Molecule | Tab Home | Pengatur tingkat penalaran (*Low, Medium, High*) dengan indikator teks cyan. |
| **Prompt Quick Pills** | Molecule | Tab Home | Baris pil aksi cepat (*Slides, Swarm, Websites, Deep Research*) yang langsung mengisi chat bar. |
| **Glass Chat Input Bar** | Molecule | Tab Home | Bar input chat kaca melayang dengan tombol tambah lampiran (+), simulasi dikte suara (mic), dan tombol kirim pesan. |
| **Aurora Storage Card** | Molecule | Tab Folders | Kartu status kapasitas memori 5 layer dengan aurora mesh gradient dinamis, twinkle plus marks, dan progress gauge bar. |
| **Frosted Glass Folders Grid** | Molecule | Tab Folders | Grid kartu folder berkas kaca dengan tab siluet SVG `#folder-shape`, highlight tepi glossy stroke, dan efek hover 3D tilt. |
| **12-Hour Activity Telemetry** | Molecule | Tab Clean | Diagram batang analitik aktivitas berkas 12 jam dengan bar hover tooltip dan live sync status. |
| **One-Tap Deep Clean CTA** | Atomic | Tab Clean | Tombol optimasi penyimpanan dengan animasi pembersihan cache 2.4 GB dan pembaruan gauge kapasitas. |
| **Floating Glass Dock** | Molecule | Navigasi Bawah | Dock navigasi bawah melayang 74px dengan latar kaca, tekstur noise SVG, dan active pill spring physics. |
| **Floating Action Button (FAB)** | Atomic | Navigasi Bawah | Tombol terpisah 60px bergradasi biru dengan ikon plus outline 26px untuk membuka modal pembuatan folder. |
| **Swirl Refraction Bottom Sheet** | Organism | Modal Dialog | Modal sheet meluncur dari bawah dilengkapi Canvas 2D swirl refraction filter, lencana ikon 3D melayang, dan form input folder baru. |
| **Web Audio Synthesizer** | Utility | Audio Feedback | Generator suara sintetis (pop, chime, tap) berbasis native AudioContext tanpa file MP3 eksternal. |

---

## 3. Spesifikasi Gaya (Style Implementation)
- **Background**: `#08090C` dengan 3 ambient floating blurred blobs di background.
- **Glass Base**: `rgba(36, 36, 38, 0.55)` dengan `backdrop-filter: blur(28px) saturate(160%)`.
- **Borders**: Asymmetric light edge (`border-top: rgba(255,255,255,0.35)`, `border-left: 0.22`, `border-bottom: 0.06`, `border-right: 0.08`).
- **Iconography**: 100% Outline Stroke `1.5px` (Lucide Icons & Phosphor Outline).
- **Noise Overlay**: SVG `feTurbulence` dengan opacity `0.04` pada dock dan modal.
- **Spring Curves**: `cubic-bezier(0.34, 1.1, 0.64, 1)` untuk pergerakan pill dock dan tombol.
