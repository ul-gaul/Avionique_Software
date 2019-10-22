from src.data_processing.orientation.orientation import Orientation
from src.data_processing.orientation.orientation_initializer import OrientationInitializer, \
    OrientationInitializerListener

from src.data_processing.orientation.angular_speed_integrator import AngularSpeedIntegrator
from src.rocket_packet.rocket_packet import RocketPacket


class OrientationProcessor(OrientationInitializerListener):
    def __init__(self, orientation_initializer: OrientationInitializer,
                 angular_speed_integrator: AngularSpeedIntegrator):
        self._orientation_initializer = orientation_initializer
        self._orientation_initializer.register_listener(self)
        self._angular_speed_integrator = angular_speed_integrator
        self._initialising = True

    def update(self, rocket_packet: RocketPacket):
        if self._initialising:
            self._orientation_initializer.update(rocket_packet)
        else:
            self._angular_speed_integrator.integrate(rocket_packet.time_stamp, rocket_packet.angular_speed_x,
                                                     rocket_packet.angular_speed_y, rocket_packet.angular_speed_z)

    def notify_orientation_initialized(self, timestamp: float, orientation: Orientation):
        self._angular_speed_integrator.set_initial_orientation(timestamp, orientation)
        self._initialising = False

    def get_rocket_orientation(self) -> Orientation:
        return self._angular_speed_integrator.get_current_rocket_orientation()

    def reset(self):
        self._initialising = True
        self._angular_speed_integrator.reset()
        self._orientation_initializer.reset()
