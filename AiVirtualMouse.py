import cv2
from cv2 import CAP_DSHOW
from matplotlib.pyplot import flag
import numpy as np
import handtracking as htm
import time
from win32api import GetSystemMetrics
from pynput.mouse import Button, Controller
 
##########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 2
#########################

mouse = Controller()
flag = 1

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = GetSystemMetrics(0),GetSystemMetrics(1)
# print(wScr, hScr)
 
while True:

    # 1. Find hand Landmarks
    success, img = cap.read()

    #perscpective Transformation
    # pts1 = np.float32([[0, 0], [0, 0], [0, 0], [0, 0]])
    # pts2 = np.float32([[0, 0], [wCam, 0],[0, hCam], [wCam, hCam]])
    # matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # img = cv2.warpPerspective(img, matrix, (640, 480))

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
    
        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        # cv2.rectangle(img, (259, 179), (497, 340),
        # (255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (0, wCam), (0, wScr))
            y3 = np.interp(y1, (0, hCam), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
        
            # 7. Move Mouse
            mouse.position = (clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

            if fingers[2] == 1:
                if flag == 1:
                    mouse.press(Button.left)
                    if fingers[2] == 1:
                        flag = 0
            else:
                mouse.release(Button.left)
                flag = 1
        # # 8. Both Index and middle fingers are up : Clicking Mode
        # if fingers[1] == 1 and fingers[2] == 1:
        #     # 9. Find distance between fingers
        #     length, img, lineInfo = detector.findDistance(8, 12, img)
        #     print(length)
        #     # 10. Click mouse if distance short
        #     if length < 40:
        #         cv2.circle(img, (lineInfo[4], lineInfo[5]),
        #         15, (0, 255, 0), cv2.FILLED)
        #         if flag == 1:
        #             mouse.press(Button.left)
        #             if length < 40:
        #                 flag = 0
        #     else:
        #         mouse.release(Button.left)
        #         flag = 1    
    
    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)