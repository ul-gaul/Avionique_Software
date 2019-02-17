import unittest
from src.data_processing.angular_position_calculator import AngularCalculator


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.angular_calculator = AngularCalculator()

    def test_intregrate(self):
        point_x = [0.0, 0.2, 0.4, 0.8, 1.0]
        point_y = [0.5, 0.8, 0.9, 1.0, 1.0]
        total = 0.0

        for i in range(len(point_x)):
            if i < len(point_x)-1:
                total += AngularCalculator.trap_integrate(point_x[i+1], point_y[i+1], point_x[i], point_y[i])

        self.assertEqual(0.88, total)
