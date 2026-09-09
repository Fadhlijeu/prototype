Saya sudah audit repo `Fadhlijeu/prototype` yang sekarang ada di GitHub, termasuk `generator/`, `Code.gs`, `generator.yml`, queue lifecycle, curator, prompt builder, dan run GitHub Actions terbaru. Kesimpulannya: **masalahnya bukan satu bug; ada 3 lapisan yang sekarang tidak konsisten: state persistence, curation lifecycle, dan diversity engine.**

## 1. Diagnosis utama

### A. APPROVE sebenarnya belum memiliki persistence yang benar-benar aman

Di Python, `approve_and_deploy()` melakukan:

1. copy kandidat ke `ui/components/glass/{slug}`
2. pindahkan pending → approved
3. modifikasi `scripts/rebuild_all.py`
4. jalankan rebuild

Itu terlihat benar di working directory runner. ([GitHub][1])

Tetapi **Python tersebut sendiri tidak melakukan commit/push**. Commit/push baru dilakukan oleh GitHub Actions sesudahnya. Workflow memang mempunyai step `git commit` + `git push`.

Masalahnya ada pada robustness step push:

```bash
for i in 1 2 3 4 5; do
  git pull --rebase origin main && git push origin main && break || sleep 3
done
```

Kalau **kelima push gagal**, loop selesai setelah `sleep 3` dan workflow tidak secara eksplisit `exit 1`. Artinya workflow bisa berakhir **Success walaupun perubahan belum pernah masuk ke `main`**.

Ini sangat cocok dengan gejala kamu: UI/Actions terlihat sukses, tetapi setelah refresh repository/deploy kembali ke keadaan lama.

Dan memang run terbaru `generate_task #12` pada 8 September 2026 tercatat **Success**, menghasilkan Pages artifact 367 KB, tetapi GitHub UI tidak memperlihatkan detail log tanpa login. ([GitHub][2])

### B. Ada race condition antara "state lokal runner" dan GitHub sebagai source of truth

Architecture sekarang:

```text
GAS
 ↓ repository_dispatch
GitHub Actions
 ↓ checkout
Python generator
 ↓ modify working tree
git commit
 ↓ push
main
 ↓ GitHub Pages
```

Secara konsep bagus.

Tetapi UI Generator Lab membaca `projects/generator-lab/queue.json`, sementara state sebenarnya tersebar di:

```text
generator/queue/pending/
generator/queue/approved/
generator/queue/rejected/
projects/generator-lab/queue.json
ui/components/glass/
scripts/rebuild_all.py
```

Tidak ada satu authoritative state store.

Workflow generate juga langsung `git add -A` terhadap queue + generated component + manifest + registry.

Jadi ketika satu event datang saat commit lain belum settle, yang kamu dapat bisa seperti:

```text
UI bilang Approved
        ↓
dispatch berhasil
        ↓
runner checkout commit lama
        ↓
item belum ada / atau state tidak sama
        ↓
workflow tetap bisa terlihat berhasil
        ↓
refresh → state lama muncul lagi
```

**Ini yang harus dihilangkan.**

---

# 2. BUG REJECTED: ini sudah jelas 100% dari source

Ini bukan dugaan.

`QueueManager.reject()` saat ini secara eksplisit mengatakan:

```python
"""Completely deletes/purges item from pending queue (hapus total)."""
```

lalu:

```python
shutil.rmtree(src, ignore_errors=True)

rej_path = os.path.join(self.rejected_dir, item_id)

if os.path.exists(rej_path):
    shutil.rmtree(rej_path, ignore_errors=True)

return "purged"
```

Artinya:

```text
PENDING
   ↓ reject
DELETE
   ↓
tidak ada rejected item
```

Bukan:

```text
PENDING → REJECTED
```

Jadi wajar halaman rejected kosong. Bahkan folder `rejected/` tidak pernah mendapatkan candidate tersebut. ([GitHub][3])

Lebih buruk lagi, tidak ada rejection archive yang menyimpan:

```text
item_id
reason
prompt
model
variation
created_at
rejected_at
files
similarity
```

Padahal data seperti itu sangat berguna sebagai **negative memory** untuk generator.

---

# 3. Kenapa setelah refresh hasil rejected muncul lagi?

Ini efek gabungan state persistence.

GAS hanya mengirim:

```text
reject_task
item_id
```

ke GitHub Actions. ([GitHub][4])

Workflow kemudian menjalankan:

```bash
python -m generator.runner curate --reject "$ITEM_ID"
```

dan setelah itu menjalankan rebuild + git commit/push.

Masalahnya:

```text
reject()
   ↓
hapus pending
   ↓
tidak ada rejected archive
   ↓
commit
```

Kalau commit/push gagal, repository tetap menyimpan pending item lama.

Pada refresh:

```text
GitHub repository
     ↓
queue.json lama
     ↓
item muncul lagi
```

Jadi gejala kamu:

> "yang dihapus pasti kembali lagi"

sangat konsisten dengan desain state sekarang.

---

# 4. APPROVE juga sebenarnya punya bug desain

Ada bagian yang cukup berbahaya:

```python
approved_dir = self.queue.approve(item_id)
```

baru kemudian:

```python
self._register_in_rebuild_script(...)
```

dan rebuild. ([GitHub][1])

Tetapi return result akhir hanya:

```python
"success": True
```

walaupun `rebuild_all.py` gagal.

Karena exception rebuild ditangkap:

```python
except Exception as e:
    rebuild_output = f"Rebuild warning: {str(e)}"
```

lalu fungsi **tetap return success=True**. ([GitHub][1])

Jadi bisa terjadi:

```text
Approve
 ↓
copy component ✅
 ↓
move approved ✅
 ↓
register ✅
 ↓
rebuild ❌
 ↓
return success=True
```

Itu harus diubah menjadi transactional.

---

# 5. Masalah diversity ternyata memang ada di generator

Ini bagian paling penting.

Prompt kamu sudah mencoba memaksa variasi:

> DO NOT generate another generic 440px rectangular card...

dan memberi beberapa geometry/palette berdasarkan kategori. ([GitHub][5])

Tetapi saya justru melihat beberapa hal yang menyebabkan model cenderung **collapse ke pola yang sama**.

### Problem 1 — prompt terlalu preskriptif

Di `generator_engine.py`, model diperintahkan secara keras:

```text
controls → pill
sliders → track
buttons → radial/FAB
telemetry → circular arc
navigation → capsule dock
dashboards → wide multi-pane
inputs → prompt bar
```

Ini bagus untuk consistency, tapi buruk untuk eksplorasi.

Akibatnya model belajar:

```text
CATEGORY = controls
→ pill

CATEGORY = telemetry
→ circular gauge

CATEGORY = buttons
→ glowing button/card
```

Jadi variasinya hanya terjadi pada **skin**, bukan pada **design architecture**. ([GitHub][5])

---

### Problem 2 — GAS hanya punya 2 prompt per kategori

Contohnya slider hanya:

```text
Aurora Magnetic Precision Slider
Refraction Density Optical Scrubber
```

Telemetry hanya dua konsep, controls dua konsep, dst.

Kemudian:

```javascript
var idx = Math.floor(Math.random() * prompts.length);
return prompts[idx];
```

Artinya secara teori kamu cuma punya **2 prompt per kategori** sebelum pengulangan.

Random bukan diversity engine.

---

### Problem 3 — palette juga di-hardcode menurut kategori

Mock generator bahkan memiliki palette fixed:

```text
telemetry → cyan/emerald
sliders → blue/indigo
buttons → pink/violet
controls → emerald/mint
navigation → indigo/violet
...
```

([GitHub][6])

Jadi walaupun bentuk berubah sedikit, warna, radius, width, aurora structure, dan material language tetap sangat terikat kategori.

---

### Problem 4 — emergency fallback ke mock dapat membuat hasil "selalu sama"

Ini bagian yang saya anggap **sangat penting**.

Router kamu secara eksplisit melakukan:

```python
if not available_models:
    available_models = [mock]
```

dan bila seluruh provider gagal:

```python
fallback_output = self._call_mock(...)
```

lalu mengembalikan:

```text
mock-emergency-fallback
```

([GitHub][6])

Sedangkan mock generator adalah generator template/deterministik berbasis kategori. ([GitHub][6])

Jadi ketika API:

```text
Gemini gagal
↓
9Router gagal
↓
TokenRouter gagal
↓
Mock
```

kamu tetap mendapatkan hasil "valid", sehingga terlihat seolah AI bekerja.

Padahal yang menghasilkan mungkin justru **mock generator**.

Ini harus diperbaiki:

```text
provider failure
    ≠
silently generate mock
```

Untuk production generator, harus:

```text
provider failure
→ status ERROR / RETRY
→ jangan masuk review queue
```

Mock hanya boleh diaktifkan eksplisit:

```text
provider=mock
```

---

# 6. Temperatur 0.7 juga bukan solusi diversity

Real model sekarang menggunakan:

```json
"temperature": 0.7
```

baik Gemini maupun OpenAI-compatible provider. ([GitHub][6])

0.7 bukan masalah utama.

Masalah utamanya adalah:

```text
same constraints
+
same category
+
same design vocabulary
+
same examples
+
same geometry rules
+
same palette rules
```

Temperature tidak akan mengubah "design space" secara signifikan.

---

# 7. Solusi yang saya rekomendasikan: jangan pakai "prompt generator", bikin "Design Variation Engine"

Arsitektur generator sebaiknya menjadi:

```text
USER DIRECTIVE
      ↓
DESIGN INTENT
      ↓
VARIATION GENOME
      ↓
EXEMPLAR RETRIEVAL
      ↓
CREATIVE BRIEF
      ↓
LLM
      ↓
STRUCTURAL ANALYSIS
      ↓
NOVELTY SCORING
      ↓
VALIDATOR
      ↓
QUEUE
      ↓
HUMAN APPROVAL
```

Bukan:

```text
prompt
 ↓
AI
 ↓
HTML
```

---

# 8. "Baca glass.md / glass_style.md, buat serupa tapi bervariasi" justru harus menjadi prompt utama

Saya setuju dengan arah yang kamu inginkan.

Generator sebaiknya diberi directive semacam:

Read and understand the project's design references before generating anything.

Primary references:

- `glass.md`
- `glass_style.md`
- `ui/components/glass/STYLE_SPEC.md`
- `ui/components/glass/css.css`
- existing components inside `ui/components/glass/`

The references define the visual language, material quality, interaction quality, and design-system constraints.

DO NOT copy an existing component.
DO NOT produce a near-duplicate.
DO NOT simply rename, recolor, resize, or rearrange an existing component.

Your task is to create a NEW design direction that belongs to the same design family.

Preserve:

- material language
- visual polish
- glass quality
- lighting logic
- typography discipline
- interaction quality
- accessibility
- design-system compatibility

Vary aggressively:

- silhouette
- geometry
- spatial composition
- information hierarchy
- component anatomy
- interaction model
- control placement
- layering strategy
- edge treatment
- depth model
- optical/refraction behavior
- motion language
- iconography
- density
- proportions
- orientation
- visual rhythm
- color harmony
- accent strategy

A generated component may be:

- horizontal
- vertical
- radial
- floating
- nested
- asymmetric
- modular
- split-pane
- stacked
- orbital
- timeline-like
- dial-like
- ribbon-like
- mesh-like
- spatial
- compact
- oversized

Do not assume the component must be a rectangular card.

Use existing components as STYLE REFERENCES, not STRUCTURAL TEMPLATES.

Before writing code, internally decide:

1. What makes this component visually distinct?
2. What is its unique geometry?
3. What is its unique interaction model?
4. What is its unique spatial composition?
5. What is its unique color strategy?
6. What existing components does it resemble?
7. How will you deliberately avoid resembling them?

The final result must feel like:
"same design universe, completely different invention."

Generate a production-quality standalone HTML component with working CSS and JavaScript.

Prioritize originality over superficial variation.

It jauh lebih tepat dengan filosofi repo kamu sendiri: **"Satu Komponen, Beragam Rupa"**. ([GitHub][7])

---

# 9. Tambahkan "variation genome"

Setiap generation harus punya JSON internal seperti:

```json
{
  "geometry": "radial-orbital",
  "composition": "asymmetric-split",
  "density": "compact",
  "orientation": "vertical",
  "interaction": "magnetic-drag",
  "depth": "layered-refraction",
  "motion": "spring + orbit",
  "material": "frosted-crystal",
  "accent": "amber-cyan",
  "lighting": "bottom-up-specular",
  "border": "directional",
  "shape_language": "organic",
  "surface": "semi-transparent",
  "information_architecture": "metric-cluster",
  "novelty_target": 0.82
}
```

Generation berikutnya **tidak boleh memakai genome yang sama**.

Dengan ini:

```text
AI tidak hanya diberi prompt
AI diberi ruang desain yang berbeda.
```

---

# 10. Pakai existing components sebagai dataset, bukan prompt dump

Sekarang generator memang membaca exemplar components. ([GitHub][5])

Tapi jangan hanya:

```text
Here are existing components...
```

Lebih baik ekstrak setiap exemplar menjadi:

```json
{
  "slug": "...",
  "category": "...",
  "geometry": "...",
  "layout": "...",
  "interaction": "...",
  "radius": "...",
  "dominant_palette": "...",
  "depth_style": "...",
  "animation_style": "...",
  "surface_type": "...",
  "structural_signature": "..."
}
```

Kemudian generator mencari:

```text
same aesthetic
+
different structural signature
```

bukan meniru HTML mentah.

---

# 11. Deduplicator sekarang terlalu lemah untuk tugas ini

Sekarang dedup check dilakukan terhadap slug/title:

```python
check_similarity(spec["slug"], spec["title"])
```

dan existing names.

Itu tidak akan mendeteksi:

```text
Component A:
Glass rectangular card + radial gradient + glowing button

Component B:
Glass rectangular card + different title + different text
```

Secara nama berbeda.

Yang harus dibandingkan adalah **design fingerprint**:

```text
DOM tree shape
CSS selector topology
layout model
geometry
radius
aspect ratio
palette
gradient count
shadow structure
interaction primitives
animation primitives
SVG composition
canvas usage
```

Kemudian:

```text
Novelty Score
0.00 = duplicate
0.25 = minor mutation
0.50 = moderate variation
0.75 = clearly different
0.90+ = structurally novel
```

Dan threshold misalnya:

```text
< 0.60 → reject automatically
0.60–0.78 → regenerate
> 0.78 → eligible for human review
```

Ini jauh lebih efektif daripada sekadar slug dedup.

---

# 12. REJECTED harus menjadi permanent archive

Ubah:

```python
reject()
```

menjadi:

```text
pending/{id}
      ↓
rejected/{id}
```

dan simpan:

```text
rejected/
 └── 1757xxxx-component-name/
      ├── index.html
      ├── index.css
      ├── index.js
      ├── component.html
      ├── manifest.json
      └── rejection.json
```

`rejection.json`:

```json
{
  "item_id": "1757...",
  "status": "REJECTED",
  "reason": "Too similar to existing telemetry components",
  "rejected_at": "2026-09-09T...",
  "similarity_score": 0.81,
  "similar_to": "telemetry-activity-chart"
}
```

Kemudian halaman:

```text
Generator Lab
├── Pending
├── Approved
└── Rejected
```

semuanya membaca satu manifest:

```json
{
  "pending": [],
  "approved": [],
  "rejected": []
}
```

Jangan lagi hanya `queue.json` yang merepresentasikan pending. Saat ini memang `export_web_manifest()` secara eksplisit hanya mengekspor pending items. ([GitHub][3])

---

# 13. Buat state machine yang benar

Saya akan ubah menjadi:

```text
GENERATING
    ↓
VALIDATING
    ↓
NOVELTY_CHECK
    ↓
PENDING_REVIEW
   ↙      ↘
APPROVED  REJECTED
   ↓         ↓
PUBLISHED   ARCHIVED
```

Bukan filesystem sebagai state machine.

`queue_meta.json` harus menjadi authoritative status.

Contoh:

```json
{
  "item_id": "...",
  "status": "APPROVED",
  "version": 3,
  "created_at": "...",
  "updated_at": "...",
  "approved_at": "...",
  "rejected_at": null,
  "published_commit": "62e4999",
  "published_path": "ui/components/glass/..."
}
```

---

# 14. Approve harus transactional

Idealnya:

```text
validate item exists
↓
lock item
↓
copy to target
↓
rebuild
↓
verify target
↓
verify showcase
↓
verify links
↓
git commit
↓
git push
↓
verify remote contains item
↓
mark APPROVED/PUBLISHED
```

Bukan:

```text
move state
→ copy
→ mungkin rebuild
→ mungkin commit
```

Dan `success=True` tidak boleh diberikan sebelum publish benar-benar selesai.

---

# 15. Perbaiki git push

Current:

```bash
git pull --rebase origin main && git push origin main && break || sleep 3
```

harus menjadi semacam:

```bash
set -e

git config user.name "Prototype Autonomous Bot"
git config user.email "bot@prototype.local"

git add -A \
  generator/queue/ \
  projects/generator-lab/ \
  ui/components/glass/ \
  scripts/rebuild_all.py \
  component.md \
  web-apps.html

if git diff --cached --quiet; then
  echo "No changes."
  exit 0
fi

git commit -m "feat(generator): update component lifecycle"

for i in 1 2 3 4 5; do
  git fetch origin main
  git rebase origin/main || git rebase --abort

  if git push origin HEAD:main; then
    echo "Push succeeded."
    exit 0
  fi

  sleep $((i * 3))
done

echo "ERROR: Unable to push after 5 attempts."
exit 1
```

Yang paling penting:

```text
5x gagal = workflow FAILED
```

bukan Success.

---

# 16. Dan jangan biarkan "mock" diam-diam menggantikan AI

Saya sangat menyarankan mengubah:

```python
if all providers fail:
    use mock
```

menjadi:

```text
Production
   ↓
provider failure
   ↓
retry another provider
   ↓
all fail
   ↓
QUEUE ERROR
```

Mock hanya:

```bash
python -m generator.runner generate ... --provider mock
```

Karena sekarang kamu bisa dengan mudah mengira:

```text
Gemini generated component
```

padahal:

```text
Gemini failed
9Router failed
TokenRouter failed
↓
mock-glass-generator-v1
```

dan ini secara langsung menjelaskan kenapa output bisa terasa sangat repetitif. ([GitHub][6])

---

# 17. Ada satu lagi: continuous generation kamu belum benar-benar menjadi "creative autonomous loop"

Current CLI memang punya:

```bash
run --continuous
```

tetapi seed-nya cuma lima:

```text
Floating glass telemetry dial
Specular breadcrumb
Obsidian segmented visualizer
Aurora notification banner
Magnetic slider
```

lalu:

```python
seed_prompt = seeds[iterations % len(seeds)]
```

Artinya setelah 5 cycle, seed kembali ke awal.

Untuk visi kamu:

> "Baca glass.md / glass_style.md, buat sesuatu yang serupa tapi bervariasi dan kreatif"

lebih tepat:

```text
REFERENCE LIBRARY
      ↓
GENERATION MEMORY
      ↓
NOVELTY ENGINE
      ↓
DESIGN GENOME RANDOMIZER
      ↓
CREATE
      ↓
ANALYZE RESULT
      ↓
UPDATE MEMORY
      ↓
NEXT DESIGN
```

Jadi **generation #100 mengetahui generation #1–99**.

Bukan hanya:

```text
random.choice(seeds)
```

---

# 18. Final architecture yang saya rekomendasikan

```text
                 ┌────────────────────┐
                 │ Google Apps Script │
                 └──────────┬─────────┘
                            │
                            ▼
                  repository_dispatch
                            │
                            ▼
               ┌─────────────────────────┐
               │ GitHub Actions Runner   │
               └────────────┬────────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       Reference      Generation       Negative
        Library         Genome          Memory
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                     Creative Brief
                            │
                            ▼
                         LLM Pool
             Gemini / Router / other providers
                            │
                            ▼
                       HTML/CSS/JS
                            │
                            ▼
                     Decompiler
                            │
                            ▼
                    Structural Analyzer
                            │
                            ▼
                    Novelty + Quality
                       /         \
                    fail          pass
                     │              │
                 regenerate      pending
                                   │
                            ┌──────┴──────┐
                            ▼             ▼
                         APPROVE       REJECT
                            │             │
                            ▼             ▼
                       PUBLISHED       ARCHIVED
                            │             │
                            └──────┬──────┘
                                   ▼
                              git commit
                                   │
                                   ▼
                              git push
                                   │
                                   ▼
                             GitHub Pages
```

## Prioritas perbaikannya

| Priority | Masalah                                                  | Status                                      |
| -------- | -------------------------------------------------------- | ------------------------------------------- |
| **P0**   | `reject()` menghapus item                                | **Bug pasti**                               |
| **P0**   | Git push failure bisa tetap Success                      | **Bug pasti**                               |
| **P0**   | `success=True` walaupun rebuild gagal                    | **Bug pasti**                               |
| **P0**   | Pending/approved/rejected tidak satu authoritative state | **Arsitektur rapuh**                        |
| **P1**   | Mock fallback terlalu silent                             | **Sangat mungkin penyebab hasil monoton**   |
| **P1**   | hanya 2 prompt/category di GAS                           | **Menyebabkan repetisi**                    |
| **P1**   | palette/geometry terlalu category-locked                 | **Membatasi creative space**                |
| **P1**   | dedup berbasis nama/slug                                 | **Tidak mendeteksi visual duplicate**       |
| **P1**   | continuous loop cuma 5 seed berulang                     | **Tidak cocok untuk autonomous generation** |

Jadi saya tidak akan menyelesaikan ini hanya dengan **"buat prompt lebih kreatif"**. Prompt kamu sekarang sudah cukup panjang; masalahnya adalah generator masih **terlalu template-driven** dan lifecycle-nya **belum transactional**.

Yang paling penting: **repo saat ini sebenarnya sudah punya fondasi bagus**. `generator.yml` sudah menerima `generate_task`, `approve_task`, dan `reject_task`, sudah memiliki `contents: write`, rebuild, commit/push, dan Pages deployment. Jadi tidak perlu bongkar total; yang perlu dilakukan adalah memperbaiki state machine dan mengganti diversity layer dari random prompt menjadi **persistent creative/novelty engine**.

Untuk live deployment, saya berhasil QA sisi GitHub Actions—termasuk run terbaru yang sukses dan menghasilkan Pages artifact—tetapi endpoint GitHub Pages-nya sendiri tidak bisa saya inspeksi dari environment web ini, jadi saya tidak akan mengklaim telah memverifikasi UI live secara visual. ([GitHub][2])

[1]: https://github.com/Fadhlijeu/prototype/blob/main/generator/curation/curator.py "prototype/generator/curation/curator.py at main · Fadhlijeu/prototype · GitHub"
[2]: https://github.com/Fadhlijeu/prototype/actions/runs/34270627193 "generate_task · Fadhlijeu/prototype@62e4999 · GitHub"
[3]: https://github.com/Fadhlijeu/prototype/blob/main/generator/engine/queue_manager.py "prototype/generator/engine/queue_manager.py at main · Fadhlijeu/prototype · GitHub"
[4]: https://github.com/Fadhlijeu/prototype/blob/main/generator/gas/Code.gs "prototype/generator/gas/Code.gs at main · Fadhlijeu/prototype · GitHub"
[5]: https://github.com/Fadhlijeu/prototype/blob/main/generator/engine/generator_engine.py "prototype/generator/engine/generator_engine.py at main · Fadhlijeu/prototype · GitHub"
[6]: https://github.com/Fadhlijeu/prototype/blob/main/generator/engine/model_router.py "prototype/generator/engine/model_router.py at main · Fadhlijeu/prototype · GitHub"
[7]: https://github.com/Fadhlijeu/prototype/tree/main/ui "prototype/ui at main · Fadhlijeu/prototype · GitHub"

Ketemu. Mari saya audit langsung Generator Lab (tempat approve/reject terjadi) dan generator inti-nya.# Audit: Fadhlijeu/prototype — GlassOS UI Generator Lab

Sudah saya telusuri repo dan versi live-nya (`fadhlijeu.github.io/prototype/projects/generator-lab/`). Arsitekturnya sekarang jelas:

**Stack yang terpasang:**

- **Frontend**: GitHub Pages statis (Generator Lab UI di `projects/generator-lab/index.html`)
- **Backend AI**: Google Apps Script Web App (URL disimpan di `sessionStorage` browser), dilindungi `ADMIN_PASSKEY` via Script Properties, dengan model cascade Gemini 3.5 Lite → TokenRouter GLM
- **Auto-deploy**: opsional GitHub Personal Access Token (juga di `sessionStorage`) yang _seharusnya_ memicu GitHub Actions untuk build & deploy ke `showcase.html`
- **State kurasi**: Pending / Approved (Showroom) / Rejected — tiga counter terpisah di UI

Ini penting: **tidak ada satu sistem terpusat**. Ada 3 sistem yang harus saling "nyambung" lewat JS di browser — Apps Script, GitHub API, dan file statis di repo. Titik putus paling mungkin ada di sambungan-sambungan ini, bukan di satu tempat.

---

## Masalah 1 & 2: Approve tidak commit, Reject tidak persist

Dua masalah ini kemungkinan besar **satu akar yang sama**: UI melakukan _optimistic update_ (langsung menghilangkan/memindahkan kartu di layar) tanpa mengonfirmasi request ke backend benar-benar sukses.

**Kandidat penyebab paling umum untuk kombinasi Apps Script + fetch dari domain lain:**

1. **CORS preflight gagal diam-diam.** Kalau kode JS mengirim `fetch()` ke Web App URL dengan `Content-Type: application/json`, browser akan mengirim preflight `OPTIONS` dulu. Google Apps Script Web App **tidak punya handler `doOptions()` bawaan** — preflight itu gagal, request POST asli tidak pernah terkirim, tapi promise-nya kadang tetap "resolve" ke state UI karena tidak ditangani dengan benar. Efeknya persis seperti yang Anda alami: di layar terlihat berhasil, tapi server tidak pernah menerima perintahnya → refresh mengembalikan data asli.
   - **Cek**: buka DevTools → Network tab saat klik Setujui/Tolak. Kalau ada request `OPTIONS` berwarna merah/failed sebelum POST, ini penyebabnya.
   - **Fix**: kirim body sebagai `text/plain;charset=utf-8` (bukan `application/json`) ke Apps Script — ini trik standar untuk menghindari preflight, lalu `JSON.parse()` manual di sisi `doPost(e)`.

2. **Approve hanya menandai status di backend, tidak memicu rebuild.** Saya lihat di README ada perintah eksplisit:

   ```
   npm run rebuild   # Sinkronisasi ulang database showcase & web-apps
   ```

   Ini sangat mengindikasikan `showcase.html` **bukan** file yang langsung ditulis saat approve — dia hasil generate dari semacam "database" komponen. Kalau step rebuild ini tidak otomatis dipicu (lewat GitHub Actions on-push, misalnya) setelah komponen baru di-commit, maka file baru bisa masuk ke repo tapi `showcase.html` tidak pernah ikut ter-update.
   - **Cek**: tab Actions di GitHub — apakah ada workflow run setelah Anda approve? Kalau tidak ada run sama sekali, trigger-nya belum jalan. Kalau ada run tapi merah (failed), buka log-nya — biasanya karena PAT scope kurang (butuh `repo` + `workflow`) atau `permissions: contents: write` belum di-set di file workflow.

3. **Reject tidak pernah menulis balik ke sumber data.** Kalau "Pending Review" di-load ulang dari Apps Script/Sheet setiap refresh, tapi tombol Reject cuma `array.splice()` di memori JS lokal — ya pasti balik lagi. Reject **harus** memanggil endpoint yang menulis status "rejected" ke sumber data yang sama dipakai untuk populate antrean, bukan cuma menghilangkan elemen dari DOM.

**Langkah verifikasi cepat**: buka Network tab, klik Setujui satu komponen, lihat apakah request ke Apps Script URL benar-benar dapat response 200 dengan body sukses — bukan cuma "request terkirim". Kalau responsnya error atau tidak ada sama sekali, itu titik masalahnya.

---

## Masalah 3: Hasil generate selalu mirip

Ini yang paling bisa saya konfirmasi langsung — saya baca `ui/components/glass/STYLE_SPEC.md`, dan ini **kemungkinan besar akar masalahnya**.

Spec Anda menulis token desain sebagai **nilai literal persis**, bukan sebagai sistem aturan dengan rentang:

- Warna aksen: `--accent-blue-1: #4A7BF7` dst — nilai hex tunggal, bukan palet pilihan
- Aurora blob: posisi & rgba persis (`circle at 30% 50%, rgba(70,110,220,0.6)...`) — bukan formula/rentang acak
- Gradient tombol: `135deg, #4A7BF7 0%, #2E5FD9 50%, #1E3A8A 100%` — angka pasti

Kalau spec ini di-inject apa adanya ke prompt AI (yang hampir pasti terjadi, karena README bilang skill ini jadi acuan tunggal untuk gaya "Glass Dark"), maka model LLM apa pun — Gemini atau GLM — akan **meniru nilai contoh itu hampir persis**, karena itu satu-satunya referensi konkret yang diberikan. Ini perilaku LLM yang sangat umum: kalau contoh yang diberi berupa nilai pasti, output akan menempel ke nilai itu, bukan berimprovisasi.

**Solusinya bukan menulis prompt "lebih baik" — tapi mengubah struktur spec itu sendiri:**

1. **Ubah token tunggal jadi palet pilihan.** Ganti `--accent-blue-1: #4A7BF7` dengan daftar 6–8 opsi hue (biru, ungu, teal, amber, rose, dst), dan instruksikan AI memilih satu secara acak per generate — jangan biarkan satu nilai jadi "default" yang selalu dipakai.
2. **Ubah posisi/opacity aurora blob jadi rentang**, bukan angka pasti. Misal: `posisi X: 20–80%, opacity: 0.4–0.7` — beri formula, bukan snapshot.
3. **Suntikkan elemen acak eksplisit ke prompt tiap panggilan**, misalnya seed/nonce angka acak + instruksi "jangan gunakan hex code yang sama dengan 3 generate terakhir" (kirim ringkasan output terakhir sebagai negative example).
4. **Naikkan temperature/top_p** di parameter API call ke Gemini/GLM — kalau default-nya rendah (banyak SDK pakai ~0.2–0.4 secara default), hasil akan cenderung deterministik walau prompt-nya berbeda.
5. **Tegaskan di prompt**: "Nilai di STYLE_SPEC ini ilustrasi arah mood saja — kamu WAJIB menciptakan hex/posisi baru yang berbeda, bukan menyalin persis." Larangan (`DILARANG gradien linier`) sudah bagus karena itu aturan struktural — tapi nilai contoh yang menyertainya perlu ditandai eksplisit sebagai "jangan disalin".

---

## Ringkasan prioritas perbaikan

1. **Cek Network tab dulu** — ini paling cepat mengonfirmasi apakah Approve/Reject benar-benar sampai ke server atau gagal diam-diam di CORS preflight
2. **Pastikan ada trigger otomatis untuk `npm run rebuild`** setelah approve (lewat GitHub Actions `on: push` atau `workflow_dispatch` yang dipicu Apps Script)
3. **Rombak STYLE_SPEC.md dari nilai literal → sistem rentang/palet pilihan acak**, plus naikkan temperature API call

Kalau Anda mau, saya bisa bantu tulis ulang draf `STYLE_SPEC.md` versi "parametrized" (dengan palet & rentang, bukan nilai pasti) yang siap Anda tempel ke prompt AI-nya — itu perbaikan dengan dampak paling langsung untuk masalah #3.
