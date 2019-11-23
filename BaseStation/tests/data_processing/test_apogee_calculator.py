import unittest

from src.data_processing.apogee import Apogee
from src.data_processing.apogee_calculator import ApogeeCalculator


class ApogeeCalculatorTest(unittest.TestCase):

    def setUp(self):
        self.apogee_calculator = ApogeeCalculator()

    def test_update_one_apogee(self):
        points = [0, 100, 194, 256, 500, 804, 300]
        timestamps = self._generate_timestamps_for(points)

        self.apogee_calculator.update(timestamps, points)

        self.assertEqual(self.apogee_calculator.get_apogee(), Apogee(5, 804))

    def test_update_distinguish_real_apogee(self):
        points = [0, 100, 194, 256, 500, 804, 300, 1000, 600, 9]
        timestamps = self._generate_timestamps_for(points)

        self.apogee_calculator.update(timestamps, points)

        self.assertEqual(self.apogee_calculator.get_apogee(), Apogee(7, 1000))

    def test_update_no_apogee(self):
        points = [0, 100, 194]
        timestamps = self._generate_timestamps_for(points)

        self.apogee_calculator.update(timestamps, points)

        self.assertEqual(self.apogee_calculator.get_apogee(), Apogee.unreached())

    def test_has_apogee_fail_with_one_point(self):
        points = [2]
        timestamps = self._generate_timestamps_for(points)

        self.apogee_calculator.update(timestamps, points)

        self.assertEqual(self.apogee_calculator.get_apogee(), Apogee.unreached())

    def test_empty_apogee(self):
        points = []
        timestamps = self._generate_timestamps_for(points)

        self.apogee_calculator.update(timestamps, points)

        self.assertEqual(self.apogee_calculator.get_apogee(), Apogee.unreached())

    def test_loop_integration(self):
        timestamps = []
        points = []
        points_fill = [0, 100, 5000, 10000, 9000, 5000, 40]

        for i in range(len(points_fill)):
            timestamps.append(i)
            points.append(points_fill[i])

            self.apogee_calculator.update(timestamps, points)

        self.assertEqual(self.apogee_calculator.get_apogee(), Apogee(3, 10000))

    @staticmethod
    def _generate_timestamps_for(points):
        return [i for i in range(len(points))]
