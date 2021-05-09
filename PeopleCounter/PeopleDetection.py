import numpy as np
import cv2
import os

class PeopleDetection():
    def __init__(self, history = 500, varThreshold = 4):


        #private
        self.__kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        self.__object_detector = cv2.createBackgroundSubtractorMOG2(history=history, varThreshold=varThreshold)

    def detect(self, frame, area_min = 150):
        '''This function retrieve the rects of the detections obtained'''

        mask = self.__object_detector.apply(frame)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.__kernel)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = []
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > area_min:
                x, y, w, h = cv2.boundingRect(cnt)
                rects.append([x, y, w, h])

        return np.array(rects)

    def computeCenters(self, rects):
        '''This function takes a rects nparray and return an ndarray of the centers'''
        centers = []
        for x, y, w, h in rects:
            centers.append([(2 * x + w) / 2, (2 * y + h) / 2])

        return np.array(centers)
