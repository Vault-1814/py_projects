# -*- coding: utf-8
import trackbar as tb
import cv2
import numpy as np
import time
"""
    ./tocfg_image -v 0 -
"""

tbs = tb.Trackbar("configuring image")

def selectCvtColor(frame):
    code = tbs.get_trackbar_value('')
    cv2.cvtColor(frame, code)


def tocfg_threshold(frame):
    fth = tb.Filter('threshold', 1, 500, 1)
    fm = tb.Filter('maxval', 0, 250, 0)
    tbs.add_filters(fth, fm)
    _, fr = cv2.threshold(frame, th, maxval, cv2.THRESH_BINARY)


cap = cv2.VideoCapture(0)

def get_grid_canvas(hor, *frames):
    """выводит кучу кадров на одно полотно по hor штук в строку"""
    h, w, p = frames[0].shape
    qty = len(frames)
    nh, nw = h * qty / hor, w * hor
    canvas = np.zeros((nh, nw, 3), dtype=np.uint8)
    n, i, l = 0, 0, 0
    while i < nh:
        j, k = 0, 0
        while j < nw:
            frame = frames[n]
            # print(n, i, j, l, k)
            if len(frame.shape) == 3:
                canvas[i, j, :] = frame[l, k, :]
            else:
                canvas[i, j, :] = [0, 0, frame[l, k]]
            if k < w - 1:
                k += 1
            else:
                n, k = n + 1, 0
            j += 1
        if l < h - 1:
            l += 1
            n = i // h * hor    # вычисляем номер кадра в начале каждой новой строки
        else:
            l = 0
        i += 1
    return canvas

while True:
    _, fr = cap.read()
    fr = cv2.resize(fr, (320, 240))
    canvas = get_grid_canvas(2, fr, fr, fr, fr)

    """
    selectCvtColor()
    tocfgBlure()
    tocfgGaussianBlure()
    tocfgThreshold()
    tocfgAdaptiveThreshold()
    tocfgCanny()
    """

    while True:
        cv2.imshow("view", canvas)
        if cv2.waitKey(1) & 0xFF == ord('w'):
            break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

