import cv2
import numpy as np

cap = cv2.VideoCapture("C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016.mp4")

fgbg = cv2.createBackgroundSubtractorMOG2()
fgbg2 = cv2.createBackgroundSubtractorKNN()


while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)


    cv2.imshow('MOG2', fgmask)
    cv2.imshow('MOG', fgmask2)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()