import cv2
import math
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True, help='Path to the video file')
# ap.add_argument('-f', '--frame', required=True, type=float,
#                 help='Provide the 0-index based position of frame where the reference is')
ap.add_argument('-l', '--length', type=float, required=True,
                help='length in meters of the reference in the video')
args = vars(ap.parse_args())


print('Loading image, please wait')
vid = cv2.VideoCapture(args['video'])

length = int(vid.get(7))
print('Total number of frames in video = ' + str(length))

print('\n' '(1) Use the bar to navigate frames by click, hold and move bar pointer using the mouse',
      '\n' '(2) Once you select the targeted frame press ESC to initialize measure')

def onChange(trackbarValue):
    vid.set(1, trackbarValue)
    ret, frame = vid.read()
    frame = cv2.resize(frame, (960, 540))
    cv2.imshow('Measure object length', frame)
    pass

coord = []
draw = False

def mouse_line(event, x, y, flags, params):
    global coord, draw

    if event == cv2.EVENT_LBUTTONDOWN:
        coord = [(x, y)]
        cv2.circle(frame, coord[0], 1, (0, 0, 255), 3)
        draw = True
    elif event == cv2.EVENT_LBUTTONUP:
        coord.append((x, y))
        draw = False
        cv2.circle(frame, coord[1], 1, (0, 0, 255), 3)

        cv2.line(frame, coord[0], coord[1], (0, 0, 255), 1)
        cv2.imshow('Measure object length', frame)

# target = args['frame']
# vid.set(1, target)

cv2.namedWindow('Measure object length')
cv2.createTrackbar('Selector', 'Measure object length', 0, length, onChange)

onChange = 0
cv2.waitKey()

frame_selector = cv2.getTrackbarPos('Selector', 'Measure object length')
vid.set(1, frame_selector)

ret, frame = vid.read()
frame = cv2.resize(frame, (960, 540))
reset = frame.copy()

cv2.setMouseCallback('Measure object length', mouse_line)
print('\n' '(3) On the image click and hold mouse left button to set starting point of reference',
      '\n' '(4) Move and release mouse left button to set ending point of reference',
      '\n' '(5) Press key ''r'' to reset selection, or Press key ''s'' to save selection and exit window',
      '\n' '(6) Several lines might be created in the frame, but only the last one will be used',
      '\n' '(7) Press key ESC to exit the window')

while True:
    cv2.imshow('Measure object length', frame)
    key = cv2.waitKey(1) & 0XFF

    if key == ord('r'):
        coord = []
        frame = reset.copy()
    if key == ord('s'):
        dist = math.sqrt((coord[0][0] - coord[1][0]) ** 2 + (coord[0][1] - coord[1][1]) ** 2)
        pixel_to_meters = args['length'] / dist
        width_m = vid.get(3) * pixel_to_meters
        height_m = vid.get(4) * pixel_to_meters
        area = width_m * height_m

        print('\n' 'Results', '\n' 'Line started at', coord[0], '\n' 'Line ended at ', coord[1])
        print('Pixel length of reference = ', dist)
        print('Pixel to meter conversion factor = ', pixel_to_meters)
        print('Width of field of view in meters = ', width_m)
        print('Height of field of view in meters = ', height_m)
        print('Area of field of view in square meters = ', area)

        break
    if key == 27:
        print('\n' 'ESC key pressed. Window quit by user')
        break

cv2.destroyAllWindows()
vid.release()
