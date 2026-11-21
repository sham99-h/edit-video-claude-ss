#!/usr/bin/env python3
"""Generate the HyperFrames composition for the Bezza delivery testimonial.

Source of truth for the edit: SEGMENTS (the cut list, in source seconds),
CORRECTIONS (transcript fixes) and the CARDS / SFX tables below.
Run:  python3 build/build.py   (from the project folder)
It rewrites index.html and compositions/*.html.
"""
import json, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
W, H = 1080, 1920
SRC = "assets/footage.mp4"
SRC_DUR = 80.80
# footage.mp4 = Drive original, HLG->SDR tonemap, plate VSA 2173 pixelated on every
# frame (OpenCV CSRT track, see build/plate/), audio rebuilt by build/audio_balance.py
# (every clip levelled to the same loudness; re-run it after changing SEGMENTS).

# ---------------------------------------------------------------------------
# 1. CUT LIST  (id, source_in, source_out, punch scale)
#    Everything not listed is cut. Reasons are in EDIT_PLAN.md.
# ---------------------------------------------------------------------------
SEGMENTS = [
    ("hook", 52.80, 55.16, 1.10),  # HOOK (starts after a "sebab"-sounding tail): "Saya dah ambil 2 kali kereta dengan Bang Jo" (repeat customer)
    ("a1",   0.00,  3.80, 1.00),   # Jo intro "...kita nak deliver"
    #  3.80-4.01 CUT: "err"
    ("a2",   4.01,  5.28, 1.10),   # "satu biji kereta"
    ("b",    5.78,  7.98, 1.00),   # "Bezza X customer daripada Rawang" (pause 5.28-5.78 cut)
    #  7.98-13.85 CUT: "Kita nak tengok feedback..." (repeat of the question below)
    ("c",   13.85, 17.64, 1.00),   # question
    ("d",   18.15, 19.32, 1.10),   # "...kali kedua?" (pause cut)
    #  19.32-21.22 CUT: "Boleh?" + awkward pause
    ("e",   21.22, 25.92, 1.00),   # repeat customer context
    ("f1",  26.56, 27.63, 1.12),   # "Ni saya ambil"
    #  27.63-28.72 CUT: "aa, apa"
    ("f2",  28.72, 29.19, 1.00),   # "Bezza lah"
    #  29.19-30.86 CUT: "erk erk" + "memang cepat"
    ("deal", 30.86, 35.80, 1.00),  # "Saya buat 3 hari sahaja, dah dapat deal dengan bank"
    ("h",   35.80, 39.10, 1.12),   # "Dan kereta pun dapat dalam 1 minggu lebih"
    ("i",   39.52, 42.47, 1.00),   # "Agak sangat cepat... sales lain"
    ("j",   43.00, 46.08, 1.12),   # "lebih 2 minggu. Ini tak sampai 2 minggu"
    #  46.08-47.45 CUT: "Sepertulah" filler + pause
    #  47.45-47.90 CUT: customer "memang"
    ("k",   47.90, 48.48, 1.00),   # "apa pesa-" (Jo)
    ("l1",  49.22, 51.40, 1.12),   # "...untuk customer kat luar? Okay guys"
    #  51.40-52.62 CUT (TikTok): "Ini bukan iklan"
    #  52.62-55.14 used as HOOK
    ("n1",  55.64, 60.22, 1.00),   # "Kalau korang nak loan cepat..."
    #  60.22-63.30 CUT (TikTok): "Serius, saya tak dibayar"
    #  63.30-70.80 CUT: repeat + "ok itu je" + 1.7s pause
    ("o",   70.80, 78.30, 1.00),   # CTA + "Assalamualaikum" + thumbs-up pose under end card
    #  78.30-80.80 CUT: camera drops to the floor
]

# ---------------------------------------------------------------------------
# 2. TRANSCRIPT CORRECTIONS (keyed by whisper word start, source seconds)
#    value: list of replacement words (time split evenly) or [] to drop.
# ---------------------------------------------------------------------------
CORRECTIONS = {
    1.70: ["Perodua", "PJ."],      # whisper: "Pro2PJ"  (VERIFY)
    0.70: ["Jo"],                  # spelling: Jo
    23.80: ["Jo"],
    23.54: [],                     # "abang" (caption: just "Jo")
    5.22: ["Bezza", "X"],          # "BezaX" = Bezza X variant
    23.18: ["deal"],               # "di"
    24.30: [],                     # "kita"
    24.60: ["ambil"],              # "atibah"
    24.98: ["kereta"],             # "pasal" (VERIFY: model kereta lama?)
    26.96: ["ambil"],              # "atibah"
    27.64: [],                     # "dengan"
    28.18: [],                     # "Atok"
    28.80: ["Bezza"],              # "Beza"
    41.82: ["SA"],                 # "SEL" -> "SA lain"
    51.86: ["bukan"],              # "saya" -> "Ini bukan iklan" (VERIFY)
    53.64: ["kali"],               # "cari"
    54.58: ["Jo."],       # "Banjo"
    59.78: ["Jo."],       # "banjur"
    64.34: ["repeat"],             # (cut anyway)
    63.20: [],                     # "sebab" (cut region)
    74.14: [],                     # "beg biru" - shown on the CTA button instead
    47.20: [],                     # "So" (filler)
    47.94: ["apa", "pesanan"],     # Jo (the "apa" word timing sits in the cut "memang")
    73.56: [],                     # "tekan" - shown on the CTA button instead
    74.58: [],                     # "dekat"
    74.86: [],                     # "bawah"
    50.82: [],                     # "Okay" caption removed
    51.02: [],                     # "guys" (would stand alone)
    58.70: ["kereta"],             # caption: "nak cepat kereta proses"
    70.46: [],                     # "so" (filler)
}
KEEP_CASE = {"SA", "X", "PJ."}
HIGHLIGHT = {"3", "hari", "bank", "cepat", "1", "minggu", "2", "kedua", "loan",
             "jo", "bezza", "rawang", "dibayar", "beg", "biru",
             "bukan", "iklan", "kali", "hashim", "serius"}

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def fr(t):
    """snap to frame"""
    return round(round(t * FPS) / FPS, 4)

# playback speed per segment (pitch-preserved); hook spoken faster
RATE = {"hook": 1.15}

timeline = []  # (id, src_in, src_out, out_start, scale)
_t = 0.0
for sid, a, b, sc in SEGMENTS:
    timeline.append((sid, a, b, fr(_t), sc))
    _t = fr(_t + (b - a) / RATE.get(sid, 1.0))
TOTAL_VIDEO = _t

def out(src_t):
    """map a source time to output time (None if cut)"""
    for sid, a, b, o, sc in timeline:
        if a - 1e-6 <= src_t <= b + 1e-6:
            return fr(o + (src_t - a) / RATE.get(sid, 1.0))
    return None

def seg(sid):
    for s in timeline:
        if s[0] == sid:
            return s
    raise KeyError(sid)

def seg_start(sid): return seg(sid)[3]
def seg_end(sid):
    s = seg(sid); return fr(s[3] + (s[2] - s[1]) / RATE.get(sid, 1.0))

END_HOLD = 0.0
TOTAL = fr(TOTAL_VIDEO + END_HOLD)

# ---------------------------------------------------------------------------
# 3. CAPTION WORDS
# ---------------------------------------------------------------------------
raw = json.load(open(ROOT / "build/transcript.raw.json"))
words = []
for s in raw:
    if words: words[-1]["brk"] = True
    for w in s["words"]:
        txt, ws, we = w["w"].strip(), w["s"], w["e"]
        if txt.startswith("-") and words:          # "apa -apa" -> "apa-apa"
            words[-1]["text"] += txt; words[-1]["e"] = we; continue
        key = next((k for k in CORRECTIONS if abs(k - ws) < 0.011), None)
        if key is not None:
            rep = CORRECTIONS[key]
            n = len(rep)
            for i, r in enumerate(rep):
                words.append({"text": r, "s": ws + (we - ws) * i / n, "e": ws + (we - ws) * (i + 1) / n})
            continue
        words.append({"text": txt, "s": ws, "e": we})

cap = []
for w in words:
    # a word belongs to the segment overlapping most of it
    best = max(timeline, key=lambda t: min(w["e"], t[2]) - max(w["s"], t[1]))
    sid, a, b, o, sc = best
    ov = min(w["e"], b) - max(w["s"], a)
    if ov < 0.04 and ov < 0.5 * (w["e"] - w["s"]):
        continue
    s_ = max(w["s"], a); e_ = min(w["e"], b)
    cap.append({"text": w["text"], "seg": sid, "s": fr(o + (s_ - a) / RATE.get(sid, 1.0)), "e": fr(o + (e_ - a) / RATE.get(sid, 1.0)), "brk": w.get("brk", False)})

cap.sort(key=lambda w: w["s"])
# group: <=3 words, break on punctuation / segment change / pause >= .15
groups, cur = [], []
for i, w in enumerate(cap):
    glue = cur and (cur[-1]["text"] in ("Bang", "1", "2", "3") ) and w["seg"] == cur[-1]["seg"]
    if cur and not glue and (len(cur) >= 5 or w["seg"] != cur[-1]["seg"] or w["s"] - cur[-1]["e"] >= 0.15
                or cur[-1]["brk"] or re.search(r"[.,?!]$", cur[-1]["text"])):
        groups.append(cur); cur = []
    cur.append(w)
if cur: groups.append(cur)
# fold a lone trailing word ("tu.", "sahaja", "cepat") into the group before it
merged = []
for g in groups:
    if merged and len(g) == 1 and len(merged[-1]) <= 5 and g[0]["seg"] == merged[-1][-1]["seg"] \
            and g[0]["s"] - merged[-1][-1]["e"] < 0.35 and not re.search(r"[.?!]$", merged[-1][-1]["text"]):
        merged[-1] = merged[-1] + g
    else:
        merged.append(g)
groups = merged

# ---------------------------------------------------------------------------
# 4. OVERLAY CARDS (each its own scene file)  times in OUTPUT seconds
# ---------------------------------------------------------------------------
T = {
    "three":   out(32.36),   # "3 hari"
    "bank":    out(35.32),   # "bank"
    "a1":      seg_start("a1"),
    "b":       seg_start("b"),
    "kali2":   out(22.08),
    "minggu1": out(38.48),
    "saleslain": out(41.82),
    "lebih2":  out(43.20),
    "taksampai": out(44.24),
    "bukan":   out(51.86),
    "duakali": out(53.18),
    "loan":    out(56.56),
    "proses":  out(58.38),
    "bangjoe": out(59.78),
    "serius":  out(60.22),
    "berminat": out(72.24),
    "tekan":   out(73.56),
    "biru":    out(74.14),
    "salam":   out(75.26),
}

CARD_CSS = """
#root{position:absolute;inset:0;font-family:'Inter',sans-serif;}
.scrim{position:absolute;left:0;right:0;top:0;height:920px;background:linear-gradient(180deg,rgba(18,12,14,.62) 0%,rgba(18,12,14,.42) 48%,rgba(18,12,14,0) 100%);}
.stack{position:absolute;left:0;right:0;top:300px;text-align:center;}
.lbl{display:inline-flex;align-items:center;gap:14px;padding:12px 26px;border-radius:999px;background:rgba(255,255,255,.14);border:1.5px solid rgba(255,255,255,.28);font-weight:700;font-size:32px;letter-spacing:.12em;color:#fff;text-transform:uppercase;}
.lbl i{display:inline-block;width:14px;height:14px;border-radius:50%;background:linear-gradient(135deg,#FF5A5F,#FF9A62);}
.ttl{font-weight:900;letter-spacing:-.045em;line-height:.96;color:#FFFFFF;text-shadow:0 6px 24px rgba(0,0,0,.35);}
.hot{background:linear-gradient(100deg,#FF5A5F 10%,#FF9A62 90%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 6px 18px rgba(0,0,0,.30));}
.acc{display:inline-block;font-weight:700;font-style:italic;font-size:42px;color:#FFD9CF;transform:rotate(-5deg);text-shadow:0 2px 12px rgba(0,0,0,.4);}
.sub{font-weight:600;font-size:36px;color:rgba(255,255,255,.9);letter-spacing:.02em;text-shadow:0 2px 10px rgba(0,0,0,.35);}
.bar{height:8px;width:180px;margin:18px auto 0;border-radius:8px;background:linear-gradient(90deg,#FF5A5F,#FF9A62);transform-origin:left center;}
"""

def scene(cid, dur, body, script, css=""):
    return f"""<template>
  <style>{CARD_CSS}{css}</style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{script}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""

cards = []  # (cid, start, dur, html)

def card(cid, start, end, body, script, css=""):
    start, end = fr(start), fr(end)
    cards.append((cid, start, fr(end - start), scene(cid, fr(end - start), body, script, css)))

def rel(t, base):  # relative time inside a card
    return round(t - base, 3)

def title_card(cid, start, end, label, title, size, accent="", sub="", hit=None, static=False, plain_label=False):
    """reference style: small white label, big pastel-yellow heavy title, optional tilted accent"""
    p = cid[:2]
    body = f"""
    <div id="{p}-scrim" class="scrim"></div>
    <div id="{p}-wrap" class="stack">
      {(f'<div id="{p}-lbl" class="sub" style="font-size:40px;font-weight:700;">{label}</div>' if plain_label else f'<div id="{p}-lbl" class="lbl"><i></i>{label}</div>') if label else ''}
      <div id="{p}-ttl" class="ttl" style="font-size:{size}px;margin-top:18px;">{title}</div>
      <div id="{p}-bar" class="bar"></div>
      {f'<div style="text-align:right;padding-right:170px;margin-top:2px;"><span id="{p}-acc" class="acc">{accent}</span></div>' if accent else ''}
      {f'<div id="{p}-sub" class="sub" style="margin-top:14px;">{sub}</div>' if sub else ''}
    </div>"""
    js = [f'tl.fromTo("#{p}-scrim", {{opacity:{1 if static else 0}}}, {{opacity:1, duration:{0.01 if static else 0.3}}}, 0);']
    if static:
        js.append(f'tl.fromTo("#{p}-wrap", {{opacity:1}}, {{opacity:1, duration:0.01}}, 0);')
    else:
        if label: js.append(f'tl.fromTo("#{p}-lbl", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.3, ease:"power4.out"}}, 0);')
        js.append(f'tl.fromTo("#{p}-ttl", {{opacity:0, filter:"blur(10px)", scale:1.06}}, {{opacity:1, filter:"blur(0px)", scale:1, duration:0.22, ease:"power4.out"}}, {rel(hit, start) if hit else 0.08});')
    js.append(f'tl.fromTo("#{p}-bar", {{scaleX:{1 if static else 0}}}, {{scaleX:1, duration:{0.01 if static else 0.45}, ease:"expo.out"}}, {0 if static else 0.2});')
    if accent: js.append(f'tl.fromTo("#{p}-acc", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.3, ease:"back.out(2)"}}, {0.35 if not static else 0.2});')
    if sub: js.append(f'tl.fromTo("#{p}-sub", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.3, ease:"power4.out"}}, 0.3);')
    js.append(f'tl.to(["#{p}-wrap","#{p}-scrim"], {{opacity:0, filter:"blur(6px)", duration:0.2, ease:"power3.in"}}, {rel(end - 0.22, start)});')
    card(cid, start, end, body, "\n".join("    " + l for l in js))

# --- HOOK (full title from frame 0) -------------------------------------------
hs, he = 0.0, seg_end("hook")
title_card("hook", hs, he, "Repeat customer", 'BELI KERETA<br><span class="hot">KALI KE-2</span>', 100, accent="dengan Jo", static=True)

# --- NAME ------------------------------------------------------------------------
ns, ne = T["a1"] + 0.45, T["b"]
title_card("name", ns, ne, "Perodua", "JO HASHIM", 100)

# --- DELIVERY ------------------------------------------------------------------
ds, de = T["b"], seg_end("b") + 0.6
title_card("delivery", ds, de, "Delivery hari ini", 'PERODUA <span class="hot">BEZZA</span>', 84, accent="ke Rawang")

# --- REPEAT CUSTOMER ---------------------------------------------------------------
ks, ke = T["kali2"] - 0.1, seg_end("f2")
title_card("repeat", ks, ke, "Repeat customer", 'KALI <span class="hot">KE-2</span>', 110)

# --- 1 MINGGU (body) ----------------------------------------------------------------
ms, me = T["minggu1"] - 0.08, T["minggu1"] + 2.0
title_card("minggu", ms, me, "Kereta sampai dalam", '<span class="hot">1</span> MINGGU', 116)

# --- CTA ----------------------------------------------------------------------------
os_, oe = seg_start("o") + 0.2, T["salam"] - 0.1
card("cta", os_, oe, """
    <div id="ca-scrim" class="scrim"></div>
    <div id="ca-q" class="ttl" style="position:absolute;left:0;right:0;top:320px;text-align:center;font-size:100px;">BERMINAT<span class="hot">?</span></div>
    <div id="ca-btn" style="position:absolute;left:0;right:0;margin:auto;width:720px;top:1320px;padding:28px 0;border-radius:999px;background:#1877F2;color:#fff;text-align:center;font-weight:800;font-size:52px;letter-spacing:-.01em;box-shadow:0 12px 0 #0b4fa8,0 26px 50px rgba(0,0,0,.30);">tekan beg biru</div>
    <svg id="ca-arrow" style="position:absolute;left:0;right:0;margin:auto;top:1475px;" width="110" height="110" viewBox="0 0 24 24"><path d="M12 22L2 11h6V2h8v9h6z" fill="#1877F2" stroke="#fff" stroke-width="1"/></svg>
""", f"""
    tl.fromTo("#ca-scrim", {{opacity:0}}, {{opacity:1, duration:0.3}}, {rel(T['berminat'] - 0.4, os_)});
    tl.fromTo("#ca-q", {{opacity:0, filter:"blur(10px)", scale:1.06}}, {{opacity:1, filter:"blur(0px)", scale:1, duration:0.22, ease:"power4.out"}}, {rel(T['berminat'] - 0.35, os_)});
    tl.fromTo("#ca-btn", {{opacity:0, y:60, scale:0.8}}, {{opacity:1, y:0, scale:1, duration:0.4, ease:"back.out(1.6)"}}, {rel(T['tekan'], os_)});
    tl.to("#ca-btn", {{scale:0.93, y:10, boxShadow:"0 3px 0 #0b4fa8,0 10px 30px rgba(0,0,0,.30)", duration:0.08, ease:"power2.in"}}, {rel(T['biru'] + 0.15, os_)});
    tl.to("#ca-btn", {{scale:1, y:0, boxShadow:"0 12px 0 #0b4fa8,0 26px 50px rgba(0,0,0,.30)", duration:0.2, ease:"power2.out"}}, {rel(T['biru'] + 0.23, os_)});
    tl.fromTo("#ca-arrow", {{opacity:0, y:-30}}, {{opacity:1, y:0, duration:0.3, ease:"power4.out"}}, {rel(T['biru'], os_)});
    tl.to("#ca-arrow", {{y:30, duration:0.3, ease:"power1.inOut", yoyo:true, repeat:3}}, {rel(T['biru'] + 0.3, os_)});
    tl.to(["#ca-q","#ca-btn","#ca-arrow","#ca-scrim"], {{opacity:0, duration:0.15}}, {rel(oe - 0.16, os_)});
""")

# --- END CARD -------------------------------------------------------------------------
es, ee = T["salam"] - 0.1, TOTAL
title_card("endcard", es, ee, "Terima kasih kerana berurusan dengan", "JO HASHIM", 104, sub="Perodua", plain_label=True)

# ---------------------------------------------------------------------------
# 5. SOUND FX  (file, picture time, peak offset, volume)
#    placed so the peak lands one frame after the picture event
# ---------------------------------------------------------------------------
PEAK = {"whoosh": 0.162, "whoosh-short": 0.162, "pop": 0.12, "impact-bass-1": 0.073,
        "click": 0.073, "sparkle": 0.027}
DUR = {"whoosh": 0.57, "whoosh-short": 0.57, "pop": 0.72, "impact-bass-1": 2.1,
       "click": 0.36, "sparkle": 1.8}
CUT_HOOK = seg_start("a1")
CUT_CTA = seg_start("o")
SFX = [
    ("pop",           T["duakali"] + 0.05, 0.9), # hook "KALI KE-2" pulse
    ("whoosh",        CUT_HOOK,         0.7),    # hook -> intro flash
    ("whoosh-short",  ns + 0.15,        0.5),    # name card wipe
    ("pop",           ds + 0.2,         0.8),    # delivery card
    ("pop",           ks + 0.3,         0.8),    # KALI KE-2
    ("impact-bass-1", T["minggu1"] + 0.1, 0.2),  # 1 MINGGU slam
    ("whoosh",        CUT_CTA,          0.6),    # jump to CTA flash
    ("pop",           T["berminat"] - 0.1, 0.8),
    ("click",         T["biru"] + 0.18, 1.2),    # button press
    ("whoosh-short",  es + 0.15,        0.45),   # end card
]

# ---------------------------------------------------------------------------
# 6. WRITE FILES
# ---------------------------------------------------------------------------
comp = ROOT / "compositions"
comp.mkdir(exist_ok=True)
for f in comp.glob("*.html"):
    f.unlink()
for cid, st, du, src in cards:
    (comp / f"{cid}.html").write_text(src)

# captions scene
cap_body, cap_js = [], []
for gi, g in enumerate(groups):
    gs = max(0.0, fr(g[0]["s"] - 0.04))
    nxt = groups[gi + 1][0]["s"] - 0.04 if gi + 1 < len(groups) else TOTAL
    ge = fr(min(max(g[-1]["e"] + 0.25, gs + 0.5), nxt, TOTAL - 0.02))
    if gs < T["tekan"] < ge:          # the CTA button takes the caption spot: clear out first
        ge = fr(T["tekan"] - 0.05)
    text_len = sum(len(w["text"]) for w in g) + len(g) - 1
    fs = int(min(56, 820 / max(1, text_len * 0.52)))
    runs = []  # consecutive keywords share one pill
    for w in g:
        hl = re.sub(r"[^\w]", "", w["text"].lower()) in HIGHLIGHT
        txt = w["text"] if w["text"] in KEEP_CASE else w["text"].lower()
        if runs and runs[-1][0] == hl and hl:
            runs[-1][1].append(txt)
        else:
            runs.append([hl, [txt]])
    spans = [f'<span id="cw{gi}_{ri}" class="{"cw hl" if hl else "cw"}">{html.escape(" ".join(ws))}</span>'
             for ri, (hl, ws) in enumerate(runs)]
    cap_body.append(f'    <div id="cg{gi}" class="cg" style="font-size:{fs}px;">{" ".join(spans)}</div>')
    cap_js.append(f'tl.set("#cg{gi}",{{visibility:"visible"}},{gs:.3f});')
    cap_js.append(f'tl.fromTo("#cg{gi}",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.08,ease:"power2.out"}},{gs:.3f});')
    cap_js.append(f'tl.to("#cg{gi}",{{opacity:0,duration:0.08,ease:"power2.in"}},{ge - 0.08:.3f});')
    cap_js.append(f'tl.set("#cg{gi}",{{opacity:0,visibility:"hidden"}},{ge:.3f});')

cap_css = """
#root{position:absolute;inset:0;font-family:'Inter',sans-serif;}
.cg{position:absolute;left:110px;right:110px;top:1340px;text-align:center;font-weight:650;line-height:1.3;letter-spacing:-.01em;color:#fff;opacity:0;visibility:hidden;overflow:visible;text-shadow:0 2px 3px rgba(0,0,0,.55),0 4px 18px rgba(0,0,0,.40);}
.cw{display:inline;}
.cw.hl{display:inline-block;padding:0 12px 2px;margin:0 2px;border-radius:12px;background:#FFFFFF;color:#B0182F;font-weight:800;text-shadow:none;box-shadow:0 4px 16px rgba(0,0,0,.28);}
"""
(comp / "captions.html").write_text(f"""<template>
  <style>{cap_css}</style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
{chr(10).join(cap_body)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + l for l in cap_js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
""")

# root index.html
vids = []
for i, (sid, a, b, o, sc) in enumerate(timeline):
    d = fr((b - a) / RATE.get(sid, 1.0))
    vids.append(f'      <video id="v-{sid}" class="clip" src="{SRC}" data-start="{o}" data-duration="{d}" '
                f'data-media-start="{a}" data-playback-rate="{RATE.get(sid, 1.0)}" data-track-index="0" data-has-audio="true" '
                f'data-fade-in="0.02" data-fade-out="0.03" playsinline></video>')

hosts = []
z = 10
for cid, st, du, _ in cards:
    z += 1
    hosts.append(f'    <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                 f'data-start="{st}" data-duration="{du}" data-track-index="1" data-track-kind="graphics" '
                 f'data-width="{W}" data-height="{H}" style="z-index:{z};"></div>')

sfx_tags = []
for i, (name, t, vol) in enumerate(SFX):
    st = fr(max(0, t + 1 / FPS - PEAK[name]))
    du = fr(min(DUR[name], TOTAL - st))
    sfx_tags.append(f'    <audio id="sfx{i:02d}" class="clip" src="assets/sfx/{name}.mp3" data-start="{st}" '
                    f'data-duration="{du}" data-track-index="3" data-volume="{vol}"></audio>')

# camera moves: punch scale per segment, flash on the 2 big cuts, shake on slams
cam_js = []
for sid, a, b, o, sc in timeline:
    cam_js.append(f'tl.set("#cam",{{scale:{sc},x:0,y:0}},{o});')
cam_js.append(f'tl.fromTo("#cam",{{scale:1.3}},{{scale:1.0,duration:0.45,ease:"expo.out"}},{CUT_HOOK});')
cam_js.append(f'tl.fromTo("#cam",{{scale:1.25}},{{scale:1.0,duration:0.45,ease:"expo.out"}},{CUT_CTA});')
cam_js.append('tl.set("#flash",{opacity:0},0);')
for c in (CUT_HOOK, CUT_CTA):
    cam_js.append(f'tl.fromTo("#flash",{{opacity:0}},{{opacity:0.9,duration:0.06,ease:"power2.in"}},{fr(c - 0.06)});')
    cam_js.append(f'tl.to("#flash",{{opacity:0,duration:0.22,ease:"power2.out"}},{c});')
for t, amp in ((T["minggu1"] + 0.1, 10),):
    cam_js.append(f'tl.to("#cam",{{keyframes:[{{x:{amp},y:-{amp//2},duration:0.04}},{{x:-{amp},y:{amp//2},duration:0.05}},'
                  f'{{x:{amp//2},y:0,duration:0.05}},{{x:0,y:0,duration:0.06}}]}},{t:.3f});')
# slow push inside the long CTA segment keeps the frame alive
cam_js.append(f'tl.to("#cam",{{scale:1.08,duration:{fr(T["salam"] - CUT_CTA - 0.5)},ease:"none"}},{fr(CUT_CTA + 0.5)});')

index = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      #cam {{ position: absolute; inset: 0; transform-origin: 50% 49%; }}
      #cam video {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; object-fit: cover; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 50; pointer-events: none; }}
    </style>
  </head>
  <body>
    <!-- GENERATED by build/build.py — edit the cut list there, then re-run. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
    <div id="cam">
{chr(10).join(vids)}
    </div>
{chr(10).join(hosts)}
    <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:40;"></div>
    <div id="flash"></div>
{chr(10).join(sfx_tags)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + l for l in cam_js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(index)

# edit decision list for the plan
edl = {"total": TOTAL, "segments": [dict(id=s, src_in=a, src_out=b, out_start=o, scale=sc) for s, a, b, o, sc in timeline],
       "cards": [dict(id=c, start=s, dur=d) for c, s, d, _ in cards],
       "sfx": [dict(name=n, at=round(t, 2), vol=v) for n, t, v in SFX],
       "captions": [" ".join(w["text"] for w in g) for g in groups]}
(ROOT / "build/edl.json").write_text(json.dumps(edl, indent=1, ensure_ascii=False))
print(f"total {TOTAL}s, {len(timeline)} segments, {len(cards)} cards, {len(groups)} caption groups, {len(SFX)} sfx")
