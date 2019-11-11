import unittest

from src.data_processing.apogee import Apogee


class ApogeeTest(unittest.TestCase):
    TIMESTAMP = 60.0
    ALTITUDE = 10000.0

    def test_apogee_is_reached_when_created_from_constructor(self):
        apogee = Apogee(self.TIMESTAMP, self.ALTITUDE)

        self.assertTrue(apogee.is_reached)

    def test_apogee_is_not_reached_when_created_from_unreached_method(self):
        apogee = Apogee.unreached()

        self.assertFalse(apogee.is_reached)
