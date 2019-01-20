import unittest
from src.angular_position_calculator import AngularCalculator


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.angular_calculator = AngularCalculator()

    def test_only_true(self):
        self.assertEqual(True, True)
