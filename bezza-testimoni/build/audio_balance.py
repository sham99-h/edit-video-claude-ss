#!/usr/bin/env python3
"""Rebuild footage audio: every clip at the same loudness, no distortion.
usage: python3 build/audio_balance.py <original_drive_video> assets/footage.mp4

1. mild spectral denoise + voice EQ (less boom at 220 Hz, presence at 3.4 kHz, air) on the original
2. per-region gain (edit segments from build/edl.json, split where the speaker changes),
   applied as a smooth sample-accurate gain envelope (ramps, no hard switches)
3. gentle compressor, static normalisation to -15 LUFS, true-peak limiter that only
   touches the odd peak (reports how hard it works)
4. measure every region again and correct the gains (iterated)
"""
import json, re, subprocess, sys, os, tempfile
import numpy as np, soundfile as sf

src, footage = sys.argv[1], sys.argv[2]
SR = 48000
ITER = 4
TARGET = -20.0                 # per-region target before final normalisation
CUSTOMER_DB = 3.0              # customer (man in the cap) sits this much above Jo
SPLITS = {50.79: 0.05}         # speaker change inside "l1" (Jo -> customer "okay"), ramp length
CUSTOMER = {"hook", "e", "f1", "f2", "deal", "h", "i", "j", "n1", "l1@50.79"}
MAX_GAIN = 24.0

edl = json.load(open(os.path.join(os.path.dirname(__file__), "edl.json")))
regions = []
for s in edl["segments"]:
    a, b = s["src_in"], s["src_out"]
    cuts = [a] + sorted(t for t in SPLITS if a < t < b) + [b]
    for x, y in zip(cuts, cuts[1:]):
        regions.append((f"{s['id']}@{x:.2f}", x, y))
def offset(name):
    seg, at = name.split("@")
    return CUSTOMER_DB if (seg in CUSTOMER or f"{seg}@{at}" in CUSTOMER) else 0.0

tmp = tempfile.mkdtemp()
def ff(*args): subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)
def lufs_file(f, t0=None, d=None):
    cmd = ["ffmpeg", "-hide_banner"] + (["-ss", str(t0), "-t", str(d)] if t0 is not None else []) + \
          ["-i", f, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]
    o = subprocess.run(cmd, capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

# 1. decode + mild denoise (mono speech)
den = os.path.join(tmp, "den.wav")
ff("-i", src, "-vn", "-ac", "1", "-ar", str(SR), "-af", "highpass=f=80,afftdn=nr=8:nf=-50:tn=1,"
   "equalizer=f=220:t=q:w=1.1:g=-2,equalizer=f=3400:t=q:w=1.0:g=2.5,treble=g=1.5:f=9000", "-c:a", "pcm_f32le", den)
x, _ = sf.read(den, dtype="float32")
t = np.arange(len(x)) / SR

def envelope(gains_db):
    """piecewise gain: hold each region's gain; ramp at in-segment splits; interpolate across cut gaps"""
    pts = []
    for (n, a, b), g in zip(regions, gains_db):
        # at a speaker split the ramp ends exactly on the split (next speaker gets full own gain)
        pts.append((a, g)); pts.append((b - SPLITS.get(round(b, 2), 0.0), g))
    pts.sort()
    xs, ys = zip(*pts)
    return 10 ** (np.interp(t, xs, ys) / 20)

def chain(gains_db, out_wav, final=False):
    y = (x * envelope(gains_db)).astype(np.float32)
    pre = os.path.join(tmp, "pre.wav"); sf.write(pre, y, SR, subtype="FLOAT")
    comp = os.path.join(tmp, "comp.wav")
    ff("-i", pre, "-af", "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=160:knee=6,acompressor=threshold=-12dB:ratio=6:attack=1:release=60:knee=3", "-c:a", "pcm_f32le", comp)
    if not final:
        return comp
    I = lufs_file(comp)
    norm = os.path.join(tmp, "norm.wav")
    ff("-i", comp, "-af", f"volume={-15.0 - I:.2f}dB", "-c:a", "pcm_f32le", norm)
    z, _ = sf.read(norm, dtype="float32")
    over = np.abs(z) > 10 ** (-1.5 / 20)
    print(f"limiter: {over.sum()} samples over -1.5 dBFS ({100*over.mean():.3f}%), worst {20*np.log10(np.abs(z).max()):+.1f} dBFS")
    for n, ra, rb in regions:
        seg = z[int(ra * SR):int(rb * SR)]
        w = 20 * np.log10(np.abs(seg).max() + 1e-9) + 1.5
        if w > 0.5: print(f"   limiter on {n.split('@')[0]:5}: up to {w:.1f} dB on {int((np.abs(seg) > 10 ** (-1.5 / 20)).sum())} samples")
    ff("-i", norm, "-af", "alimiter=limit=0.84:attack=3:release=80:level=false,aresample=48000", "-ac", "2", "-c:a", "pcm_s16le", out_wav)
    return out_wav

def meas(f):
    return [lufs_file(f, a + 0.03, max(0.4, b - a - 0.06)) for _, a, b in regions]

L0 = meas(den)
gains = [min(MAX_GAIN, TARGET + offset(n) - L) for (n, _, _), L in zip(regions, L0)]
for it in range(ITER):
    L = meas(chain(gains, None))
    base = [v - offset(n) for (n, _, _), v in zip(regions, L)]
    med = sorted(base)[len(base) // 2]
    print(f"iter {it}: spread {max(base)-min(base):.1f} dB  " + " ".join(f"{n.split('@')[0]}:{v:.1f}" for (n, _, _), v in zip(regions, L)))
    gains = [min(MAX_GAIN, g + (med + offset(n) - v)) for (n, _, _), g, v in zip(regions, gains, L)]
wav = chain(gains, os.path.join(tmp, "final.wav"), final=True)
out = footage + ".tmp.mp4"
ff("-i", footage, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out)
os.replace(out, footage)
print("gains:", " ".join(f"{n.split('@')[0]}:{g:+.1f}" for (n, _, _), g in zip(regions, gains)))
