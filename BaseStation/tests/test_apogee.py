import unittest
from src.ui.altitude_graph import ApogeeCalculator


class TestApogee(unittest.TestCase):

    def setUp(self):
        self.apogee_calculator = ApogeeCalculator()
        self.points = [0, 100, 194, 256, 500, 804]

    def test_init(self):
        with self.assertRaises(ValueError):
            self.apogee_calculator.init([])

        self.assertTrue(self.apogee_calculator.init(self.points))

    def test_getApogee(self):
        self.apogee_calculator.init(self.points)
        self.assertEqual(self.apogee_calculator.get_apogee(5), 500)
