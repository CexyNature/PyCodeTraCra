import cv2
import sys

win = "C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4"
mac = "/Users/Cesar/PyCode_MacOSv1/GP010016_fast.mp4"

# Set up tracker.
# Instead of MIL, you can also use
# BOOSTING, MIL, KCF, TLD, MEDIANFLOW or GOTURN

tracker = cv2.Tracker_create('MIL')

# Read video
vid = cv2.VideoCapture(mac)

# Exit if video not opened.
if not vid.isOpened():
    print
    "Could not open video"
    sys.exit()

# Read first frame.q
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

while True:
    # Read a new frame
    ok, frame = vid.read()
    if not ok:
        break

    # Update tracker
    ok, bbox = tracker.update(frame)

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