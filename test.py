import cv2
import numpy as np
import csv
import dlib

cap = cv2.VideoCapture("C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4")

_, prev = cap.read()

Frames = cap.get(7)
print('Frames='+str(Frames))

frame_counter=1

#Initialize lists for frame counter
outputFrameIndices=[]

resultFile = open("cnt.csv", "w")
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
fgbg2 = cv2.createBackgroundSubtractorKNN()

while(1):
    ret, next = cap.read()

    outputFrameIndices.append(frame_counter)
    print("Number of frames: " + str(len(outputFrameIndices)))

    frame = cv2.bitwise_and(next, mask)

    # blurred = cv2.GaussianBlur(frame, (5,5), 4)
    bit_fil = cv2.bilateralFilter(frame, 5, 75, 75)
    # fgmask = fgbg.apply(bit_fil)
    fgmask2 = fgbg.apply(bit_fil)

    # fgmask_f = fgbg.apply(frame)
    # fgmask2_f = fgbg2.apply(frame)

    mask_blur = cv2.GaussianBlur(fgmask2, (3,3), sigmaX=5, sigmaY=1)
    # cv2.imshow("mask_blur", mask_blur)

    res = cv2.erode(mask_blur, (5,5), iterations=3)
    cv2.imshow("res", res)

    _, contours, _ = cv2.findContours(res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if w > 5 and h > 5 and w < 40 and h < 40:
            cv2.rectangle(next, (x,y), (x+w, y+h), (0,255,0),1)
            center = cv2.circle(next, (int(x+w/2), int(y+h/2)), 1,(0,0,255), -1)
            cx = int(x+w/2)
            cy = int(y+h/2)

            # print(len(center))

            points = (cx, cy)

            print(points)

            wr.writerow([(str(len(outputFrameIndices))),cnt, cx, cy])

    # cv2.imshow("blurred", blurred)
    # cv2.imshow("blur", bit_fil)
    # cv2.imshow('MOG2', fgmask)
    cv2.imshow('MOG', fgmask2)
    # cv2.imshow("MOG2_f", fgmask2_f)
    # cv2.imshow("MOG_f", fgmask_f)

    cv2.imshow('next', next)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
resultFile.close()