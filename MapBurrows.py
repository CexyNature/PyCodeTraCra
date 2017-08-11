import cv2
import numpy as np
import csv
from pymouse import PyMouseEvent


cap = cv2.VideoCapture('C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4')
_, prev = cap.read()

Frames = cap.get(7)
print('Frames = '+str(Frames))

frame_counter = 1
#Initialize lists for frame counter
outputFrameIndices = []

resultFile = open("burrows.csv", "w")
wr = csv.writer(resultFile, delimiter=",")

# cx,cy = 0,0

# Creating mask
mask = np.zeros(prev.shape, dtype=np.uint8)
roi_corners = np.array([[(300, 360), (300, 600), (910, 600), (910, 100), (510,100), (300, 360)]], dtype=np.int32)
# fill the ROI so it doesn't get wiped out when the mask is applied
channel_count = prev.shape[2]
ignore_mask_color = (255,) * channel_count
cv2.fillPoly(mask, roi_corners, ignore_mask_color)

fgbg = cv2.createBackgroundSubtractorMOG2()
fgbg2 = cv2.createBackgroundSubtractorKNN()q

while(1):
    ret, next = cap.read()
    frame = cv2.bitwise_and(next, mask)
    outputFrameIndices.append(frame_counter)
    # print("Number of frames: " + str(len(outputFrameIndices)))

    wr.writerow([(str(len(outputFrameIndices)))])

    cv2.imshow('frame masked', frame)

    class DetectMouseClick(PyMouseEvent):
        def __init__(self):
            PyMouseEvent.__init__(self)

        def click(self, x, y, button, press):
            if button == 1:
                if press:
                    print("click", '({},{})'.format(x, y))
            else:
                self.stop()


    O = DetectMouseClick()
    O.run()

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
resultFile.close()