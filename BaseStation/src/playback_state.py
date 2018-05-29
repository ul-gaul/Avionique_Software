from enum import Enum


class PlaybackState:
    class Mode(Enum):
        MOVE_FORWARD = 1
        MOVE_BACKWARD = 2
    min_speed_factor = 1.0
    max_speed_factor = 16.0

    def __init__(self, speed_factor, mode: Mode):
        self.mode = mode
        self.speed_factor = min(max(speed_factor, self.min_speed_factor), self.max_speed_factor)

    def get_speed(self):
        return self.speed_factor

    def get_mode(self):
        return self.mode

    def speed_up(self):
        self.speed_factor = min(self.speed_factor * 2, self.max_speed_factor)

    def speed_down(self):
        self.speed_factor = max(self.speed_factor / 2, self.min_speed_factor)

    def set_mode_forward(self):
        self.mode = self.Mode.MOVE_FORWARD

    def set_mode_backward(self):
        self.mode = self.Mode.MOVE_BACKWARD

    def is_neutral(self):
        return self.speed_factor == 1.0

    def is_going_forward(self):
        return self.mode == self.Mode.MOVE_FORWARD

    def is_going_backward(self):
        return self.mode == self.Mode.MOVE_BACKWARD
