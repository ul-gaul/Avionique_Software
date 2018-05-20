class TimeTravel:
    MOVE_FORWARD = 'forward'
    MOVE_BACKWARD = 'backward'
    speed_factor = 1.0
    mode = MOVE_FORWARD
    max_speed_factor = 16.0

    def get_speed(self):
        return self.speed_factor

    def speed_up(self):
        if self.speed_factor < self.max_speed_factor:
            self.speed_factor = self.speed_factor * 2
        else:
            self.speed_factor = self.max_speed_factor

    def speed_down(self):
        if self.speed_factor > 1.0:
            self.speed_factor = self.speed_factor / 2
        else:
            self.speed_factor = 1.0

    def set_mode_forward(self):
        self.mode = self.MOVE_FORWARD

    def set_mode_backward(self):
        self.mode = self.MOVE_BACKWARD

    def is_neutral(self):
        return self.speed_factor == 1.0

    def is_going_forward(self):
        return self.mode == self.MOVE_FORWARD

    def is_going_backward(self):
        return self.mode == self.MOVE_BACKWARD
