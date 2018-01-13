import cv2
import numpy as np
import glob
import os

print(cv2.__version__)

cap = cv2.VideoCapture(1)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Load previously saved data
with np.load('B_480.npz') as X:
    dist, mtx = [X[i] for i in X]
print(mtx)
print(dist)

objp = np.zeros((7*5, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

sh = (0, 0, 0)
while True:
    os.sys.exc_clear()
    _, img = cap.read()
    #img = cv2.resize(img, (640, 360))
    sh = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 5))

    if ret:
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        cv2.drawChessboardCorners(img, (7, 5), corners2, ret)
        retval, rvec, tvec = cv2.solvePnP(objp, corners, mtx, dist, flags=cv2.SOLVEPNP_ITERATIVE)
        #retval, rvec, tvec, inliers = cv2.solvePnPRansac(objp, corners, mtx, dist,
                                          # flags=cv2.SOLVEPNP_ITERATIVE)
        rvec = cv2.Rodrigues(rvec)
        print('wat?? ', retval)
        print('rotation: ', rvec[0])
        print('translation', tvec)


    cv2.imshow('PnP', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
