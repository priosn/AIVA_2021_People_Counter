import unittest
from PeopleCounterLib import *

class PeopleCounterTest(unittest.TestCase):

    def test_PeopleCounterLib(self):
        path_video = "../dataset/OneStopNoEnter1front.mpg"
        counter = PeopleCounterLib()
        counter.compute(path_video=path_video, showvideo=False)
        results = counter.lastReport()
        result = results[0]
        ground_truth = np.array([13, 0, 1, 24, 2, 3, 14, 21])
        comp = []
        comp.append(abs(result[1] - ground_truth[0]) < 2)
        comp.append((result[2:4] == ground_truth[1:3]).all())
        comp.append(abs(result[4] - ground_truth[3]) < 2)
        comp.append((result[5:7] == ground_truth[4:6]).all())
        comp.append(abs(result[7] - ground_truth[6]) < 2)
        comp.append(abs(result[8] - ground_truth[7]) < 2)
        self.assertTrue(sum(comp))

if __name__ == '__main__':
    unittest.main()