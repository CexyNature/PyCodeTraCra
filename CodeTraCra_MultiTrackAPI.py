import numpy as np
import cv2
import sys

pathW = "C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4"
pathM = "/Users/Cesar/PyCode_MacOSv1/GP010016_fast.mp4"

print('Select 3 tracking targets')

cv2.namedWindow("tracking")
camera = cv2.VideoCapture(pathM)
tracker = cv2.MultiTracker('MIL')
init_once = False

ok, image=camera.read()
if not ok:
    print('Failed to read video')
    exit()

bbox1 = cv2.selectROI('tracking', image, fromCenter=False)
bbox2 = cv2.selectROI('tracking', image, fromCenter=False)
bbox3 = cv2.selectROI('tracking', image, fromCenter=False)

while camera.isOpened():
    ok, image=camera.read()
    if not ok:
        print('no image to read')
        break

    if not init_once:
        ok = tracker.add(image, bbox1)
        ok = tracker.add(image, bbox2)
        ok = tracker.add(image, bbox3)
        init_once = True

    ok, boxes = tracker.update(image)
    print(ok, boxes)

    for newbox in boxes:
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(image, p1, p2, (200,0,0))

    cv2.imshow('tracking', image)
    k = cv2.waitKey(1)
    if k == 27 : break # esc pressed

camera.release()
cv2.destroyAllWindows()