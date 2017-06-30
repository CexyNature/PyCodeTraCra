import cv2
import numpy as np
import csv

pathW = "C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4"
pathM = "/Users/Cesar/PyCode_MacOSv1/GP010016_fast.mp4"


resultFile = open("burrows.csv", "w")
wr = csv.writer(resultFile, delimiter=",")

#Initialize list of clicks coordinates
burrows = []
Counter_burrow = 0
position = (0,0)

pos = (0,0)

def click(event, x, y, flags, param):
    global burrows, burrows_counter, position, pos

    if event == cv2.EVENT_LBUTTONDOWN:
        # burrows = [(x, y)]
        position = (x, y)
        burrows.append(position)
        wr.writerow(position)
        print(burrows)
        print(position)

    if event == cv2.EVENT_MOUSEMOVE:
        pos = (x, y)

cap = cv2.VideoCapture(pathM)

while(cap.isOpened()):

    ret, next = cap.read()

    cv2.namedWindow('next')
    cv2.setMouseCallback('next', click)

    for i, val in enumerate(burrows):
        cv2.circle(next, val, 3, (0, 255, 0), 2)
        Counter_burrow = i + 1

    cv2.putText(next, "Number of burrows detected {}".format(Counter_burrow), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(next, "Last burrow coordinate {}".format(position), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 255, 255), 2)
    cv2.putText(next, "Mouse position {}".format(pos), (50, 710), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)


    cv2.imshow('next', next)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

# close all open windows
cv2.destroyAllWindows()
resultFile.close()