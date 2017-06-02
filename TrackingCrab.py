import cv2
import numpy as np

cap = cv2.VideoCapture("C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016.mp4")

_, prev = cap.read()

# Coordinates polygon for mask
pts = np.array([[0, 0], [0, 510], [710, 0]], np.int32)
# Reshaping pts array to be an array of undefined (-1) layers, 1 group layer, and 2 values per group. Basically adding a dim
pts = pts.reshape((-1, 1, 2))

# Creating mask
mask = np.zeros(prev.shape, dtype=np.uint8)
roi_corners = np.array([[(0, 510), (0, 720), (1280, 720), (1280, 0), (710, 0)]], dtype=np.int32)
# fill the ROI so it doesn't get wiped out when the mask is applied
channel_count = prev.shape[2]
ignore_mask_color = (255,) * channel_count
cv2.fillPoly(mask, roi_corners, ignore_mask_color)

# Container for running average
prev_masked = cv2.bitwise_and(prev, mask)
avg = np.float32(prev_masked)

# Creating kernel for closing
kernel = np.ones((1, 1), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
PrevCen = np.array([10, 10])

# Creating second kernel for dilation
kernel1 = np.ones((2, 2), np.uint8)

while True:
    _, next = cap.read()

    masked_image = cv2.bitwise_and(next, mask)
    masked_image_rz = cv2.resize(masked_image, (960, 540))
    cv2.imshow('image_masked_rz', masked_image_rz)

    ##    mask2 = cv2.fillPoly(next, [pts], (0,0,0))
    ##    mask2_rz = cv2.resize(mask2, (960,540))
    ##    cv2.imshow('mask2_rz', mask2_rz)


    cv2.accumulateWeighted(masked_image, avg, 0.001)
    averun = cv2.convertScaleAbs(avg)
    averunG = cv2.cvtColor(averun, cv2.COLOR_BGR2GRAY)
    averunG_rz = cv2.resize(averunG, (960, 540))
    ##    cv2.imshow('averunG_rz', averunG_rz)

    nextG = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    nextG_rz = cv2.resize(nextG, (960, 540))
    ##    cv2.imshow('nextG_rz', nextG_rz)

    flow = np.array(abs(np.array(nextG, np.float32) - np.array(averunG, np.float32)), np.uint8)
    flow_rz = cv2.resize(flow, (960, 540))
    ##    cv2.imshow('flow_rz', flow_rz)


    lower = 50
    upper = 255
    rang = cv2.inRange(flow, lower, upper)
    rang_rz = cv2.resize(rang, (960, 540))
    ##    cv2.imshow('rang_rz', rang_rz)

    opening = cv2.morphologyEx(rang, cv2.MORPH_OPEN, kernel)
    opening_rz = cv2.resize(opening, (960, 540))
    cv2.imshow('opening_rz', opening_rz)

    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    closing_rz = cv2.resize(closing, (960, 540))
    cv2.imshow('closing_rz', closing_rz)

    dilation = cv2.dilate(closing, kernel1, iterations=5)
    dilation_rz = cv2.resize(dilation, (960, 540))
    cv2.imshow('dilation_rz', dilation_rz)

    res = cv2.bitwise_and(masked_image, masked_image, mask=dilation)
    res_rz = cv2.resize(res, (960, 540))
    cv2.imshow("res_rz", res_rz)

    ##    _,contours,_ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ##    cv2.drawContours(next, contours, -1, (200,0,20), 1)

    ##
    ##    M = [0,0]
    ##    n = 0
    ##    for cnt in contours:
    ##        x,y,w,h = cv2.boundingRect(cnt)
    ##        if w>1 and h>1 and w<200 and h<200:
    ##            M[0] += x + float(w)/2.
    ##            M[1] += y + float(h)/2.
    ##            n += 1
    ##
    ##    if M[0]!=0 and M[0]!=0:
    ##        M = np.array(M)
    ##        NewCen = PrevCen + 0.9*(M-PrevCen)
    ##        cntX = int(NewCen[0]/n)
    ##        cntY = int(NewCen[1]/n)
    ##        cv2.circle(next,(cntX,cntY),5,(130,50,200),-1)
    ##        cv2.putText(next,str(cntX)+','+str(cntY), (cntX+10,cntY+10),font,1,(130,50,200))
    ##        PrevCen = NewCen
    ##
    ##    prevG = nextG

    ##    nextrz = cv2.resize(next, (960,540))
    ##    cv2.imshow('nextrz',nextrz)


    k = cv2.waitKey(1) & 0xFF
    if k == 27: break

cap.release()
cv2.destroyAllWindows()