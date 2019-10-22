import math

from src.data_processing.orientation.quaternion import Quaternion


class Orientation:

    def __init__(self, roll: float = 0, pitch: float = 0, yaw: float = 0):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def to_quaternion(self):
        return Quaternion.euler_degrees_to_quaternion(self.yaw, self.pitch, self.roll)

    def to_axis_angles(self):
        """
        :return: A tuple as (angle, x, y, z). The angle is in degrees.
        """
        c1 = math.cos(self.yaw * 0.5)
        c2 = math.cos(self.roll * 0.5)
        c3 = math.cos(self.pitch * 0.5)
        s1 = math.sin(self.yaw * 0.5)
        s2 = math.sin(self.roll * 0.5)
        s3 = math.sin(self.pitch * 0.5)

        angle = math.degrees(2 * math.acos(c1 * c2 * c3 - s1 * s2 * s3))
        x = s1 * s2 * c3 + c1 * c2 * s3
        y = s1 * c2 * c3 + c1 * s2 * s3
        z = c1 * s2 * c3 - s1 * c2 * s3

        return angle, x, y, z

    def __eq__(self, other):
        if not isinstance(other, Orientation):
            return False

        return self.roll == other.roll and self.pitch == other.pitch and self.yaw == other.yaw

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.roll, self.pitch, self.yaw))
