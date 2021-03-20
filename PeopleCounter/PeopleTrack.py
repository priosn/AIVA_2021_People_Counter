import numpy as np

class PeopleTrack(object):

    def tracking(self, video):
        """
        :param video: numpy matrix (n,m)
        :return: string with the text recognized in codebar
        """

        return np.array([[13,0,1,24,2,3,16,18],[26,0,1,-1,-1,-1, -1, -1]])