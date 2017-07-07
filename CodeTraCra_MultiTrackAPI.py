import cv2

win = "C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4"
mac = "/Users/Cesar/PyCode_MacOSv1/GP010016_fast.mp4"

print('Select 3 crabs using the bounding box, and press enter or space after each selection')

cv2.namedWindow("tracking")
vid = cv2.VideoCapture(mac)
tracker = cv2.MultiTracker('MIL')
init_once = False

ok, image = vid.read()
if not ok:
    print('Failed to read video')
    exit()

bbox1 = cv2.selectROI('tracking', image, fromCenter = False)
bbox2 = cv2.selectROI('tracking', image, fromCenter = False)
bbox3 = cv2.selectROI('tracking', image, fromCenter = False)
bbox4 = cv2.selectROI('tracking', image, fromCenter = False)
while vid.isOpened():
    ok, image = vid.read()
    if not ok:
        print('no image to read')
        break

    if not init_once:
        ok = tracker.add(image, bbox1)
        ok = tracker.add(image, bbox2)
        ok = tracker.add(image, bbox3)
        ok = tracker.add(image, bbox4)
        init_once = True

    ok, boxes = tracker.update(image)
    print(ok, boxes)

    for newbox in boxes:
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(image, p1, p2, (200, 0, 0))

    cv2.imshow('tracking', image)
    k = cv2.waitKey(1)
    if k == 27:
        print("ESC - key pressed. Window quit by user")
        break  #esc pressed

vid.release()
cv2.destroyAllWindows()