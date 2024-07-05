import unittest
from app.util.initialize_check import is_connected

class TestInternetCheck(unittest.TestCase):

    def test_is_connected(self):
        result = is_connected()
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()