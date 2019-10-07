import unittest

from src.data_processing.orientation.quaternion import Quaternion


class QuaternionTest(unittest.TestCase):

    def setUp(self):
        self.quaternion = Quaternion()

    def test_radians_to_quaternion(self):
        computed_quaternion = Quaternion.euler_radians_to_quaternion(0, 0, 3.14/2)
        computed_quaternion = Quaternion(round(computed_quaternion.w, 3), round(computed_quaternion.x, 3),
                                         round(computed_quaternion.y, 3), round(computed_quaternion.z, 3))

        result = Quaternion(0.707, 0.707, 0, 0)

        self.assertEqual(computed_quaternion, result, "actual: {} | excepted: {}".format(str(computed_quaternion),
                                                                                         str(result)))

    def test_degrees_to_quaternion(self):
        computed_quaternion = Quaternion.euler_degrees_to_quaternion(0, 0, 90)
        computed_quaternion = Quaternion(round(computed_quaternion.w, 3), round(computed_quaternion.x, 3),
                                         round(computed_quaternion.y, 3), round(computed_quaternion.z, 3))

        result = Quaternion(0.707, 0.707, 0, 0)

        self.assertEqual(computed_quaternion, result, "actual: {} | excepted: {}".format(str(computed_quaternion),
                                                                                         str(result)))
