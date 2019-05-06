import unittest

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import config


class VideoIdListTestCase(unittest.TestCase):
    def test_no_duplicate(self):
        video_id_set = set(config.VIDEO_ID_LIST)
        self.assertEqual(len(video_id_set), len(config.VIDEO_ID_LIST))


if __name__ == "__main__":
    unittest.main()
