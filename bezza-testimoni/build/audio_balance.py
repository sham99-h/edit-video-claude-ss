#!/usr/bin/env python3
"""Rebuild footage audio so every used clip sits at the same loudness.
usage: python3 build/audio_balance.py <original_drive_video> assets/footage.mp4
- per-region gain (edit segments from build/edl.json, split where the speaker changes)
- gentle dynamic leveller (dynaudnorm) to even out words inside a clip
- loudnorm -15 LUFS + -1.5 dBFS limiter; then measure every region again and correct
  the gains (iterated) so all regions land within ~1 dB of each other.
"""
import json, re, subprocess, sys, os
src, footage = sys.argv[1], sys.argv[2]
ITER = 5
SPLITS = {50.82}   # speaker changes inside an edit segment (Jo -> customer in "l1")
# customer (man in the cap) sits this many dB above Jo
CUSTOMER_DB = 3.0
CUSTOMER = {"hook", "e", "f1", "f2", "deal", "h", "i", "j", "n1", "l1@50.82"}
def offset(name):
    seg, at = name.split("@")
    return CUSTOMER_DB if (seg in CUSTOMER or f"{seg}@{at}" in CUSTOMER) else 0.0
edl = json.load(open(os.path.join(os.path.dirname(__file__), "edl.json")))
regions = []
for s in edl["segments"]:
    a, b = s["src_in"], s["src_out"]
    cuts = [a] + sorted(t for t in SPLITS if a < t < b) + [b]
    for x, y in zip(cuts, cuts[1:]):
        regions.append((f"{s['id']}@{x:.2f}", x, y))

def lufs(f, t0, d):
    o = subprocess.run(["ffmpeg","-hide_banner","-ss",str(t0),"-t",str(d),"-i",f,"-vn","-af","ebur128","-f","null","-"],
                       capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
def meas(f):
    return [lufs(f, a + 0.03, max(0.4, b - a - 0.06)) for _, a, b in regions]

def render(gains, out):
    vols = [f"volume=enable='between(t,{a-0.04:.2f},{b+0.04:.2f})':volume={g:.2f}dB"
            for (_, a, b), g in zip(regions, gains)]
    chain = ",".join(vols + ["dynaudnorm=f=300:g=15:p=0.9:m=3:s=12",
                             "loudnorm=I=-15:TP=-1.5:LRA=7",
                             "alimiter=limit=0.84:attack=5:release=60:level=false", "aresample=48000"])
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vn","-af",chain,"-c:a","pcm_s16le",out], check=True)

L0 = meas(src)
gains = [max(-12, min(32, -16.0 + offset(n) - L)) for (n, _, _), L in zip(regions, L0)]
wav = footage + ".bal.wav"
for it in range(ITER):
    render(gains, wav)
    L = meas(wav)
    base = [v - offset(n) for (n, _, _), v in zip(regions, L)]
    med = sorted(base)[len(base) // 2]
    print(f"iter {it}: spread {max(base)-min(base):.1f} dB (after offset)  " + " ".join(f"{n.split('@')[0]}:{v:.1f}" for (n, _, _), v in zip(regions, L)))
    if it < ITER - 1:
        gains = [max(-12, min(32, g + (med + offset(n) - v))) for (n, _, _), g, v in zip(regions, gains, L)]
tmp = footage + ".tmp.mp4"
subprocess.run(["ffmpeg","-v","error","-y","-i",footage,"-i",wav,"-map","0:v","-map","1:a","-c:v","copy",
                "-c:a","aac","-b:a","256k","-movflags","+faststart",tmp], check=True)
os.replace(tmp, footage); os.remove(wav)
print("gains:", " ".join(f"{n.split('@')[0]}:{g:+.1f}" for (n, _, _), g in zip(regions, gains)))
