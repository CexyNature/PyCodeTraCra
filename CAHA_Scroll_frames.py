import cv2
import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True, help='Path to the video file')
ap.add_argument('-l', '--length', type=float, required=True,
                help='length in meters of the reference in the video')
args = vars(ap.parse_args())


print('Loading image, please wait')
vid = cv2.VideoCapture(args['video'])

length_vid = int(vid.get(7))
print('Total number of frames in video = ' + str(length_vid))

print('(1) Use the bar to scroll frames by click, hold and move bar pointer using the mouse',
      '\n' '(2) On the image, click and hold mouse left button to set starting point of reference',
      '\n' '(3) Move and release mouse left button to set ending point of reference',
      '\n' '(4) A line showing your selection will appear in the image',
      '\n' '(5) Several lines might be created in a frame, but only the last one will be used',
      '\n' '(6) Press key ''s'' to save selection, and exit the window',
      '\n' '(7) Press key ESC to exit the window',
      '\n' '(8) Change frame will reset selection', )

coord = []
draw = False

def onChange(trackbarValue):

    vid.set(1, trackbarValue)
    ret, frame = vid.read()
    frame = cv2.resize(frame, (960, 540))
    cv2.imshow('Measure object length', frame)
    pass

    ret, frame = vid.read()
    frame = cv2.resize(frame, (960, 540))

    def mouse_line(event, x, y, flags, params):
        global coord, draw
        if event == cv2.EVENT_LBUTTONDOWN:
            coord = [(x, y)]
            cv2.circle(frame, coord[0], 1, (0, 0, 255), 2)
            draw = True
            cv2.imshow('Measure object length', frame)
        elif event == cv2.EVENT_LBUTTONUP:
            coord.append((x, y))
            draw = False
            cv2.circle(frame, coord[1], 1, (0, 0, 255), 2)

            cv2.line(frame, coord[0], coord[1], (0, 0, 255), 1)
            cv2.imshow('Measure object length', frame)


    cv2.setMouseCallback('Measure object length', mouse_line)

cv2.namedWindow('Measure object length')
cv2.createTrackbar('Selector', 'Measure object length', 0, length_vid, onChange)

while True:
    onChange = 0

    key = cv2.waitKey(0) & 0xFF

    if key == ord('s'):
        dist = math.sqrt((coord[0][0] - coord[1][0]) ** 2 + (coord[0][1] - coord[1][1]) ** 2)
        pixel_to_meters = args['length'] / dist
        width_m = vid.get(3) * pixel_to_meters
        height_m = vid.get(4) * pixel_to_meters
        area = width_m * height_m

        print('Line started at', coord[0], '\n' 'Line ended at ', coord[1])
        print('Pixel length of reference = ', dist)
        print('Pixel to meter conversion factor = ', pixel_to_meters)
        print('Width of field of view in meters = ', width_m)
        print('Height of field of view in meters = ', height_m)
        print('Area of field of view in square meters = ', area)
        break

    if key == 27:
        break

print('Your last selection has the next coordinates: ', coord)
print('Your last selection was taken in frame ', vid.get(1)-2)

