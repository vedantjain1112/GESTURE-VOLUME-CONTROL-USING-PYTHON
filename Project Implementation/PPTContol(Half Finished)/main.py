import os
import cv2
import imutils
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# CAMERA SETUP

width, height = 1280, 720
folderPath = "Presentation"

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# GET THE LIST OF PRESENTATION IMAGES
pathImages = sorted(os.listdir(folderPath), key=len)
#print(pathImages)

# VARIABLES
imgNumber = 0
hs, ws = (120*1), (213*1)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 20
#annotations = []

# HAND DETECTOR
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:

    # IMPORTING THE IMAGES
    success, img = cap.read()
    img = imutils.resize(img, width=720, height=300)
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        #print(fingers)
        lmList = hand['lmList']
        indexFinger = lmList[8][0], lmList[8][1]

        # CONSTRAIN VALUES FOR EASIER DRAWINGS
        #xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        #yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        #indexFinger = xVal, yVal

        if cy <= gestureThreshold:    # IF HAND IS AT THE HEIGHT OF THE FACE

            # GESTURE 1 - LEFT
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                if imgNumber > 0:
                    buttonPressed = True
                    imgNumber -= 1

            # GESTURE 2 - RIGHT
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                if imgNumber < len(pathImages) - 1:
                    buttonPressed = True
                    imgNumber += 1

        # GESTURE 3 - SHOW POINTER
#        if fingers == [0, 1, 1, 0, 0]:
#            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        # GESTURE 4 - DRAW POINTER
#        if fingers == [0, 1, 0, 0, 0]:
#            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
#            annotations.append(indexFinger)

    # BUTTON PRESSED ITERATIONS
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0;
            buttonPressed = False

#    for i in range(len(annotations)):
#        cv2.line(imgCurrent, annotations[i - 1], annotations[i])

    # ADDING WEB CAM IMAGE ON THE SLIDE
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w-ws:w] = imgSmall

    cv2.imshow("Images", img)
    cv2.imshow("Slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


