import cv2
from threading import Thread
from queue import Queue

win = "C:/Users/jc306494/Documents/PythonAnalysis/SampleVid/GP010016_fast.mp4"
mac = "/Users/Cesar/PyCode_MacOSv1/GP010016_fast.mp4"
win2 = 'C:/Users/jc306494/Documents/2CAHA_JCU PhD/1CAHA_Data/Crabs/13JUL2017/DCIM/100_VIRB/VIRB0006.MP4'
mac2 = '/Users/Cesar/PyCode_MacOSv1/VIRB0006.MP4'

class FileVideoStream:
    def __init__(self, path, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(win2)
        self.stopped = False

        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop()
                    return

                # add the frame to the queue
                self.Q.put(frame)

    def read(self):
        # return next frame in the queue
        return self.Q.get()

    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

