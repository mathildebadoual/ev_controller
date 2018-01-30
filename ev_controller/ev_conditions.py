""" Conditions to stay or transit a state """

import ev_controller.ev_actions as ev_actions
import ev_controller.ev_states as ev_states


class Condition:
    def __init__(self):
        pass

    def test_true(self, value):
        raise NotImplementedError


