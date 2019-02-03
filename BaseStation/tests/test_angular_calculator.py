import unittest
from src.angular_position_calculator import AngularCalculator


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.angular_calculator = AngularCalculator()

    def test_angular_velocity_to_euler(self):
        angular_velocity = (75, 50, 25)
        self.angular_calculator.compute_angular_velocity(angular_velocity)

        computed_angle = self.angular_calculator.get_angles_degrees()
        rounded_angle = round(computed_angle[0], 2), round(computed_angle[1], 2), round(computed_angle[2], 2)

        self.assertEqual(rounded_angle, (93.54, 74.5, 33.69))

    def test_euler_radians_to_quaternion(self):
        self.angular_calculator.euler_radians_to_quaternion(0, 0, 3.14/2)
        computed_quaternion = self.angular_calculator.get_quaternions()
        rounded_quaternion = round(computed_quaternion[0], 3), round(computed_quaternion[1], 3), round(computed_quaternion[2], 3), round(computed_quaternion[3], 3)

        self.assertEqual(rounded_quaternion, (0.707, 0.0, 0.0, 0.707))

    def test_euler_degrees_to_quaternion(self):
        self.angular_calculator.euler_degrees_to_quaternion(0, 0, 90)
        computed_quaternion = self.angular_calculator.get_quaternions()
        rounded_quaternion = round(computed_quaternion[0], 3), round(computed_quaternion[1], 3), round(computed_quaternion[2], 3), round(computed_quaternion[3], 3)

        self.assertEqual(rounded_quaternion, (0.707, 0.0, 0.0, 0.707))

    def test_full_class_euler_radians_to_quaternion(self):
        angular_velocity = (75, 50, 25)
        self.angular_calculator.compute_angular_velocity(angular_velocity)

        computed_quaternion = self.angular_calculator.get_quaternions()
        rounded_quaternion = round(computed_quaternion[0], 3), round(computed_quaternion[1], 3), round(computed_quaternion[2], 3), round(computed_quaternion[3], 3)

        self.assertEqual((0.435, 0.565, -0.264, 0.65), rounded_quaternion)
