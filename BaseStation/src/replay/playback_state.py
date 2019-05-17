from enum import Enum


class PlaybackState:
    class Mode(Enum):
        FORWARD = 1
        BACKWARD = 2

    min_speed_factor = 1.0
    max_speed_factor = 16.0

    def __init__(self, speed_factor: float = 1, mode: Mode = Mode.FORWARD):
        self.mode = mode
        self.speed_factor = min(max(speed_factor, self.min_speed_factor), self.max_speed_factor)

    def get_speed(self):
        return self.speed_factor

    def get_mode(self):
        return self.mode

    def fast_forward(self):
        if self.is_going_forward():
            self._speed_up()
        elif self.is_normal_speed():
            self._set_mode_forward()
        else:
            self._speed_down()

    def rewind(self):
        if self.is_going_backward():
            self._speed_up()
        elif self.is_normal_speed():
            self._set_mode_backward()
        else:
            self._speed_down()

    def _speed_up(self):
        self.speed_factor = min(self.speed_factor * 2, self.max_speed_factor)

    def _speed_down(self):
        self.speed_factor = max(self.speed_factor / 2, self.min_speed_factor)

    def _set_mode_forward(self):
        self.mode = self.Mode.FORWARD

    def _set_mode_backward(self):
        self.mode = self.Mode.BACKWARD

    def is_normal_speed(self):
        return self.speed_factor == self.min_speed_factor

    def is_going_forward(self):
        return self.mode == self.Mode.FORWARD

    def is_going_backward(self):
        return self.mode == self.Mode.BACKWARD

    def reset(self):
        self.mode = self.Mode.FORWARD
        self.speed_factor = 1.0
