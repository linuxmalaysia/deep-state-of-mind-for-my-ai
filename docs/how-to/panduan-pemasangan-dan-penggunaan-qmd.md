---
okf_version: 0.2
type: how-to
title: "Panduan Lengkap Enjin Carian QMD (Quick Markdown Search)"
timestamp: "2026-10-11T05:38:00Z"
topics: ["qmd", "search-engine", "embeddings", "vector-search", "bm25", "mcp", "wsl2"]
resource: "file:///docs/how-to/panduan-pemasangan-dan-penggunaan-qmd.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}]
status: stable
generated: {by: google-jules, timestamp: "2026-10-11T05:38:00Z"}
stale_after: "2027-10-11"
spec_version: "0.2"
description: "Panduan lengkap pemasangan, seni bina berbilang projek, pengindeksan bertahap (incremental indexing), automasi cron, dan integrasi Model Context Protocol (MCP) untuk enjin carian QMD."
verified: true
concept_id: panduan_pemasangan_dan_penggunaan_qmd
---
# Panduan Lengkap Enjin Carian QMD (Quick Markdown Search)

> **Persekitaran:** Linux WSL2 (Ubuntu 24.04 / Node.js 22+)
> **Klasifikasi:** Sistem Carian Tempatan Berdaulat (Sovereign On-Device Search)
> **Lokasi Indeks:** `~/.cache/qmd/index.sqlite` (SQLite + FTS5 + sqlite-vec)
> **Model AI Tempatan:** embeddinggemma-300M (Vektor), Qwen3-Reranker-0.6B (Penyusunan Semula), QMD Query Expansion 1.7B (Pengembangan Pertanyaan)

---

## 1. Pengenalan & Ciri Utama QMD

**QMD (Quick Markdown Search)** ialah enjin carian hibrid tempatan (*on-device hybrid search engine*) yang direka khas untuk fail Markdown dan kod sumber. Ia menggabungkan:
1. **Carian Leksikal (BM25):** Padanan kata kunci pantas tanpa memerlukan GPU/LLM (`qmd search`).
2. **Carian Semantik Vektor:** Carian konsep berasaskan makna teks menggunakan model benaman padat GGUF (`qmd vsearch`).
3. **Carian Hibrid + Reranking (Disyorkan):** Menggabungkan skor leksikal dan vektor dengan Reciprocal Rank Fusion (RRF) serta penarafan semula menggunakan model *reranker* (`qmd query`).
4. **Integrasi MCP (Model Context Protocol):** Menyediakan antara muka protokol standard untuk ejen AI (Antigravity, Cursor, Claude Code) mencari dan membaca dokumen tanpa membaca keseluruhan fail.

---

## 2. Pemasangan & Persediaan Awal (Installation)

### A. Keperluan Sistem
- Node.js versi 22 atau ke atas (`node -v`).
- Direktori npm global tanpa hak akses root (`~/.npm-global`).
- Pakej kompilasi sistem (pilihan, jika sqlite-vec memerlukan binaan tempatan): `build-essential`.

### B. Langkah Pemasangan Melalui NPM
```bash
# 1. Konfigurasi direktori npm global pengguna (elakkan sudo)
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'

# 2. Masukkan ke dalam PATH (~/.bashrc)
export PATH="$HOME/.npm-global/bin:$PATH"

# 3. Pasang pakej qmd secara global
npm install -g @tobil/qmd

# 4. Sahkan pemasangan
qmd --help
```

### C. Muat Turun Model AI Tempatan (GGUF)
QMD menggunakan model tempatan bersaiz padat yang disimpan dalam format GGUF:
```bash
qmd pull
```
Model yang dimuat turun merangkumi:
- `embeddinggemma-300M-GGUF` (Penjanaan vektor benaman)
- `Qwen3-Reranker-0.6B-Q8_0-GGUF` (Penarafan semula ketepatan carian)
- `qmd-query-expansion-1.7B-gguf` (Pengembangan semantik pertanyaan)

---

## 3. Seni Bina Berbilang Projek (Multi-Project Separation)

Bagi mengelakkan kekeliruan hasil carian (*cross-project clutter*), setiap projek diasingkan menggunakan koleksi tersendiri (*project-scoped collections*):

```
                     ~/.cache/qmd/index.sqlite
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
  [ oss-docs ]            [ cbc-mcmc-docs ]       [ aws-php-docs ]
  qmd://oss-docs/         qmd://cbc-mcmc-docs/    qmd://aws-php-docs/
  (Projek Ini)            (Projek CBC MCMC)       (Projek AWS PHP)
        │                       │                       │
        ▼                       ▼                       ▼
  [ oss-agents ]          [ cbc-mcmc-agents ]     [ aws-php-agents ]
  qmd://oss-agents/       qmd://cbc-mcmc-agents/  qmd://aws-php-agents/
```

### A. Mendaftarkan Koleksi Projek
Setiap direktori didaftarkan dengan nama unik:
```bash
# Contoh mendaftarkan dokumentasi dan ejen projek:
qmd collection add /path/to/project/docs --name oss-docs
qmd collection add /path/to/project/.agents --name oss-agents

# Tambah ringkasan konteks manusia (Context Summary)
qmd context add qmd://oss-docs/ "Dokumentasi teknikal, panduan tadbir urus kedaulatan, tutorial, dan senarai arkib"
qmd context add qmd://oss-agents/ "Perlembagaan ejen AI, memori spatial istana, senarai tugas, dan kemahiran khusus"
```

### B. Memeriksa Status Koleksi
```bash
# Senarai ringkas koleksi
qmd collection list

# Status kesihatan indeks dan jumlah fail/vektor
qmd status
```

---

## 4. Pengindeksan Bertahap & Efisien (Incremental Indexing)

QMD menggunakan semakan cap masa (*mtime*) dan cincangan SHA-256 bagi setiap dokumen:
- Fail yang **tidak berubah TIDAK AKAN diindeks semula** dan TIDAK AKAN dijana semula vektornya.
- Hanya fail yang **baru ditambah atau diubah suai** sahaja yang diproses.

### A. Arahan Pengindeksan Harian / Manual:
```bash
# 1. Imbas fail baru, ubah suai, atau padam merentas semua koleksi (sangat pantas, ~1-2 saat):
qmd update

# 2. Jana vektor untuk blok teks (chunks) baharu sahaja:
qmd embed

# 3. (Pilihan) Bersihkan vektor yatim daripada fail yang telah dipadam:
qmd cleanup
```

---

## 5. Automasi Berkala (Hourly Cron Sync di WSL2)

Bagi memastikan dokumen sentiasa terindeks secara automatik tanpa memerlukan arahan manual, skrip automasi dan entri crontab telah disediakan:

### A. Lokasi Skrip Automasi (`~/.local/bin/qmd-sync-hourly.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
LOG_FILE="$HOME/.local/var/log/qmd-sync.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Starting QMD incremental update ===" >> "$LOG_FILE"
if command -v qmd >/dev/null 2>&1; then
    qmd update >> "$LOG_FILE" 2>&1 || true
    qmd embed >> "$LOG_FILE" 2>&1 || true
fi
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === QMD incremental update completed ===" >> "$LOG_FILE"
```

### B. Konfigurasi Crontab
Dijalankan pada minit ke-0 setiap jam:
```cron
0 * * * * /home/$USER/.local/bin/qmd-sync-hourly.sh
```

---

## 6. Kaedah Penggunaan & Carian (Usage Workflows)

### A. Carian Khusus Projek (Scoped Search - Disyorkan)
Gunakan bendera `-c <koleksi>` untuk mengecilkan skop carian hanya pada projek semasa:
```bash
# 1. Carian Hibrid (Gabungan kata kunci + makna + penarafan semula):
qmd query "gitea podman setup postgresql" -c oss-docs

# 2. Carian Kata Kunci Pantas (BM25 - tiada beban CPU):
qmd search "container-postgresql-1.service" -c oss-docs

# 3. Carian Semantik Murni:
qmd vsearch "bagaimana memulihkan pangkalan data selepas reboot" -c oss-docs
```

### B. Carian Merentas Semua Projek (Global Search)
Apabila mencari corak yang pernah dibuat dalam mana-mana projek:
```bash
qmd query "weasyprint pure white css"
```

### C. Mengambil & Membaca Kandungan Dokumen
```bash
# Baca dokumen dengan nombor baris
qmd get qmd://oss-docs/how-to/GITEA-POSTGRESQL-PODMAN-SETUP.md

# Baca baris tertentu (contoh: baris 10 hingga 30)
qmd get qmd://oss-docs/how-to/GITEA-POSTGRESQL-PODMAN-SETUP.md:10:20
```

---

## 7. Integrasi Ejen AI Melalui FastMCP (`mcp_config.json`)

QMD menyokong Model Context Protocol (MCP) secara terbina dalam melalui arahan `qmd mcp` (stdio transport).

### Konfigurasi Ejen Antigravity (`~/.gemini/config/mcp_config.json`):
```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

Alatan yang disediakan kepada ejen AI:
- `query`: Carian hibrid dengan hujah `query` dan `collection`.
- `get`: Membaca dokumen atau julat baris dokumen.
- `multi_get`: Mengambil banyak dokumen serentak menggunakan corak glob.
- `status`: Memeriksa integriti pangkalan data dan senarai koleksi berdaftar.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-10-11*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
