import numpy as np
from KalmanFilter import KalmanFilter
from scipy.optimize import linear_sum_assignment
from collections import deque
import cv2

class Tracks(object):
	"""docstring for Tracks"""
	def __init__(self, detection, trackId):
		super(Tracks, self).__init__()
		self.KF = KalmanFilter()
		self.KF.predict()
		self.KF.correct(np.matrix(detection).reshape(2,1))
		self.trace = deque(maxlen=500)
		self.nframe = deque(maxlen=500)
		self.prediction = detection.reshape(1,2)
		self.trackId = trackId
		self.skipped_frames = 0

	def predict(self,detection):
		self.prediction = np.array(self.KF.predict()).reshape(1,2)
		self.KF.correct(np.matrix(detection).reshape(2,1))

	def genMainPoints(self, fps = 25):

		main_points = np.ones(9)*-1
		main_points[0] = self.trackId
		if len(self.trace) == 0:
			return main_points
		main_points[1] = self.nframe[0]/fps
		if (40 > self.trace[0][0,0]) and (20 < self.trace[0][0,1]):
			main_points[2] = 0
			main_points[3] = 1
			for i in range(len(self.nframe)):
				if self.trace[i][0,0] > 40:
					main_points[7] = self.nframe[i]/fps
					break
			for i in range(len(self.nframe)):
				if self.trace[i][0, 0] > 200:
					main_points[8] = self.nframe[i]/fps
					break
		elif (340 < self.trace[0][0,0]) and (20 < self.trace[0][0,1]):
			main_points[2] = 3
			main_points[3] = 2
			for i in range(len(self.nframe)):
				if self.trace[i][0, 0] < 200:
					main_points[7] = self.nframe[i]/fps
					break
			for i in range(len(self.nframe)):
				if self.trace[i][0, 0] < 40:
					main_points[8] = self.nframe[i]/fps
					break
		elif (340 > self.trace[0][0,0] > 200) and (20 > self.trace[0][0,1]):
			main_points[2] = 5
			main_points[3] = 4
			for i in range(len(self.nframe)):
				if self.trace[i][0, 0] < 200:
					main_points[7] = self.nframe[i]/fps
					break
			for i in range(len(self.nframe)):
				if self.trace[i][0, 0] < 40:
					main_points[8] = self.nframe[i]/fps
					break
		main_points[4] = self.nframe[-1]/fps
		if (40 > self.trace[-1][0,0]) and (20 < self.trace[-1][0,1]):
			main_points[5] = 1
			main_points[6] = 0
		elif (340 < self.trace[-1][0,0]) and (20 < self.trace[-1][0,1]):
			main_points[5] = 2
			main_points[6] = 3
		elif (340 > self.trace[-1][0,0] > 200) and (20 > self.trace[-1][0,1]):
			main_points[5] = 4
			main_points[6] = 5

		return main_points




class PeopleTrack(object):
	"""docstring for Tracker"""
	def __init__(self, dist_threshold, max_frame_skipped, max_trace_length):
		super(PeopleTrack, self).__init__()
		self.dist_threshold = dist_threshold
		self.max_frame_skipped = max_frame_skipped
		self.max_trace_length = max_trace_length


		#private
		self.__trackId = 0
		self.__tracks = []
		self.__removed_tracks = []
		self.__nframes = -1
		self.__track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
						(127, 127, 255), (255, 0, 255), (255, 127, 255),
						(127, 0, 255), (127, 0, 127),(127, 10, 255), (0,255, 127)]


	def update(self, detections):
		'''This function update the tracker positions and manage them'''

		# Update the current frame
		self.__nframes += 1
		# If no detections are passed, them these statements manage it.
		if detections.size == 0:

			for i in range(len(self.__tracks)):
				self.__tracks[i].skipped_frames +=1

			del_tracks = []
			for i in range(len(self.__tracks)):
				if self.__tracks[i].skipped_frames > self.max_frame_skipped:
					del_tracks.append(i)

			if len(del_tracks) > 0:
				for i in range(len(del_tracks)):
					self.__removed_tracks.append(self.__tracks[del_tracks[i]])
					del self.__tracks[del_tracks[i]]

			return 0


		if len(self.__tracks) == 0:
			for i in range(detections.shape[0]):
				track = Tracks(detections[i], self.__trackId)
				self.__trackId +=1
				self.__tracks.append(track)

		# Calculate the distance between detentions and prediction for each track
		N = len(self.__tracks)
		M = len(detections)
		cost = []
		for i in range(N):
			diff = np.linalg.norm(self.__tracks[i].prediction - detections.reshape(-1,2), axis=1)
			cost.append(diff)

		cost = np.array(cost)*0.1
		row, col = linear_sum_assignment(cost)
		assignment = [-1]*N
		for i in range(len(row)):
			assignment[row[i]] = col[i]

		un_assigned_tracks = []

		# Check if the threshold condition is fulfilled
		for i in range(len(assignment)):
			if assignment[i] != -1:
				if (cost[i][assignment[i]] > self.dist_threshold):
					assignment[i] = -1
					un_assigned_tracks.append(i)
				# else:
				# 	self.tracks[i].skipped_frames += 1
			else:
				self.__tracks[i].skipped_frames +=1

		#Those with no assigments are deleted
		del_tracks = []
		for i in range(len(self.__tracks)):
			if self.__tracks[i].skipped_frames > self.max_frame_skipped :
				del_tracks.append(i)

		if len(del_tracks) > 0:
			for i in range(len(del_tracks)):
				self.__removed_tracks.append(self.__tracks[del_tracks[i]])
				del self.__tracks[del_tracks[i]]
				del assignment[del_tracks[i]]

		for i in range(len(detections)):
			if i not in assignment:
				track = Tracks(detections[i], self.__trackId)
				self.__trackId +=1
				self.__tracks.append(track)


		for i in range(len(assignment)):
			if(assignment[i] != -1):
				self.__tracks[i].skipped_frames = 0
				self.__tracks[i].predict(detections[assignment[i]])
			self.__tracks[i].trace.append(self.__tracks[i].prediction)
			self.__tracks[i].nframe.append(self.__nframes)

	def drawTracks(self, frame):
		'''This function allows you tu paint tracks on the frame'''
		for j in range(len(self.__tracks)):
			if (len(self.__tracks[j].trace) > 1):
				x = int(self.__tracks[j].trace[-1][0, 0])
				y = int(self.__tracks[j].trace[-1][0, 1])
				tl = (x - 10, y - 10)
				br = (x + 10, y + 10)
				cv2.rectangle(frame, tl, br, self.__track_colors[j], 1)
				cv2.putText(frame, str(self.__tracks[j].trackId), (x - 10, y - 20), 0, 0.5, self.__track_colors[j], 2)
				for k in range(len(self.__tracks[j].trace)):
					x = int(self.__tracks[j].trace[k][0, 0])
					y = int(self.__tracks[j].trace[k][0, 1])
					cv2.circle(frame, (x, y), 3, self.__track_colors[j], -1)
				cv2.circle(frame, (x, y), 6, self.__track_colors[j], -1)

		return frame

	def reportMainPoints(self, rtype = 'all', timelapsemin = 5, fps = 25):
		'''Generate a report of the main points concerning to each track
		:param rtype: type of report to be generated. Choose between 'all' or 'best'
		:type rtype: str
		:param timelapsemin: minime time distance between first and last frame
		:type timelapsemin: int
		:param fps: frames per second
		:type fps: int
		'''
		all_tracks = self.__tracks + self.__removed_tracks
		report = []
		for i in range(len(all_tracks)):
			report.append(all_tracks[i].genMainPoints(fps = fps))

		if rtype == 'all':
			return np.array(report)
		if rtype == 'best':
			report_best = []
			for rp in report:
				if (rp[4]-rp[1]) > timelapsemin:
					report_best.append(rp)
			return np.array(report_best)






		



