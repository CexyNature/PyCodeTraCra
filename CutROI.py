import cv2
import argparse
import os
import time

#Create list container for ROI coordinates
coordROI = []
#Create boolean for cropping action
crop = False

#Define function to create ROI bounding box from mouse event
def selectcrop(event, x, y, flags, param):
    global coordROI, crop

    #When left buttom is clicked record coordinates and change boolean flag
    if event == cv2.EVENT_LBUTTONDOWN:
        coordROI = [(x,y)]
        crop = True

    #When left buttom is released record coordinates and change boolean flag
    elif event == cv2.EVENT_LBUTTONUP:
        coordROI.append((x,y))
        crop = False

        cv2.rectangle(frame, coordROI[0], coordROI[1], (0,250,255), 1)
        cv2.imshow('frame', frame)

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = 'Provide path to image')
ap.add_argument('-f', '--folder', required = True, help = 'Provide path to folder where files will be saved')
args = vars(ap.parse_args())

frame = cv2.imread(args['image'])
duplicate = frame.copy()
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', selectcrop)

while True:
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF

    #Press r to reset cropping ROI
    if key == ord('r'):
        coordROI = []
        frame = duplicate.copy()

    #Press c to crop selection
    elif key == ord('c'):
        if len(coordROI) == 2:
            ROIimg = duplicate[coordROI[0][1]:coordROI[1][1], coordROI[0][0]:coordROI[1][0]]
            cv2.imshow('Selection', ROIimg)
            base_filename = time.strftime('%Y%m%d-%H%M%S')
            dirFolder = os.path.join(args['folder'], base_filename + '.' + 'jpg')
            print(base_filename)
            cv2.imwrite(dirFolder, ROIimg)

    elif key == 27:
        break

cv2.destroyAllWindows()