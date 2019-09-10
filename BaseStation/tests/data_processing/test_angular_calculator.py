import unittest
from src.data_processing.angular_position_calculator import AngularCalculator


class AngularCalculatorTest(unittest.TestCase):

    def setUp(self):
        self.angularCalculator = AngularCalculator(1)
        self.point_x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.point_y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.point_z = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_integrate_with_frequency_1(self):
        total = self.angularCalculator.integrate_all(self.point_x, self.point_y, self.point_z)

        self.assertEqual(50.0, total[0])

    def test_integrate_with_frequency_2(self):
        self.angularCalculator.sample_frequency = 2

        total = self.angularCalculator.integrate_all(self.point_x, self.point_y, self.point_z)

        self.assertEqual(25.0, total[0])
