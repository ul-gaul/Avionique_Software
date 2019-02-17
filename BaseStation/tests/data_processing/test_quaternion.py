import unittest
from src.data_processing.quaternion import Quaternion


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.quaternion = Quaternion()

    def test_radians_to_quaternion(self):
        computed_quaternion = Quaternion.euler_radians_to_quaternion(0, 0, 3.14/2)

        computed_quaternion.x = round(computed_quaternion.x, 3)
        computed_quaternion.y = round(computed_quaternion.y, 3)
        computed_quaternion.z = round(computed_quaternion.z, 3)
        computed_quaternion.w = round(computed_quaternion.w, 3)

        result = Quaternion()
        result.set(0.707, 0, 0, 0.707)
        
        self.assertTrue(computed_quaternion, result)

    def test_degrees_to_quaternion(self):
        computed_quaternion = Quaternion.euler_degrees_to_quaternion(0, 0, 90)
        rounded_quaternion = round(computed_quaternion.x, 3), round(computed_quaternion.y, 3), round(computed_quaternion.z, 3), round(computed_quaternion.w, 3)

        result = Quaternion()
        result.set(0.707, 0, 0, 0.707)

        self.assertTrue(rounded_quaternion, result)
