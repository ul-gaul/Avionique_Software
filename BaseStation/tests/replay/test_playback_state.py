import unittest

from src.replay.playback_state import PlaybackState


class PlaybackStateTest(unittest.TestCase):

    def test_fast_forward_should_double_speed_when_fast_forwarding(self):
        initial_speed = 1.0
        playback_state = PlaybackState(initial_speed, PlaybackState.Mode.FORWARD)

        playback_state.fast_forward()

        self.assertEqual(playback_state.get_speed(), initial_speed * 2)
        self.assertEqual(playback_state.get_mode(), PlaybackState.Mode.FORWARD)

    def test_fast_forward_should_set_mode_forward_when_rewinding_at_normal_speed(self):
        initial_speed = 1.0
        playback_state = PlaybackState(initial_speed, PlaybackState.Mode.BACKWARD)

        playback_state.fast_forward()

        self.assertEqual(playback_state.get_speed(), initial_speed)
        self.assertEqual(playback_state.get_mode(), PlaybackState.Mode.FORWARD)

    def test_fast_forward_should_halve_speed_when_fast_rewinding(self):
        initial_speed = 2.0
        playback_state = PlaybackState(initial_speed, PlaybackState.Mode.BACKWARD)

        playback_state.fast_forward()

        self.assertEqual(playback_state.get_speed(), initial_speed / 2)
        self.assertEqual(playback_state.get_mode(), PlaybackState.Mode.BACKWARD)

    def test_fast_forward_should_not_accelerate_beyond_max_speed(self):
        initial_speed = PlaybackState.max_speed_factor
        playback_state = PlaybackState(initial_speed, PlaybackState.Mode.FORWARD)

        playback_state.fast_forward()

        self.assertEqual(playback_state.get_mode(), PlaybackState.Mode.FORWARD)
        self.assertEqual(playback_state.get_speed(), PlaybackState.max_speed_factor)

    def test_rewind_should_double_speed_when_rewinding(self):
        initial_speed = 1.0
        playback_state = PlaybackState(initial_speed, PlaybackState.Mode.BACKWARD)

        playback_state.rewind()

        self.assertEqual(playback_state.get_speed(), initial_speed * 2)
        self.assertEqual(playback_state.get_mode(), PlaybackState.Mode.BACKWARD)

    def test_rewind_should_set_mode_backward_when_fast_forwarding_at_normal_speed(self):
        initial_speed = 1.0
        playback_state = PlaybackState(initial_speed, PlaybackState.Mode.FORWARD)

        playback_state.rewind()

        self.assertEqual(playback_state.get_mode(), PlaybackState.Mode.BACKWARD)
        self.assertEqual(playback_state.get_speed(), initial_speed)

    def test_rewind_should_halve_speed_when_fast_forwarding(self):
        initial_speed = 2.0
        playback_state = PlaybackState(initial_speed, PlaybackState.Mode.FORWARD)

        playback_state.rewind()

        self.assertEqual(playback_state.get_speed(), initial_speed / 2)
        self.assertEqual(playback_state.get_mode(), PlaybackState.Mode.FORWARD)

    def test_rewind_should_not_accelerate_beyond_max_speed(self):
        initial_speed = PlaybackState.max_speed_factor
        playback_state = PlaybackState(initial_speed, PlaybackState.Mode.BACKWARD)

        playback_state.rewind()

        self.assertEqual(playback_state.get_mode(), PlaybackState.Mode.BACKWARD)
        self.assertEqual(playback_state.get_speed(), PlaybackState.max_speed_factor)

    def test_reset_should_set_mode_forward(self):
        playback_state = PlaybackState(mode=PlaybackState.Mode.BACKWARD)

        playback_state.reset()

        self.assertTrue(playback_state.is_going_forward())

    def test_reset_should_set_normal_speed(self):
        playback_state = PlaybackState(speed_factor=PlaybackState.max_speed_factor)

        playback_state.reset()

        self.assertEqual(playback_state.get_speed(), 1)
