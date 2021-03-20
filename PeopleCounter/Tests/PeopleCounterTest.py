import unittest
import cv2
import numpy as np
from PeopleDetection import PeopleDetection
from PeopleTrack import PeopleTrack

class PeopleCounterTest(unittest.TestCase):
    def test_PeopleDetection(self):
        video = cv2.VideoCapture("OneStopNoEnter1front.mpg")
        detector = PeopleDetection()
        result=detector.detection(video)
        self.assertTrue((result == np.array([[13,0,1],[24,2,3],[26,0,1]])).all())

    def test_PeopleTrack(self):
        video = cv2.VideoCapture("OneStopNoEnter1front.mpg")
        tracker = PeopleTrack()
        result=tracker.tracking(video)
        self.assertTrue((result == np.array([[13,0,1,24,2,3,16,18],[26,0,1,-1,-1,-1, -1, -1]])).all())

if __name__ == '__main__':
    unittest.main()
