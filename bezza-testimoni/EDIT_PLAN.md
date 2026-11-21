# Edit Plan — Delivery Perodua Bezza (Jo Hashim) — v5

**Sumber:** video iPhone 80.7s, 9:16 (HDR HLG → ditukar ke SDR)
**Hasil edit:** 51.2s, 1080×1920, 30fps — **status: PREVIEW DRAF v5 (belum render final)**
**Preview:** `renders/PREVIEW_bezza_testimoni_v5.mp4` (540×960, watermark)

## Perubahan v5 (ikut feedback)

1. **"DMM Sales (PJ)" dibuang** dari name card & end card (kini "Perodua" sahaja). Reben fizikal atas kereta masih tertulis DMM Sales — itu dalam footage.
2. **Caption "sales lain" → "SA lain".**
3. **Grafik "DEAL BANK DALAM 3 HARI" dibuang** (beserta SFX & shake).
4. **"Bang Jo" / "abang Jo" → "Jo"** dalam caption (audio masih sebut "Bang Jo").
5. **"Err" sebelum "satu biji kereta" dibuang** (src 3.80–4.01: "deliver *err* satu biji kereta"). Perkataan "Bezza X" kekal — "X" ialah varian kereta; caption kini "Bezza X".
6. **Intro: bunyi "sebab" di awal dibuang** — klip intro kini mula 0.18s lewat (src 52.80), selepas hujung perkataan sebelumnya. Disahkan dengan transkrip semula render.

## Perubahan v4

1. **"Erk erk" di intro dibuang.** Ia datang dari klip "Memang cepat" (src 29.8–30.9, ada dua bunyi pendek) — klip itu dibuang terus.
2. **Plat VSA 2173 di-blur** (pixelate + blur) pada setiap frame. Plat dijejak dengan OpenCV CSRT dan blur dibakar terus ke dalam footage (`build/plate/`).
3. **Hook baru = repeat customer:** *"Saya dah ambil 2 kali kereta dengan Bang Jo"* (1.15×), tajuk penuh dari frame pertama "REPEAT CUSTOMER / **BELI KERETA KALI KE-2**". Bahagian "kereta sampai 1 minggu" dipulangkan ke tempat asal (lepas "deal dengan bank") dengan kad "KERETA SAMPAI DALAM 1 MINGGU".
4. **Caption "Okay guys" dibuang** (audio kekal).
5. **Caption "nak cepat kita proses" → "nak cepat kereta proses".**

## Perubahan v3

1. **Hook dipercepatkan 1.2×** (suara customer, pitch kekal) — hook kini 3.6s (dulu 4.3s).
2. **Caption lebih kecil** (maks 64px, dulu 84px) dan **diturunkan ke paras peha** (y≈1340).
3. **Perkataan "so" dibuang** dari caption ("So apa pesanan", "so korang yang").
4. **Tajuk hook ditulis penuh dari frame pertama:** "KERETA SAMPAI DALAM **1 MINGGU**" (tak tunggu lagi).
5. **Suara Jo untuk "apa pesanan untuk customer kat luar?" dikuatkan** ~+4.7 dB (−21.3 → −16.6 LUFS) dengan limiter, tiada clipping.
6. **"Butang biru" → "beg biru"** di caption dan butang CTA ("TEKAN BEG BIRU").

## Perubahan v2

1. **JOE → JO** di semua tempat: caption, name card, end card, "Bang Jo".
2. **Hook ditukar:** video sekarang buka dengan *"Memang cepat. Dan kereta pun dapat dalam 1 minggu lebih"* + grafik "KERETA SAMPAI DALAM **1 MINGGU**". Ayat *"Saya buat 3 hari sahaja, dah dapat deal dengan bank"* dipulangkan ke tempat asal (selepas "Ni saya ambil Bezza lah").
3. **Grafik "Sales lain vs Bang Jo" dibuang.** Audio customer kekal.
4. **Cop "BUKAN IKLAN" dibuang**, dan ayat yang diucap "Ini bukan iklan" pun dipotong (lihat TikTok di bawah).
5. **Ayat-ayat testimoni dibuang:** chip "TESTIMONI CUSTOMER", "SERIUS! 100% TESTIMONI IKHLAS", kad "LOAN CEPAT / PROSES CEPAT".

## Pematuhan TikTok — apa yang dibuat

| Risiko | Tindakan |
|---|---|
| **Kandungan komersial tak didedahkan** (salesperson post, tapi cakap "bukan iklan" / "saya tak dibayar") — boleh dikira mengelirukan di bawah polisi Branded Content | Ayat **"Ini bukan iklan"** dan **"Serius, ini saya tak dibayar untuk apa-apa"** dipotong dari audio & caption |
| **Dakwaan kewangan / pinjaman** ("lulus bank 3 hari", "loan cepat") boleh dianggap janji mengelirukan | Kad "LOAN CEPAT" dibuang. Kad "3 HARI" kini ada nota: *"Pengalaman customer ini. Tempoh kelulusan bergantung pada bank."* |
| Perbandingan merendahkan pihak lain | Grafik "Sales lain 2+ minggu" dibuang |
| Hak cipta audio | Tiada muzik. SFX daripada Pixabay (Pixabay Content License, boleh guna komersial) |
| Teks keluar safe zone UI TikTok | Semua grafik & caption dalam zon selamat TikTok (check HyperFrames lulus) |

**Bila post di TikTok, awak sendiri perlu:**
- Hidupkan **Content disclosure → "Your brand"** (sebab ni promosi jualan sendiri).
- Pastikan customer **izinkan** muka dia & nombor plat (VSA 2173) disiar. Kalau tak pasti, boleh blur plat (minta saya).
- Caption post: elak janji macam "confirm lulus", "loan pasti approve", "tanpa dokumen".

## Struktur edit (output)

| Masa | Beat | Grafik | SFX |
|---|---|---|---|
| 0:00–0:04.3 | **HOOK** "Memang cepat… kereta dapat dalam 1 minggu lebih" | "KERETA SAMPAI DALAM" (frame 0) → **1 MINGGU** slam + shake | impact |
| 0:04.3 | Cut | Flash + punch | whoosh |
| 0:04.7–0:09.5 | Jo kenalkan diri | Name card **JO HASHIM · Perodua · DMM Sales (PJ)** | whoosh-short |
| 0:09.5–0:12 | Delivery Bezza → Rawang | Kad delivery | pop |
| 0:12–0:17 | Soalan feedback | caption | — |
| 0:17.4–0:24 | Customer kali ke-2 | "REPEAT CUSTOMER / KALI KE-2" | pop |
| 0:24–0:29 | "3 hari sahaja dah dapat deal dengan bank" | "DEAL BANK DALAM **3 HARI**" + nota | click, impact |
| 0:29–0:35 | Sebelum ni dengan sales lain lebih 2 minggu… | caption sahaja | — |
| 0:35–0:37 | "Pesanan untuk customer?" | chip "PESANAN UNTUK ANDA?" | pop |
| 0:38.5–0:40.7 | "Dah ambil 2 kali dengan Bang Jo" | "2X BELI KERETA dengan Bang Jo" | whoosh-short |
| 0:40.7–0:45.4 | "Kalau korang nak dapat loan cepat… ambil dengan Bang Jo" | caption sahaja | — |
| 0:45.4–0:49.6 | CTA | "BERMINAT?" → butang **TEKAN BEG BIRU** + anak panah | whoosh, pop, click |
| 0:49.6–0:52.7 | End card | **TERIMA KASIH! / JO HASHIM** atas shot thumbs-up | whoosh-short |

**Bahagian dibuang (jumlah ~28s):** "kita nak tengok feedback…" (repeat), "Boleh?" + jeda, "Sepertulah", "Ini bukan iklan", "Serius saya tak dibayar…", "dah dua kali, kali kedua, memang cepat" (repeat), "Ok itu je" + jeda 1.7s, shot kamera jatuh di hujung, dan semua jeda lebih kurang 0.5s.

**Audio:** −13.6 LUFS, true peak −1.0 dBTP, tiada clipping (diukur, bukan didengar).

## Masih perlu disahkan ⚠️

1. "Perodua PJ" (transkripsi dengar "Pro2PJ")
2. "ambil **kereta** saya yang belakang tu" (perkataan "kereta" diteka)

## Cara ubah

Semua keputusan dalam `build/build.py`. Lepas ubah:

```bash
python3 build/build.py && npx hyperframes check
```
