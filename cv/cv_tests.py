#!/usr/bin/env python
import cv2
import cv2.cv as cv
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


def shape_callback(msg):
    plt.figure(1)
    im = cv2.imread('raw_images/image1.jpg')
    h, w = im.shape[:2]

    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    img_filt = cv2.medianBlur(img, 55)
    img_th = cv2.adaptiveThreshold(img_filt, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    ret, thresh = cv2.threshold(img,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    size = h, w, 3

    # TODO find useful contour
    m = np. zeros(size, dtype=np.uint8)
    m[:, :, :] = (255, 255, 255)
    cv2.drawContours(m, contours, 2, (0, 0, 255), 3)
    plt.subplot(221)
    plt.imshow(m)

    cnt = contours[2]
    mts = cv2.moments(cnt)

    cx = int(mts['m10'] / mts['m00'])
    cy = int(mts['m01'] / mts['m00'])
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)

    epsilon = 0.1 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    m = np. zeros(size, dtype=np.uint8)
    m[:, :, :] = (255, 255, 255)
    cv2.drawContours(m, cnt, -1, (255, 0, 0), 3)
    plt.subplot(222)
    plt.imshow(m)

    hull = cv2.convexHull(cnt)

    m = np. zeros(size, dtype=np.uint8)
    m[:, :, :] = (255, 255, 255)
    cv2.drawContours(m, hull, -1, (0, 255, 0), 3)
    plt.subplot(223)
    plt.imshow(m)

    k = cv2.isContourConvex(hull)
    # rectangle
    x, y, w, h = cv2.boundingRect(hull)
    cv2.rectangle(m, (x, y), (x + w, y + h), (0, 255, 0), 10)
    # circle
    (x, y), radius = cv2.minEnclosingCircle(hull)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(m, center, radius, (0, 0, 255), 10)
    # ellipse
    ellipse = cv2.fitEllipse(hull)
    cv2.ellipse(m, ellipse, (0, 255, 0), 2)

    print(k)
    print(cx, cy, area, perimeter)

    plt.hlines(cy, 0, w)
    plt.vlines(cx, 0, h)

    print(h, w)
    plt.show()

shape_callback(1)

for i in range(0, len(contours)):
    if cv2.contourArea(contours[i]) < 100:
        continue
    approx = self.getApprox(contours[i])
    self.drawContourEx(canvas, approx)

cv2.imshow('frame1', canvas)
