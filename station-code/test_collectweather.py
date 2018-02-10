import unittest
from collectweather import StationConfig

"""
Test Module
example of multiline docstring
"""


class SimplisticTest(unittest.TestCase):
    def setUp(self):
        self.func = StationConfig()
    """Simple Tests"""
    def test(self):
        self.assertTrue(True)

    def test_returnsdict(self):
        self.assertIsNotNone(self.func.configs)


if __name__ == '__main__':
    unittest.main()
