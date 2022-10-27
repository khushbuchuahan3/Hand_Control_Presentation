#In This project we can use pinkeyfinger change pages to right and thumb changes pages in left direction
import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=1, detectionCon=0.8)
import os

height, width = 1200, 700
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
hs, ws = int(200), int(200)
imgnumber = 0
folderpath = "images"
pathimages = sorted(os.listdir(folderpath), key=len)
thresold = 300
buttonpressed = False
buttoncounter = 0
buttondelay = 30

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    pathfullimages = os.path.join(folderpath, pathimages[imgnumber])
    imagecurrunt = cv2.imread(pathfullimages)
    imgsmall = cv2.resize(img, (ws, hs))
    h, w, _ = imagecurrunt.shape
    imagecurrunt[0:hs, w - ws:w] = imgsmall
    hands, img = detector.findHands(img)
    cv2.line(img, (0, thresold), (width, thresold), (0, 255, 0), 3)

    if hands and buttonpressed is False:
        hand = hands[0]
        finger = detector.fingersUp(hand)

        cx, cy = hand['center']
        lmList = hand['lmList']
        indexFinger=lmList[8][0],lmList[8][1]

        if cy <= thresold:

            if finger == [1, 0, 0, 0, 0]:

                print("left")
                if imgnumber > 0:
                    buttonpressed = True
                    imgnumber -= 1
            if finger == [0, 0, 0, 0, 1]:

                print("Right")
                if imgnumber < len(pathimages) - 1:
                    buttonpressed = True
                    imgnumber += 1
        if finger == [0, 1, 1, 0, 1]:
            cv2.circle(imagecurrunt,indexFinger,20,(255,0,0),cv2.FILLED)

    if buttonpressed:
        buttoncounter += 1
        if buttoncounter > buttondelay:
            buttoncounter = 0
            buttonpressed = False

    cv2.imshow("img1", imagecurrunt)
    cv2.imshow("img", img)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyWindow()