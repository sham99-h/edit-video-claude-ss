import cv2, json, subprocess, sys, numpy as np
src, boxes_f, out = sys.argv[1:4]
B = np.array([b[1:5] for b in json.load(open(boxes_f))], float)
ok_ = np.array([b[5] for b in json.load(open(boxes_f))])
for i in range(len(B)):            # hold last good box when lost
    if not ok_[i] and i: B[i] = B[i-1]
K = 5                               # temporal smoothing
Bs = np.array([np.median(B[max(0,i-K//2):i+K//2+1], axis=0) for i in range(len(B))])
cap = cv2.VideoCapture(src)
W, H = 1080, 1920
p = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30",
    "-i","-","-i",src,"-map","0:v","-map","1:a","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
    "-g","15","-keyint_min","15","-sc_threshold","0","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
    "-c:a","copy","-movflags","+faststart",out], stdin=subprocess.PIPE)
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    x, y, w, h = Bs[min(i, len(Bs)-1)]
    px, py = w*0.12, h*0.30
    x0, y0 = int(max(0, x-px)), int(max(0, y-py)); x1, y1 = int(min(W, x+w+px)), int(min(H, y+h+py))
    if x1 > x0+4 and y1 > y0+4:
        roi = f[y0:y1, x0:x1]
        small = cv2.resize(roi, (max(1,(x1-x0)//14), max(1,(y1-y0)//14)), interpolation=cv2.INTER_AREA)
        pix = cv2.resize(small, (x1-x0, y1-y0), interpolation=cv2.INTER_NEAREST)
        pix = cv2.GaussianBlur(pix, (0,0), 6)
        m = np.zeros((y1-y0, x1-x0), np.float32); r=8
        m[r:-r, r:-r] = 1; m = cv2.GaussianBlur(m, (0,0), 4)[..., None]
        f[y0:y1, x0:x1] = (pix*m + roi*(1-m)).astype(np.uint8)
    p.stdin.write(f.tobytes()); i += 1
p.stdin.close(); p.wait(); print(i, "frames written")
