import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required = True, help = 'path to the video')
ap.add_argument('-s', '--skip_frames', required = True, help = 'number of frames to skip')
args = vars(ap.parse_args())

vid = cv2.VideoCapture(args['video'])

length = int(vid.get(7))
print('Total number of frames = ' + str(length))

def onChange(trackbarValue):
    vid.set(1, trackbarValue)
    ret, frame = vid.read()
    cv2.imshow('Analyse interval', frame)
    pass

cv2.namedWindow('Analyse interval')
cv2.createTrackbar('start', 'Analyse interval', 0, length, onChange )
cv2.createTrackbar('end', 'Analyse interval', 240, length, onChange )

onChange = 0
cv2.waitKey()

start = cv2.getTrackbarPos('start', 'Analyse interval')
end = cv2.getTrackbarPos('end', 'Analyse interval')

if start >= end:
    raise Exception('start must be less than end')

vid.set(1, start)

fgbg = cv2.createBackgroundSubtractorMOG2()

index_first_frame = int(vid.get(1))
counter_unit = 1
counter = []
counter1 = []
print('Analysis started at frame ' + str(index_first_frame))

video1 = cv2.VideoWriter(filename='video1.avi', fourcc=1, frameSize=(960,580), fps=24)

while(vid.isOpened()):
    ret = vid.grab()
    counter.append(counter_unit)

    if ret == True:
        ret, frame = vid.retrieve()

        if len(counter) % int(args['skip_frames']) == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # frame = fgbg.apply(frame)
            frame = cv2.resize(frame, (960,580))
            cv2.imshow('frame', frame)
            video1.write(frame)
            counter1.append(counter_unit)
            # print(vid.get(1))

        if vid.get(1) >= end:
            break

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    else:
        print('Video issues')
        break
print('Total frames in interval = ' + str(len(counter)))
print('Total frames analysed = ' + str(len(counter1)))
vid.release()
video1.release()
cv2.destroyAllWindows()
