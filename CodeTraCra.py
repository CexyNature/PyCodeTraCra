import cv2
import numpy as np
import csv

win = 'C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4'
mac = '/Users/Cesar/PyCode_MacOSv1/GP010016_fast.mp4'

vid = cv2.VideoCapture(mac)
_, prev = vid.read()

Frames = vid.get(7)
print('Total number of frames = ' + str(Frames))

# Initialize lists for frame counter
frame_counter = 1
outputFrameIndices = []

# Create file to print results
resultFile = open('cnt.csv', 'w', newline = '\n')
wr = csv.writer(resultFile, delimiter = ",")
wr.writerow(['Total number of frames = ' + str(Frames)])
wr.writerow(['Frame', 'Contour list', 'Coord x', 'Coord y'])

# Creating mask
mask = np.zeros(prev.shape, dtype = np.uint8)
roi_corners = np.array([[(300, 360), (300, 600), (910, 600), (910, 100), (510, 100), (300, 360)]], dtype = np.int32)
# Fill the ROI so it doesn't get wiped out when the mask is applied
channel_count = prev.shape[2]
ignore_mask_color = (255, ) * channel_count
cv2.fillPoly(mask, roi_corners, ignore_mask_color)

# Initialize background-subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(history = 500, varThreshold = 30, detectShadows = False)
fgbg2 = cv2.createBackgroundSubtractorKNN()

while(vid.isOpened()):
    ret, next = vid.read()

    if ret == True:
        outputFrameIndices.append(frame_counter)
        print("Frame number: " + str(len(outputFrameIndices)))

        # Apply mask to image
        frame = cv2.bitwise_and(next, mask)

        # blurred = cv2.GaussianBlur(frame, (5,5), 4)
        bit_fil = cv2.bilateralFilter(frame, 5, 75, 75)
        # bit_fil = cv2.cvtColor(bit_fil, cv2.COLOR_BGR2GRAY)

        # fgmask = fgbg.apply(bit_fil)
        fgmask = fgbg.apply(bit_fil, learningRate = 0.001)
        # fgmask2 = fgbg2.apply(bit_fil)

        # fgmask_f = fgbg.apply(frame)
        # fgmask2_f = fgbg2.apply(frame)

        mask_blur = cv2.GaussianBlur(fgmask, (3, 3), sigmaX=5, sigmaY=1)
        mask_blur = cv2.resize(mask_blur, (720, 405))
        # cv2.imshow("mask_blur", mask_blur)

        # res = cv2.dilate(mask_blur, cv2.getStructuringElement (cv2.MORPH_ELLIPSE, (1, 1)), iterations = 1)
        # res = cv2.erode(fgmask, (5, 5), iterations = 3)
        # cv2.imshow('res', res)

        _, contours, _ = cv2.findContours(mask_blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            if w > 10 and h > 10 and w < 50 and h < 50:
                cv2.rectangle(next, (x, y), (x+w, y+h), (0, 255, 0), 1)
                center = cv2.circle(next, (int(x+w/2), int(y+h/2)), 1, (0, 0, 255), -1)
                cx = int(x+w/2)
                cy = int(y+h/2)

                # print(len(center))

                points = (cx, cy)

                # print(points)

                wr.writerow([(str(len(outputFrameIndices))), cnt, cx, cy])

        # cv2.imshow("blurred", blurred)
        # cv2.imshow("blur", bit_fil)
        # cv2.imshow('MOG2', fgmask)
        # cv2.imshow('MOG', fgmask2)
        # cv2.imshow("MOG2_f", fgmask2_f)
        # cv2.imshow("MOG_f", fgmask_f)

        # cv2.imshow('next', next)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break

vid.release()
cv2.destroyAllWindows()
resultFile.close()
