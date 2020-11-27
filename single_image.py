import cv2
import time
import numpy as np
import imutils

boardState = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]

# image from webcam
img = cv2.imread("board-00+22-1.png")


# isolate board from whole image
# convert to grayscale/apply blur/canny
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray,25,20,20)
edged = cv2.Canny(gray,30, 200)
# get contours
cnts = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse = True)[:10]

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.1 * peri, True)

    if len(approx) == 4:
        screenCnt = approx
        break;


#cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

# Analyze board
board = img[screenCnt[0,0,1]:screenCnt[2,0,1],screenCnt[2,0,0]:screenCnt[0,0,0]]

# f
b_gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
b_gray = cv2.bilateralFilter(b_gray,25,20,20)
b_edged = cv2.Canny(b_gray,30, 200)

b_cnts = cv2.findContours(b_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
b_cnts = imutils.grab_contours(b_cnts)
b_cnts = sorted(b_cnts, key=cv2.contourArea, reverse = True)[:10]


for c in b_cnts:
    b_peri = cv2.arcLength(c, True)
    b_approx = cv2.approxPolyDP(c, 0.15 * b_peri, True)

    if len(b_approx) >= 4:
        boardCnt = b_approx
        cv2.drawContours(board, [boardCnt], -1, (0, 255, 0), 3)




cv2.imshow("Capturing", board)
print(board.shape)

key = cv2.waitKey(0)




cv2.destroyAllWindows()