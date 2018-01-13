import cv2

PATH = 'cv2_640_480/'

cap = cv2.VideoCapture(1)

count = 35
while True:
    _, img = cap.read()
    cv2.imshow('calib', img)
    cv2.moveWindow('calib', 100, 100)
    k = cv2.waitKey(6) & 0xFF
    if k in [27, ord('q')]:
        break
    elif k == ord('s'):
        cv2.imwrite(PATH + str(count) + '.png', img)
        count += 1
        print(str(count) + 'frame saved!')
        continue
