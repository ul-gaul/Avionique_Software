import unittest
from src.angular_position_calculator import AngularCalculator


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.angular_calculator = AngularCalculator()

    def test_angular_velocity_to_euler(self):
        angular_velocity = (75, 50, 25)
        self.angular_calculator.compute_angular_velocity(angular_velocity)

        computed_angle = self.angular_calculator.get_angles()
        rounded_angle = round(computed_angle[0], 2), round(computed_angle[1], 2), round(computed_angle[2], 2)

        self.assertEqual(rounded_angle, (93.54, 74.5, 33.69))

    def test_euler_to_quaternion(self):
        angular_velocity = (75, 50, 25)
        self.angular_calculator.compute_angular_velocity(angular_velocity)

        computed_quaternion = self.angular_calculator.get_quaternions()
        rounded_quaternion = round(computed_quaternion[0], 3), round(computed_quaternion[1], 3), round(computed_quaternion[2], 3), round(computed_quaternion[3], 3)

        self.assertEqual(rounded_quaternion, (0.646, 0.611, 0.208, 0.407))

