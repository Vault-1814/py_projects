import numpy as np
import cv2
import imutils
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

_, frame = cap.read()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
plt.imshow(hsv)

plt.show()

while False:
    cv2.imshow("a", hsv)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
