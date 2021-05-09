from PeopleTrack import *
from PeopleDetection import *


class PeopleCounterLib:
    def __init__(self):

        #private
        self.__detector = PeopleDetection()
        self.__tracker = PeopleTrack(51, 30, 5)
        self.__last_report = 0

    def compute(self, path_video: str, showvideo: bool = False):

        cap = cv2.VideoCapture(path_video)
        cap.set(cv2.CAP_PROP_FPS, 0.5)
        fps = cap.get(cv2.CAP_PROP_FPS)

        if not cap.isOpened():
            print("Error al abrir el video")

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            # 1. Extract Region of interest
            roi = frame[90:200, 0:375]
            rects = self.__detector.detect(roi)
            centers = self.__detector.computeCenters(rects)

            # 2. Object Tracking
            self.__tracker.update(centers)

            if showvideo:
                self.__tracker.drawTracks(roi)
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(30)
                if key == 27:
                    continue

        cap.release()
        cv2.destroyAllWindows()

        self.__last_report = self.__tracker.reportMainPoints(rtype='best', fps=fps)

    def lastReport(self):
        return self.__last_report


