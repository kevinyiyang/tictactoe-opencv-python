import cv2
import time
import numpy as np
import imutils

video = cv2.VideoCapture(0)


images = []

maxImageCount = 10;
i = 0;

while True:
    check, frame = video.read()


    if i < maxImageCount:
        images.append(frame);

    #avgImage =

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray,25,20,20)
    edged = cv2.Canny(gray,30, 200)


    #find all contours that are rectangles
    cnts = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse = True)[:1]
    screenCnt = None


    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015*peri, True)

        if len(approx) == 4:

            screenCnt = approx
            #cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)



    cv2.imshow("Capturing", frame)

    key = cv2.waitKey(100)

    if key == ord('q'):
        break


video.release()

cv2.destroyAllWindows()