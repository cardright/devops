import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))
from imagemanager import ImageManager


class TestImageManager(unittest.TestCase):

    def test_create(self):
        im = ImageManager()
        im.download("matrix")
        self.assertTrue(im)


if __name__ == '__main__':
    unittest.main()
