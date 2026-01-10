# 🛡️ GitHub Copilot Integration Protocol (UK English & DBP)

Dokumen ini menjelaskan cara mengkonfigurasi GitHub Copilot supaya mematuhi kerangka kerja **DSOM** secara automatik dan manual.

## ⚙️ 1. Konfigurasi Automatik (.github)
Copilot secara automatik akan membaca fail arahan jika ia diletakkan di lokasi yang betul.

* **Lokasi Fail:** `.github/copilot-instructions.md`
* **Fungsi:** Menetapkan undang-undang DSOM, penggunaan **UK English**, dan **Bahasa Melayu Malaysia (DBP)** sebagai arahan sistem kekal.

## 💬 2. Penggunaan Manual dalam Chat
Untuk memastikan Copilot mempunyai konteks yang tepat semasa sesi chat, gunakan rujukan fail (mentions) berikut:

### Teknik Mentions (#)
Apabila bertanya dalam Chat, sertakan fail 'Brain' sebagai rujukan:
> "Based on **#file:.agent/brain/task.md** and **#file:.agent/brain/walkthrough.md**, what is the next logical step for the sitemap implementation?"

### Penggunaan Arahan Workspace (@workspace)
Gunakan `@workspace` untuk bertanya soalan merentas keseluruhan struktur repositori:
> "**@workspace** explain how the DSOM laws are enforced in this project using UK English."

## 📜 3. Pintasan Reanimasi (/reanimate)
Gunakan fail prom (`.github/prompts/dsom-reanimate.prompt.md`) untuk memulakan sesi dengan pantas:
1. Taip `/` dalam chat.
2. Pilih `dsom-reanimate`.
3. Copilot akan membaca semua artifak brain dan menyelaraskan status semasanya.

---
*Generated for the DSOM Sovereign Environment.*

