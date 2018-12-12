import unittest
from src.apogee_calculator import ApogeeCalculator


class TestApogee(unittest.TestCase):

    def setUp(self):
        self.apogee_calculator = ApogeeCalculator()

    def test_update(self):
        points = [0, 100, 194, 256, 500, 804, 300]
        self.apogee_calculator.update(points)
        self.assertEqual(self.apogee_calculator.apogee, 804)

        points = [0, 100, 194, 256, 500, 804, 300, 1000, 600, 9]
        self.apogee_calculator.update(points)
        self.assertEqual(self.apogee_calculator.apogee, 1000) # PB

        points = [0, 100, 194]
        self.apogee_calculator.update(points)
        self.assertEqual(self.apogee_calculator.apogee, 0)

    def test_has_apogee(self):
        points = [0, 100, 200, 20]
        self.apogee_calculator.update(points)
        self.assertEqual(self.apogee_calculator.has_apogee(), True)

        points = [2]
        self.apogee_calculator.update(points)
        self.assertEqual(self.apogee_calculator.has_apogee(), False)

        points = [0, 100, 200, 20, 1000, 2000, 100000, 5]
        self.apogee_calculator.update(points)
        self.assertEqual(self.apogee_calculator.has_apogee(), True)

        points = [0, 100, 200, 20, 1000, 2000, 100000, 5]
        self.apogee_calculator.update(points)
        self.assertEqual(self.apogee_calculator.has_apogee(), True)

    def test_empty_apogee(self):
        points = []
        self.apogee_calculator.update(points)
        self.assertEqual(self.apogee_calculator.has_apogee(), False)

    def test_loop(self):
        points = []
        points_fill = [0, 100, 5000, 10000, 9000, 5000, 40]

        for i in range(len(points_fill)):
            points.append(points_fill[i])
            self.apogee_calculator.update(points)

        self.assertEqual(self.apogee_calculator.apogee, 10000)
