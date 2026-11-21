# Edit Plan — Delivery Perodua Bezza (Jo Hashim) — v9

**Sumber:** video iPhone 80.7s, 9:16 (HDR HLG → ditukar ke SDR)
**Hasil edit:** 49.6s, 1080×1920, 30fps — **status: PREVIEW DRAF v9 (belum render final)**
**Preview:** `renders/PREVIEW_bezza_testimoni_v9.mp4` (540×960, watermark)

## Perubahan v11 (storyboard sahaja — belum dirender)

Video rujukan diambil sebagai **inspirasi struktur sahaja** (label kecil + tajuk besar tebal, caption huruf kecil). Palet sendiri, serasi dengan kereta merah maroon:
- Tajuk **putih Inter Black**, satu kata kunci dalam **gradien coral** (#FF5A5F → #FF9A62) + garis bawah coral beranimasi.
- Label dalam **pil kaca** (putih lutsinar) dengan titik coral.
- Aksen kecil italic merah jambu lembut (#FFD9CF).
- Caption putih huruf kecil; kata kunci dalam **pil putih, teks merah maroon** (#B0182F) — jelas walaupun atas reben merah. Kata kunci bersebelahan berkongsi satu pil.
- Butang CTA kekal biru (sebab "beg biru").

## Perubahan v10 (storyboard sahaja — belum dirender: `STORYBOARD.jpg`)

**Gaya font ikut video rujukan TikTok** (`build/font_reference.png`):
- Tajuk: label kecil putih huruf besar + tajuk besar **kuning pastel (#F7E36B), Inter Black, jarak huruf rapat**, bayang lembut, tiada outline. Aksen kecil kuning condong ("dengan Jo", "ke Rawang").
- Scrim gelap lembut di bahagian atas supaya tajuk kuning terbaca atas bumbung putih.
- Caption: **huruf kecil, Inter semi-bold putih**, bayang lembut tanpa outline, kata kunci **kuning tebal**, 4–5 perkataan sebaris (paras peha).
- Kotak hitam/merah lama dibuang. Butang CTA biru dikekalkan (font Inter, "tekan beg biru").

## Perubahan v9 — suara pecah dibaiki

**Punca:** (1) suara Jo di "apa pesanan untuk customer kat luar" sangat perlahan dalam rakaman (−36 dB), jadi dikuatkan +26.5 dB — dan sempadan gain jatuh 0.02s *selepas* customer mula sebut "okay", jadi suara customer pun dikuatkan +26 dB lalu dihimpit limiter (pecah). (2) Di semua klip, puncak selepas gain naik sampai +9 dB atas had dan dihimpit kuat oleh leveller/limiter.

**Baiki (`build/audio_balance.py` ditulis semula):**
- denoise ringan (afftdn 8 dB) + high-pass 70 Hz pada audio asal
- gain setiap klip dalam bentuk sampul lancar (ramp), sempadan Jo→customer dialih ke 50.79 dengan ramp 50ms
- leveller automatik (dynaudnorm) & loudnorm dinamik dibuang → compressor lembut + compressor puncak pantas + normalisasi statik
- limiter kini hanya sentuh puncak pendek: maks 3.5 dB pada <0.1% sampel (dulu ~25 dB di bahagian pesanan)
- gain maksimum turun dari +26.5 ke +17.4 dB

Hasil diukur: setiap klip dalam 0.8 dB (Jo ≈ −16.7, customer ≈ −13.8 LUFS, customer +3 dB), mix −14.9 LUFS, true peak −1.2 dBTP, tiada clipping.

## Perubahan v8 (ikut feedback)

1. **Suara customer (lelaki bertopi) +3 dB** berbanding Jo (diukur: customer ≈ −12.3 LUFS, Jo ≈ −15.3 LUFS per klip).
2. **"Aa, apa" di 0:19–0:20 dipotong** (src 27.63–28.72) → "Ni saya ambil… Bezza lah".
3. **"Memang" sebelum soalan Jo dipotong** (src 47.45–47.90) → "…dapat kereta. Apa pesanan untuk customer kat luar?"
4. **Butang "TEKAN BEG BIRU" diturunkan ke tempat caption** (y≈1320) + anak panah di bawahnya; caption "tekan beg biru dekat bawah" dibuang.

## Perubahan v7 (preview: `renders/PREVIEW_bezza_testimoni_v9.mp4`)

- **Kad "PESANAN UNTUK ANDA?" dibuang** (beserta bunyi pop). Bahagian itu kini caption sahaja.

## Perubahan v6 (ikut feedback)

**Suara semua klip diseimbangkan.** Audio dibina semula dari fail asal (`build/audio_balance.py`):
setiap klip (dipisah ikut siapa bercakap) diberi gain sendiri, diratakan dengan leveller lembut,
kemudian diukur semula dan dibetulkan 5 kali.

| | Klip paling kuat | Klip paling perlahan | Beza |
|---|---|---|---|
| v5 | −11.5 LUFS (customer) | −17.4 LUFS (Jo) | **5.9 dB** |
| v6 | −13.5 LUFS | −15.8 LUFS | **2.3 dB** (termasuk SFX) |

Mix keseluruhan −14.6 LUFS, true peak −1.0 dBTP, tiada clipping. Bunyi latar tidak naik berbanding v5 (diukur).

## Perubahan v5

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
