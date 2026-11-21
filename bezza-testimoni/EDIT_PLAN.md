# Edit Plan — Delivery Perodua Bezza (Jo Hashim) — v2

**Sumber:** video iPhone 80.7s, 9:16 (HDR HLG → ditukar ke SDR)
**Hasil edit:** 52.7s, 1080×1920, 30fps — **status: PREVIEW DRAF v2 (belum render final)**
**Preview:** `renders/PREVIEW_bezza_testimoni_v2.mp4` (540×960, watermark)

## Perubahan v2 (ikut feedback)

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
| 0:45.4–0:49.6 | CTA | "BERMINAT?" → butang **TEKAN BUTANG BIRU** + anak panah | whoosh, pop, click |
| 0:49.6–0:52.7 | End card | **TERIMA KASIH! / JO HASHIM** atas shot thumbs-up | whoosh-short |

**Bahagian dibuang (jumlah ~28s):** "kita nak tengok feedback…" (repeat), "Boleh?" + jeda, "Sepertulah", "Ini bukan iklan", "Serius saya tak dibayar…", "dah dua kali, kali kedua, memang cepat" (repeat), "Ok itu je" + jeda 1.7s, shot kamera jatuh di hujung, dan semua jeda lebih kurang 0.5s.

**Audio:** −13.6 LUFS, true peak −1.0 dBTP, tiada clipping (diukur, bukan didengar).

## Masih perlu disahkan ⚠️

1. "Perodua PJ" (transkripsi dengar "Pro2PJ")
2. "tekan **butang biru**" (transkripsi dengar "backbiro")
3. "ambil **kereta** saya yang belakang tu" (perkataan "kereta" diteka)

## Cara ubah

Semua keputusan dalam `build/build.py`. Lepas ubah:

```bash
python3 build/build.py && npx hyperframes check
```
