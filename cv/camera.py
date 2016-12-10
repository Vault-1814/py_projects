import numpy as np
import cv2
import imutils

cap = cv2.VideoCapture(1)

while True:
    cx = []
    cy = []
    ret, frame = cap.read()
    h, w = frame.shape[:2]
    # print(h, w)
    h, w = (600, 600)
    frame = cv2.resize(frame, (h, w))

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #img_gray_gaus = cv2.resize(img_gray, (300, 300))
    img_blure = cv2.GaussianBlur(img_gray, (5, 5), 0)
    #thresh = cv2.adaptiveThreshold(img_blure, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    ret, thresh = cv2.threshold(img_blure, 127, 255, 0)
    thresh = cv2.threshold(img_blure, 60, 255, cv2.THRESH_BINARY_INV)[1]
    ret, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.cv.CV_DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    # Marker labelling
    markers = np.zeros((h, w), np.int32)
    markers_vis = sure_fg.copy()
    cur_marker = 1
    colors = np.int32(list(np.ndindex(2, 2, 2))) * 255
    #ret, markers = cv2.connectedComponents(sure_fg)
    markers_vis = markers_vis + 1
    markers_vis[unknown == 255] = 0

    size = h, w, 3
    m = np.zeros(size, dtype=np.uint8)
    m[:, :, :] = (255, 255, 255)

    markers = cv2.watershed(m, markers)
    m[markers == -1] = [255, 0, 0]
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0] if imutils.is_cv2() else contours[1]

    size = h, w, 3
    m = np.zeros(size, dtype=np.uint8)
    m[:, :, :] = (255, 255, 255)


    for i in range(0, len(contours)):
        hull = cv2.convexHull(contours[i])
        epsilon = 0.001 * cv2.arcLength(hull, True)
        approx = cv2.approxPolyDP(hull, epsilon, True)
        cv2.drawContours(m, approx, -1, (0, 0, 255), 3)
        #x, y, w, h = cv2.boundingRect(hull)
        #cv2.rectangle(m, (x, y), (x + w, y + h), (0, 255, 0), 1)
        mts = cv2.moments(contours[i])
        if mts['m00'] != 0:
            cx.append(int(mts['m10'] / mts['m00']))
            cy.append(int(mts['m01'] / mts['m00']))

    for j in range(0, len(cx)):
        cv2.line(m, (0, cy[j]), (2 * h, cy[j]), (0, 0, 0))
        cv2.line(m, (cx[j], 0), (cx[j], 2 * w), (0, 0, 0))
    #cv2.drawContours(m, contours, -1, (0, 0, 255), 1)

    def geometry():
        mts = cv2.moments(hull)
        cx = int(mts['m10'] / mts['m00'])
        cy = int(mts['m01'] / mts['m00'])
        area = cv2.contourArea(hull)
        perimeter = cv2.arcLength(hull, True)

        epsilon = 0.001 * cv2.arcLength(hull, True)
        approx = cv2.approxPolyDP(hull, epsilon, True)
        size = h, w, 3
        m = np.zeros(size, dtype=np.uint8)
        m[:, :, :] = (255, 255, 255)
        cv2.drawContours(m, approx, -1, (0, 0, 255), 1)
        x, y, w, h = cv2.boundingRect(hull)
        cv2.rectangle(m, (x, y), (x + w, y + h), (0, 255, 0), 1)
        # circle
        (x, y), radius = cv2.minEnclosingCircle(hull)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(m, center, radius, (0, 0, 255), 1)
        # ellipse
        #ellipse = cv2.fitEllipse(hull)
        #Xcv2.ellipse(m, ellipse, (255, 0, 0), 1)
        # center
        cv2.line(m, (0, cy), (2*h, cy), (0, 0, 0))
        cv2.line(m, (cx, 0), (cx, 2 * w), (0, 0, 0))

    cv2.imshow('frame2', thresh)
    cv2.imshow('frame3', m)

    #cv2.putText(blure, str(frame), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    # Display the resulting frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()