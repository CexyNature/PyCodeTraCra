import cv2
import sys
import csv
from datetime import datetime
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True, help='Path to the video file')
ap.add_argument('-m', '--method', required = True, help = 'Select one method: BOOSTING, MIL, KCF, TLD, MEDIANFLOW')
args = vars(ap.parse_args())

startTime = datetime.now()

win = "C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4"
win = "C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/VIRB0009.mp4"
mac = "/Users/Cesar/PyCode_MacOSv1/GP010016_fast.mp4"
mac2 = '/Users/Cesar/PyCode_MacOSv1/VIRB0006.MP4'

resultFile = open("Tracking.csv", "w", newline='\n')
wr = csv.writer(resultFile, delimiter=",")
wr.writerow(['Coord x','Coord y'])
position = (0,0)

# Set up tracker.
# Instead of MIL, you can also use
# BOOSTING, MIL, KCF, TLD, MEDIANFLOW or GOTURN

tracker = cv2.Tracker_create(args['method'])

# Read video
vid = cv2.VideoCapture(args['video'])

# Exit if video not opened
if not vid.isOpened():
    print("Could not open video")
    sys.exit()

# Read first frame
ok, frame = vid.read()
if not ok:
    print('Cannot read video file')
    sys.exit()

# Define an initial bounding box
# bbox = (650, 355, 25, 25)
bbox = cv2.selectROI('tracking select', frame, fromCenter=False)

# Uncomment the line below to select a different bounding box
# bbox = cv2.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bbox)

fgbg = cv2.createBackgroundSubtractorMOG2(history = 500, varThreshold = 30, detectShadows = False)

while True:
    # Read a new frame
    ok, frame = vid.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not ok:
        break

    # frame1 = fgbg.apply(frame)
    # frame1 = cv2.erode(frame1, (5, 5), iterations=4)
    # frame1 = cv2.dilate(frame1, (2,2), iterations=8)
    # frame2 = cv2.bitwise_and(frame1, frame)
    # frame3 = np.array(abs(np.array(frame1, np.float32) - np.array(frame, np.float32)), np.uint8)
    # cv2.imshow('frame1', frame1)
    # cv2.imshow('frame2', frame2)
    # cv2.imshow('frame3', frame3)

    # Update tracker
    ok, bbox = tracker.update(frame)
    position = (bbox[0],bbox[1])
    # print(position)
    wr.writerow(position)
    # Draw bounding box
    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0, 0, 255))

    # Display result
    cv2.imshow("Tracking", frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
vid.release()
cv2.destroyAllWindows()
print(datetime.now() - startTime)
