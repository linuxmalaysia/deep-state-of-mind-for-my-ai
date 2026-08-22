---
okf_version: 0.2
type: guide
title: "Nota Lapangan: Panduan Praktikal Pasukan untuk AI Antigravity & DSOM Bersama Cikgu Haris"
timestamp: "2026-08-22T17:18:00Z"
topics: ["antigravity", "gemini", "dsom", "ansible", "gitops", "skills", "jules", "panduan-pasukan"]
description: "Sintesis nota lapangan praktikal, strategi model, automasi kemahiran (skills), dan disiplin GitOps DSOM untuk perkongsian bersama rakan sepasukan."
resource: "file:///docs/tutorials/NOTA-LAPANGAN-ANTIGRAVITY-DSOM.md"
sources: ["docs/tutorials/TEAM-DSOM-MASTERCLASS.md", "START-HERE.md", ".agents/AGENTS.md"]
generated: "google-antigravity"
verified: true
status: "active"
stale_after: "2027-08-22T00:00:00Z"
---

# 📝 Nota Lapangan: Panduan Praktikal AI Antigravity & Protokol DSOM
### *(Berdasarkan Sesi Perkongsian & Bimbingan Cikgu Haris / LinuxMalaysia)*

> **Sasaran:** Jurutera Perisian, Pentadbir Sistem (SysAdmin), Jurutera DevOps, dan Ahli Pasukan Teknikal.  
> **Tujuan:** Panduan rujukan pantas dwibahasa (Bahasa Melayu Piawai DBP & Standard UK English) untuk memahami cara bekerja secara efektif bersama AI Agent (Google Antigravity, Gemini Pro, Claude Sonnet, Google Jules) berlandaskan protokol **Deep State of Mind (DSOM)**.

---

## 📌 Ringkasan Eksekutif & Minda Asas (*Core Mindset*)

Dalam pembangunan moden berbantukan AI, **AI bukan pengganti kepakaran manusia, sebaliknya bertindak sebagai Pengganda Produktiviti (*Productivity Multiplier*) dan Kembar Kognitif Digital (*Cognitive Digital Twin*)**.

Masalah terbesar apabila bekerja dengan AI ialah **kehilangan ingatan (*context window amnesia*)** dan **halusinasi arahan terminal (*silent destructive actions*)**. Melalui protokol DSOM dan penggunaan Google Antigravity Desktop, kita membina pagar keselamatan (*guardrails*) dan ingatan kekal (*spatial memory*).

---

## 🎯 1. Pengurusan Model & Kos Token (*Model Strategy & Token Budgeting*)

| Model | Kegunaan & Peranan | Karakteristik & Tip Penggunaan |
| :--- | :--- | :--- |
| **Gemini Pro (Default)** | **Pilihan Utama (*Workhorse*)** | Keseimbangan terbaik antara kepantasan, kefahaman kod, dan kecekapan token. Digunakan untuk 80–90% tugasan harian. |
| **Claude Sonnet** | **Penaakulan Kompleks (*High-Wisdom*)** | Digunakan apabila menghadapi *architectural refactoring*, pepijat (*bugs*) rumit, atau analisis mendalam. Menggunakan lebih banyak bajet token. |
| **Model Terbuka / Percuma (Flash Lite / OSS)** | **Tugasan Ringan & Pengekstrakan** | Sangat jimat token; sesuai untuk semakan sintaks asas, penukaran format data, atau carian dokumen ringkas. |

> [!TIP]
> **Petua Jimat Token:** Jangan muat naik keseluruhan kod (*codebase*) ke dalam chat! Gunakan format metadata **Open Knowledge Format (OKF)** YAML di bahagian atas fail `.md` supaya AI hanya membaca ringkasan ~50 token berbanding 500,000 token teks penuh kod mentah.

---

## 🧠 2. Mengatasi Sifat 'Lupa' AI Melalui Git Sovereignty

AI tidak mempunyai ingatan jangka panjang melainkan kita menyediakan struktur ingatan fizikal:

1. **Komit Git yang Kerap & Berbutir (*Atomic Commits*):**
   - Arahkan AI untuk membuat `git commit` bagi setiap perubahan logik yang lengkap.
   - *Contoh Prompt:* `"Sahkan kod dengan ujian unit, kemudian komit fail yang diubah dengan mesej semantik discrete git commit."`
   - Elakkan arahan pukal `git commit -am` yang mencampurkan semua fail tanpa kawalan.

2. **Gunakan Perintah `/learn` untuk Mengekalkan Ingatan:**
   - Setiap kali anda membetulkan kesilapan AI atau menghasilkan corak kerja yang bagus, taipkan `/learn`.
   - Antigravity akan menyusun fail `learning_proposal.md` untuk mengabadikan peraturan (*rules*) atau kemahiran (*skills*) tersebut.
   - **Pencerahan:** Ciri `/learn` terbina di peringkat platform Antigravity IDE (bukan sekadar bergantung kepada akaun berbayar), membolehkan pembaikan diserap terus ke dalam fail SOP tempatan.

---

## 📁 3. Struktur Direktori Projek yang Kemas (*6-Pillar Minimal Footprint*)

Untuk memastikan ruang kerja sentiasa bersih dan difahami oleh mana-mana AI, wujudkan struktur folder standard ini:

```text
my-project/
├── .agents/
│   ├── AGENTS.md             <-- Perlembagaan & undang-undang AI (29 Rules)
│   ├── brain/                <-- Ingatan spatial (task.md, walkthrough.md)
│   └── skills/               <-- Kemahiran projek tempatan (SOP berekod)
├── docs/                     <-- Dokumentasi rasmi & output dokumen AI
│   ├── governance/           <-- Polisi teknikal & garis panduan
│   └── tutorials/            <-- Panduan langkah demi langkah
├── references/               <-- Tempat letak dokumen rujukan mentah (PDF/Specs)
├── tools/                    <-- Skrip automasi & Git Pre-Commit Guardrails
├── .cursorrules              <-- Gateway untuk Cursor IDE
├── CLAUDE.md                 <-- Gateway untuk Claude Desktop
├── START-HERE.md             <-- Peta orientasi onboarding pasukan
└── README.md / CHANGELOG.md  <-- Lejar universal
```

* **Folder `references/`:** Tempat meletakkan fail PDF spesifikasi, dokumen arkitek lama, atau nota perbincangan.
* **Folder `docs/`:** Tempat AI menulis, menyusun, dan menyimpan analisis teknikal dalam format Markdown `.md`.

---

## 🛡️ 4. Disiplin Pelaksanaan Perintah: Ansible Playbook vs Terminal Terus

> [!CAUTION]
> **Undang-Undang Utama Keselamatan:** Jangan sesekali membenarkan AI menjalankan perintah bahaya secara terus (*raw terminal commands*) di atas pelayan pengeluaran (*production server*)!

1. **Jadikan Ansible Playbook sebagai Lejar Operasi:**
   - Arahkan AI: *"Jangan run command terus. Bina satu Ansible Playbook yang idempoten untuk laksanakan konfigurasi ini."*
2. **Kelebihan Pendekatan Ini:**
   - **Boleh Diulang (*Idempotent*):** Boleh diuji berkali-kali tanpa merosakkan sistem.
   - **Terdokumentasi dalam Git:** Setiap arahan tercatat rapi dalam repositori sebagai rekod audit.
   - **Keselamatan Terjamin:** Manusia boleh menyemak (*peer review*) setiap tugasan YAML sebelum dimainkan ke pelayan sasaran (`ansible-playbook -i hosts playbook.yml --check`).

---

## ⚙️ 5. Menukar Tugasan Berulang Menjadi *Skills* (AI SOPs)

Apabila anda dapati ada tugasan yang berulang (contoh: format dokumen DOCX, suntik tandatangan lesen, kira token):

1. **Berikan Arahan Penukaran (*Skill Creation Prompt*):**
   ```markdown
   Turn this successful workflow and script into a reusable DSOM agent skill.
   Create a folder under `.agents/skills/<skill-name>/` containing `SKILL.md` with OKF v0.2 frontmatter.
   ```
2. **Lokasi Penyimpanan *Skills*:**
   * **Global / Pengguna:** `~/.gemini/antigravity/builtin/skills/` (Tersedia merentas semua projek).
   * **Projek Tempatan (*Recommended*):** `<project-root>/.agents/skills/<skill-name>/SKILL.md` (Tersimpan dalam Git projek, membolehkan seluruh pasukan berkongsi kemahiran yang sama).

---

## 🤝 6. Kolaborasi Multi-Agent: Google Jules & Antigravity

* **Google Jules (Cloud Autonomous Agent):**
  * Bertindak di latar belakang (*asynchronous background agent*) melalui GitHub.
  * Menjalankan audit isu, pembaikan pepijat (*bug fixing*), atau pembinaan ciri baharu dalam *pull request* (PR) berasingan.
* **Google Antigravity (Local Interactive Twin):**
  * Digunakan untuk pengaturcaraan berpasangan (*pair-programming*), semakan kod, dan ujian unit tempatan.
* **Protokol Segerak Selamat (*Safe Rebase Sync*):**
  Sebelum menarik perubahan yang dibuat oleh Jules, elakkan konflik dengan arahan GitOps bertahan:
  ```powershell
  # Windows PowerShell / Bash
  git stash
  git pull --rebase origin main
  git stash pop
  ```

---

## 📋 Senarai Semak Harian Pasukan (*Team Daily Checklist*)

- [ ] **Mula Sesi (SOD):** Buka Antigravity dan baca status tugasan daripada `.agents/brain/task.md`.
- [ ] **Semasa Membangunkan Ciri:** Wujudkan fail rancangan pelaksanaan (`implementation_plan.md`) sebelum menulis kod besar.
- [ ] **Sebelum Komit:** Jalankan ujian unit tempatan (`uv run pytest`) untuk memastikan 100% lulus.
- [ ] **Tamat Sesi (EOD):** Jana blok ringkasan `[DSOM EPISODIC RECORD]` supaya rakan sepasukan atau sesi AI esok hari dapat menyambung kerja dengan sifar amnesia.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-22*  
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
