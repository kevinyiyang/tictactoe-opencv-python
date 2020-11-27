import cv2
import imutils

# initialize board state
# -1: Human piece
#  0: empty
#  1: Computer piece
boardState = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]

# image from webcam
img = cv2.imread("board-m01.png")


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
if screenCnt is not None:
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
            #cv2.drawContours(board, [boardCnt], -1, (0, 255, 0), 3)




# split board into 9 sections - each will be analyzed for user input
#get dimensions of board
b_h = board.shape[0];
b_w = board.shape[1];

#print(b_h)
#print(b_w)

seg_h = int(b_h/3)
seg_w = int(b_w/3)

#print(seg_h)
#print(seg_w)


#print(board.shape)


#print(board[2*seg_h:3*seg_h,2*seg_w:3*seg_w])
segments = []

PADDING = 10
if boardCnt is not None:
    for i in range(0,3):
        for j in range(0,3):

            segment = board[ i*seg_h + PADDING:(i+1)*seg_h -PADDING, j*seg_w+ PADDING:(j+1)*seg_w - PADDING]

            s_gray = cv2.cvtColor(segment, cv2.COLOR_BGR2GRAY)
            s_gray = cv2.bilateralFilter(s_gray, 25, 20, 20)
            s_edged = cv2.Canny(s_gray, 30, 200)

            s_cnts = cv2.findContours(s_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            s_cnts = imutils.grab_contours(s_cnts)
            s_cnts = sorted(s_cnts, key=cv2.contourArea, reverse=True)[:10]

            for c in s_cnts:
                s_peri = cv2.arcLength(c, True)
                s_approx = cv2.approxPolyDP(c, 0.15 * s_peri, True)

                if len(s_approx) >= 4:
                    segCnt = s_approx
                    #cv2.drawContours(board, [segCnt], -1, (0, 255, 0), 3)
                    boardState[i][j] = 1



print(boardState[0])
print(boardState[1])
print(boardState[2])




cv2.imshow("Capturing", board)

key = cv2.waitKey(0)




cv2.destroyAllWindows()