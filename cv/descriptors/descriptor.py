import cv2
from matplotlib import pyplot as plt
from trackbar import Filter, Trackbar

f_qmax = Filter("qc", 0, 1000, 100)
f_q = Filter("x", 0, 1, 0.1)
f_dist = Filter("k", 0, 1000, 100)
tbs = Trackbar(f_qmax, f_q, f_dist)


def getPointsForTracking(image, qmax, q, dist):
    corners = cv2.goodFeaturesToTrack(image, qmax, q+0.1, dist)
    crnrs = (corners[:, 0, 0], corners[:, 0, 1])
    return crnrs


# frame = "../raw_images/for_descriptor.jpg"
cap = cv2.VideoCapture(0)
while True:
    m, q,d = tbs.get_trackbar_values()
    _, frame = cap.read()
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(m,q,d)
    corners = getPointsForTracking(imgray, m,0.01,d)
    kps = []
    for c in corners:
        kp = cv2.KeyPoint(c[0], c[1], 100)
        kps.append(kp)

    cv2.drawKeypoints(imgray, kps, frame)
    cv2.imshow("l", frame)

    if cv2.waitKey(1) & 0xFF is ord('q'):
        break