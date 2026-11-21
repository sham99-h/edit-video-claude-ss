import cv2, json, sys
src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src)
S = 0.5
init = (415, 1470, 243, 65)  # x,y,w,h at full res, frame @1.0s (plate visible from 0)
boxes = []
tr = None
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    small = cv2.resize(f, None, fx=S, fy=S)
    if tr is None:
        tr = cv2.TrackerCSRT_create()
        tr.init(small, tuple(int(v*S) for v in init))
        box, okt = init, True
    else:
        okt, b = tr.update(small)
        box = tuple(v / S for v in b) if okt else boxes[-1][1:5]
    boxes.append([i, *[round(v, 1) for v in box], bool(okt)])
    i += 1
json.dump(boxes, open(out, 'w'))
print(i, 'frames; lost', sum(1 for b in boxes if not b[5]))
