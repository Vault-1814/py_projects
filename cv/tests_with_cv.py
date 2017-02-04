import numpy as np
import cv2
import imutils
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(1)


while True:
    _, frame = cap.read()

    print(frame.shapexx)

    cv2.imshow("a", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
