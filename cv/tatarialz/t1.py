import cv2


print(cv2.__version__)

cap = cv2.VideoCapture(0)

while (True):

    _, f = cap.read()
    cv2.imshow("1", f)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()