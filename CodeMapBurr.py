import cv2
import csv

#Path to video file
win = "C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4"
mac = "/Users/Cesar/PyCode_MacOSv1/GP010016_fast.mp4"
mac2 = '/Users/Cesar/PyCode_MacOSv1/VIRB0006.MP4'

#Create file where burrows coordinates will be saved
resultFile = open("burrows.csv", "w", newline='\n')
wr = csv.writer(resultFile, delimiter=",")
wr.writerow(['Coord x','Coord y', 'Frame click'])

#Initialize list of clicks coordinates, burrows counter, position burrow, and position mouse
burrows = []
Counter_burrow = 0
position = (0,0)
posmouse = (0,0)

#Define mouse click function
def click(event, x, y, flags, param):
    global burrows, position, posmouse, resultFile

    if event == cv2.EVENT_LBUTTONDOWN:
        position = (x, y)
        burrows.append(position)
        info = x, y, vid.get(1)
        wr.writerow(info)
        # wr.writerow([position, vid.get(1)])
        resultFile.flush()
        print(burrows)

    if event == cv2.EVENT_MOUSEMOVE:
        posmouse = (x, y)

#Initialize capture of video
vid = cv2.VideoCapture(mac)
fps = vid.get(5)
print(fps)

vid.set(6, 60)
print(vid.get(5))

# while (cap.get(1) < cap.get(7)):
while(vid.isOpened()):

    ret, frame = vid.read()

    if ret == True:
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', click)

        for i, val in enumerate(burrows):
            cv2.circle(frame, val, 3, (0, 255, 0), 2)
            Counter_burrow = i + 1

        cv2.putText(frame, "Number of burrows detected {}".format(Counter_burrow), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, "Last burrow coordinate {}".format(position), (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 255, 255), 2)
        cv2.putText(frame, "Mouse position {}".format(posmouse), (50, 710), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


        # cv2.imshow('frame', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("Q - key pressed. Window quit by user")
            break
    else:
        break

# Close all open windows
vid.release()
cv2.destroyAllWindows()
# Close CSV file
resultFile.close()
