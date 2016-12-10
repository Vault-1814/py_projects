import numpy as np
import cv2
import imutils

class VideoCV:

    def __init__(self, cameraId):
        self.cap = cv2.VideoCapture(cameraId)
        if self.cap is None:
            raise Exception('Failed video flow for camera %s', cameraId)

    def getRawFrame(self, resize=False, height=300, width=300):
        ret, frame = self.cap.read()
        if resize:
            frame = cv2.resize(frame, (height, width))
        return frame

    def getThresholdImage(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blure = cv2.GaussianBlur(img_gray, (5, 5), 0)
        # thresh = cv2.adaptiveThreshold(img_blure, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        ret, thresh = cv2.threshold(img_blure, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return thresh

    def getContours(self, thresh):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    # only for convex hull
    def getApprox(self, contour):
        hull = cv2.convexHull(contour)
        epsilon = 0.001 * cv2.arcLength(hull, True)
        approx = cv2.approxPolyDP(hull, epsilon, True)
        return approx

    def drawContourEx(self, canvas, contour, color=(0, 0, 255)):
        cv2.drawContours(canvas, contour, -1, color, 3)
        mts = cv2.moments(contour)
        h, w = canvas.shape[:2]
        if mts['m00'] != 0:
            cx = int(mts['m10'] / mts['m00'])
            cy = int(mts['m01'] / mts['m00'])
            cv2.line(canvas, (0, cy), (2 * h, cy), (0, 0, 0))
            cv2.line(canvas, (cx, 0), (cx, 2 * w), (0, 0, 0))

    def getCanvas(self, h, w):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        canvas[:, :, :] = (255, 255, 255)
        return canvas

    def clearCanvas(self, canvas):
        canvas[:, :, :] = (255, 255, 255)
        return canvas

    def run(self):
        frame = self.getRawFrame()
        h, w = frame.shape[:2]
        canvas = self.getCanvas(h, w)
        while True:
            self.clearCanvas(canvas)
            frame = self.getRawFrame()
            thresh = self.getThresholdImage(frame)
            contours = self.getContours(thresh)
            for i in range(0, len(contours)):
                approx = self.getApprox(contours[i])
                self.drawContourEx(canvas, approx)
            cv2.imshow('frame', canvas)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    videoCV = VideoCV(0)
    videoCV.run()

main()
