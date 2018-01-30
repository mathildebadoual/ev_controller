""" Conditions to stay or transit a state """

import ev_controller.ev_actions as ev_actions
import ev_controller.ev_states as ev_states
import random


class Condition:
    def __init__(self):
        random.seed(a=10)

    def test_is_true(self):
        return NotImplementedError


class HasToLeave(Condition):
    def test_is_true(self):
        random_num = random.randint(0, 1)
        if random_num:
            return True
        else:
            return False


class HasToComeBack(Condition):
    def test_is_true(self):
        random_num = random.randint(0, 1)
        if random_num:
            return True
        else:
            return False
