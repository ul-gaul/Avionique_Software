import unittest
from src.data_processing.angular_position_calculator import AngularCalculator


class AngularCalculatorTest(unittest.TestCase):

    def setUp(self):
        self.angularCalculator = AngularCalculator()

    def test_integrate_with_frequency_1(self):
        time_stamps = [i for i in range(11)]
        point_x = [i for i in range(11)]
        point_y = [i for i in range(11)]
        point_z = [i for i in range(11)]

        total = self.angularCalculator.integrate_all(time_stamps, point_x, point_y, point_z)

        self.assertEqual(50.0, total[0])

    def test_integrate_with_frequency_2(self):
        time_stamps = [i / 2 for i in range(11)]
        point_x = [i for i in range(11)]
        point_y = [i for i in range(11)]
        point_z = [i for i in range(11)]

        total = self.angularCalculator.integrate_all(time_stamps, point_x, point_y, point_z)

        self.assertEqual(25.0, total[0])
