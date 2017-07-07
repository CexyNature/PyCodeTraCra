### to do: Instead of selecting ROI Manually try with cv2.selectROI command
### apply MeanShift to image of blobs from one channel.

import numpy as np
import cv2

win = "C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4"
mac = "/Users/Cesar/PyCode_MacOSv1/GP010016_fast.mp4"

vid = cv2.VideoCapture(win)

_, prev = vid.read()

# Creating mask
mask = np.zeros(prev.shape, dtype=np.uint8)


roi_corners = np.array([[(300, 360), (300, 600), (910, 600), (910, 100), (510,100), (300, 360)]], dtype=np.int32)
# fill the ROI so it doesn't get wiped out when the mask is applied
channel_count = prev.shape[2]
ignore_mask_color = (255,) * channel_count
cv2.fillPoly(mask, roi_corners, ignore_mask_color)

fgbg = cv2.createBackgroundSubtractorMOG2()
fgbg2 = cv2.createBackgroundSubtractorKNN()

#setup initial location of window
r,h,c,w = 340,50,650,50
# 570,420
# 745,490
# 650,349
track_window = (c,r,w,h)

#set up the ROI for tracking
roi = prev[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask1,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,next = vid.read()
    if ret == True:

        frame = cv2.bitwise_and(next, mask)
        bit_fil = cv2.bilateralFilter(frame, 5, 75, 75)
        fgmask2 = fgbg.apply(bit_fil)
        mask_blur = cv2.GaussianBlur(fgmask2, (3, 3), sigmaX=5, sigmaY=1)
        res = cv2.erode(mask_blur, (5, 5), iterations=3)
        # cv2.imshow("res", res)

        _, contours, _ = cv2.findContours(res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # for cnt in contours:
        #     x, y, w, h = cv2.boundingRect(cnt)
        #
        #     if w > 5 and h > 5 and w < 40 and h < 40:
        #         cv2.rectangle(next, (x, y), (x + w, y + h), (0, 255, 0), 1)
        #         center = cv2.circle(next, (int(x + w / 2), int(y + h / 2)), 1, (0, 0, 255), -1)


        masked = cv2.bitwise_and(next, next, mask=res)
        cv2.imshow('masked', masked)
        # cv2.imshow('next', next)

        hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([masked],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x,y,w,h = track_window
        img2 = cv2.rectangle(next, (x,y), (x+w,y+h), 255,2)
        cv2.imshow('img2',img2)
        # cv2.imshow('hsv', hsv)
        # cv2.imshow('dst', dst)


        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break


    else:
        break

vid.release()
cv2.destroyAllWindows()
