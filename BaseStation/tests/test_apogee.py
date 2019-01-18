import unittest
from src.apogee_calculator import ApogeeCalculator


class TestApogee(unittest.TestCase):

    def setUp(self):
        self.apogee_calculator = ApogeeCalculator()

    def test_update_one_apogee(self):
        points = [0, 100, 194, 256, 500, 804, 300]
        self.apogee_calculator.update(points)

        self.assertEqual(self.apogee_calculator.get_apogee(), (5, 804))

    def test_update_distinguish_real_apogee(self):
        points = [0, 100, 194, 256, 500, 804, 300, 1000, 600, 9]
        self.apogee_calculator.update(points)

        self.assertEqual(self.apogee_calculator.get_apogee(), (7, 1000))

    def test_update_no_apogee(self):
        points = [0, 100, 194]
        self.apogee_calculator.update(points)

        self.assertIsNone(self.apogee_calculator.get_apogee())

    def test_has_apogee_fail_with_one_point(self):
        points = [2]
        self.apogee_calculator.update(points)
        self.assertIsNone(self.apogee_calculator.get_apogee())

    def test_empty_apogee(self):
        points = []
        self.apogee_calculator.update(points)
        self.assertIsNone(self.apogee_calculator.get_apogee())

    def test_loop_integration(self):
        points = []
        points_fill = [0, 100, 5000, 10000, 9000, 5000, 40]

        for i in range(len(points_fill)):
            points.append(points_fill[i])
            self.apogee_calculator.update(points)

        self.assertEqual(self.apogee_calculator.get_apogee(), (3, 10000))
