# GlassOS Autonomous UI Generator Pipeline

Arsitektur generator otonom, pipeline kurasi komponen UI, dan integrasi cloud Google Apps Script (GAS) untuk ekosistem **GlassOS Dark Glass**.

---

## 🏛️ Arsitektur Sistem

```
                 DIRECTIVE & POLICY
                         ↓
                  DECISION ENGINE
          (Klasifikasi Intent, Kategori, Tag)
                         ↓
                 GENERATION ENGINE
                         ↓
                   MODEL ROUTER
          (Gemini → 9Router → Mock Cascade)
                         ↓
                      GENERATE
                         ↓
                 DECOMPILER ENGINE
          (HTML → HTML + CSS + JS + Manifest)
                         ↓
                     VALIDATOR
          (Token Glass, Size, Semantik, ARIA)
                         ↓
                    DEDUPLICATOR
          (Similarity Memory vs UI Eksisting)
                         ↓
                  REVIEW QUEUE
           (Pending Review Limit: 100)
                         ↓
                   HUMAN CURATOR
                  /             \
          APPROVE                 REJECT
             ↓                       ↓
    Pasang ke /ui/glass         Arsip ke /rejected
    Rebuild Showcase
```

---

## 📂 Struktur Direktori

```text
generator/
├── config/
│   ├── policy.json         # Aturan wajib & batasan desain
│   ├── directive.md        # Prompt direktif otonom sistem
│   └── models.json         # Konfigurasi model & cascade priority
├── engine/
│   ├── decision_engine.py  # Layer klasifikasi intent & variasi
│   ├── model_router.py     # Router provider dengan auto-cooldown
│   ├── generator_engine.py # Generator prompt assembler
│   ├── decompiler.py       # Single-file HTML to modular extractor
│   ├── validator.py        # Quality gate & token validation
│   ├── deduplicator.py     # Similarity memory checker
│   └── queue_manager.py    # Pengelola siklus hidup antrean
├── curation/
│   └── curator.py          # CLI & automated deployment engine
├── gas/
│   └── Code.gs             # Google Apps Script cloud bridge
├── queue/
│   ├── pending/            # Komponen menunggu kurasi manusia
│   ├── approved/           # Komponen yang telah disetujui
│   └── rejected/           # Komponen yang ditolak
├── runner.py               # CLI entrypoint utama
└── README.md
```

---

## 🔒 Keamanan & Pemisahan Secrets (Zero Hardcoded Keys)

1. **Repo Publik Bebas Kredensial**:
   - Repository ini **TIDAK PERNAH** menyimpan API key, token, atau webhook secret.
   - Kredensial provider dibaca dari environment variables:
     - `GEMINI_API_KEY`: Kunci API Google Gemini.
     - `ROUTER_API_KEY`: Kunci API 9Router / OpenAI-compatible endpoint.
2. **Google Apps Script Security**:
   - Seluruh secret cloud disimpan pada `PropertiesService.getScriptProperties()` di Google Apps Script console, bukan di berkas `Code.gs`.
3. **Offline / Mock Fallback Provider**:
   - Generator dilengkapi `mock` provider bawaan sehingga dapat dijalankan, diuji, dan dieksekusi 100% secara offline tanpa memerlukan koneksi API berbayar.

---

## ⚡ Panduan Penggunaan CLI

### 1. Menghasilkan Komponen Tunggal
```powershell
# Menggunakan prompt spesifik
python -m generator.runner generate --prompt "Floating Glass Input Field with Aurora Glow"

# Menggunakan provider tertentu (misal offline mock)
python -m generator.runner generate --prompt "Aurora Glass Pill Badge" --provider mock

# Langsung approve dan pasang ke design system (untuk developer)
python -m generator.runner generate --prompt "Glass Toast Alert" --provider mock --auto-approve
```

### 2. Menjalankan Loop Otonom Kontinu
```powershell
# Menjalankan 3 siklus generasi otonom
python -m generator.runner run --max-iterations 3 --delay 2

# Menjalankan loop kontinu (berhenti jika antrean pending mencapai 100)
python -m generator.runner run --continuous --delay 5
```

### 3. Kurasi Manusia (Review Queue)
```powershell
# Menampilkan statistik antrean
python -m generator.runner curate --stats

# Menampilkan daftar komponen yang menunggu review
python -m generator.runner curate --list

# Menyetujui dan memasang komponen ke ui/components/glass/
python -m generator.runner curate --approve <ITEM_ID>

# Menolak komponen
python -m generator.runner curate --reject <ITEM_ID> --reason "Desain terlalu mirip komponen lama"
```
