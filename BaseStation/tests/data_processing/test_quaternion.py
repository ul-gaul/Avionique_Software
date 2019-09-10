import unittest
from src.data_processing.quaternion import Quaternion


class QuaternionTest(unittest.TestCase):

    def setUp(self):
        self.quaternion = Quaternion()

    def test_set_new_values(self):
        self.quaternion.set(1, 2, 3, 4)

        self.assertEqual(Quaternion(1, 2, 3, 4), self.quaternion)

    def test_radians_to_quaternion(self):
        quaternion = Quaternion.euler_radians_to_quaternion(0, 0, 3.14/2)
        quaternion.set(round(quaternion.w, 3), round(quaternion.x, 3), round(quaternion.y, 3), round(quaternion.z, 3))

        result = Quaternion(0.707, 0.707, 0, 0)

        self.assertEqual(quaternion, result, "actual: {} | excepted: {}".format(str(quaternion), str(result)))

    def test_degrees_to_quaternion(self):
        quaternion = Quaternion.euler_degrees_to_quaternion(0, 0, 90)
        quaternion.set(round(quaternion.w, 3), round(quaternion.x, 3), round(quaternion.y, 3), round(quaternion.z, 3))

        result = Quaternion(0.707, 0.707, 0, 0)

        self.assertEqual(quaternion, result, "actual: {} | excepted: {}".format(str(quaternion), str(result)))
