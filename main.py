import cv2;
import os;
import mediapipe as mp 
import numpy as np

from cvzone.HandTrackingModule import HandDetector


width,height =1280,720
folderPath = "images"

#camera setup
cap=cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

#get the list
pathImages = sorted(os.listdir(folderPath),key=len)
#print(pathImages)

imgNumber = 0
hs,ws = int(180*1),int(320*1)
gestureThreshold = 250
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationNumber = 0
annotationStart =  False

#Hand Detector
detector = HandDetector(detectionCon=0.8,maxHands=1)
while True:
 success,img = cap.read()
 img = cv2.flip(img, 1)
 pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
 imgCurrent=cv2.imread(pathFullImage)
 
 imgCurrent=cv2.resize(imgCurrent,(1280,720))
 
 hands,img=detector.findHands(img)
 
 if hands and buttonPressed is False:
     hand = hands[0]
     fingers = detector.fingersUp(hand)
     cx,cy =hand['center']
     lmList=hand['lmList']
     
     #constrain values for easier drawing
     indexFinger = lmList[8][0],lmList[8][1]
     xVal = int(np.interp(lmList[8][0],[width //2,width],[0,width]))
     yVal = int(np.interp(lmList[8][1],[100,height-100],[0,height]))
     indexFinger = xVal,yVal
     
     if cy <= gestureThreshold:
         annotationStart =  False
        #Gesture 1 - left 
         if fingers == [1, 0, 0, 0, 0]:
             annotationStart =  False
             #print("Left")
             if imgNumber>0:
              buttonPressed= True
              annotations = [[]]
              annotationNumber = 0
              imgNumber -= 1
         
         #Gesture 2 - right    
         if fingers == [1, 0, 0, 0, 1]:
             annotationStart =  False
             #print("Right")
             if imgNumber <len(pathImages)-1:
              buttonPressed= True
              annotations = [[]]
              annotationNumber = 0            
              imgNumber += 1   
         
    #Gesture 3 - pointer
     if fingers  == [0, 1, 1, 0, 0]:
      cv2.circle(imgCurrent,indexFinger,12,(0,0,225),cv2.FILLED)
      annotationStart =  False
       
       #Gesture 4 - draw
     if fingers  == [0, 1, 0, 0, 0]:
         if annotationStart is False:
              annotationStart =True
              annotationNumber +=1
              annotations.append([])
         cv2.circle(imgCurrent,indexFinger,12,(0,0,225),cv2.FILLED)
         annotations[annotationNumber].append(indexFinger)      
     else:
         annotationStart = False
         
       #Gesture 5 - erase   
     if fingers  == [1, 1, 1, 1, 1]:
         if annotations:
             if annotationNumber>=0:
              annotations.pop(-1)
              annotationNumber -= 1
              buttonPressed = True
             
 else:
    annotationStart =  False   
    
 if buttonPressed:
  buttonCounter +=1  
  if buttonCounter> buttonDelay:
         buttonCounter = 0
         buttonPressed = False
 
 for i in range (len(annotations)):
     for j in range(len(annotations[i])):
       if j !=0:
        cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)
 
 cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)
 imgSmall = cv2.resize(img,(ws,hs))
 h, w, _ = imgCurrent.shape
 imgCurrent[0:hs, w - ws:w] = imgSmall
 
 cv2.imshow("Image",img)
 cv2.imshow("Slides",imgCurrent)
 key=cv2.waitKey(1)
 if key == ord('q'):
  break


