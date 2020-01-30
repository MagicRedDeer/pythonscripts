import unittest
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.info('setUpClass')

    def setUp(self):
        logging.info('setUp')

    def test_first(self):
        logging.info('test_first')

    def test_second(self):
        logging.info('test_second')

    def tearDown(self):
        logging.info('tearDown')

    @classmethod
    def tearDownClass(cls):
        logging.info('tearDownClass')

if __name__ == "__main__":
    unittest.main()


