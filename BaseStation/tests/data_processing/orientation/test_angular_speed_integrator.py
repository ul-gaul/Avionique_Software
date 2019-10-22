from unittest import TestCase

from src.data_processing.orientation.angular_speed_integrator import AngularSpeedIntegrator
from src.data_processing.orientation.orientation import Orientation


class AngularSpeedIntegratorTest(TestCase):

    def setUp(self):
        self.integrator = AngularSpeedIntegrator()

    def test_integrate_with_frequency_1(self):
        for i in range(11):
            self.integrator.integrate(i, i, i, i)

        self.assertEqual(self.integrator.get_current_rocket_orientation(), Orientation(50.0, 50.0, 50.0))

    def test_integrate_with_frequency_2(self):
        for i in range(11):
            self.integrator.integrate(i/2, i, i, i)

        self.assertEqual(self.integrator.get_current_rocket_orientation(), Orientation(25.0, 25.0, 25.0))

    def test_integrate_with_initial_orientation(self):
        self.integrator.set_initial_orientation(5, Orientation(5, 10, 15))
        for i in range(11):
            self.integrator.integrate(i + 5, i, i, i)

        self.assertEqual(self.integrator.get_current_rocket_orientation(), Orientation(55.0, 60.0, 65.0))

    def reset_should_reset_current_orientation(self):
        self.integrator.set_initial_orientation(5, Orientation(5, 10, 15))
        self.integrator.integrate(6, 1, 1, 1)

        self.integrator.reset()

        self.assertEqual(self.integrator.get_current_rocket_orientation(), Orientation(0.0, 0.0, 0.0))
