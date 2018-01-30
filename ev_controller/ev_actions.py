""" Electic Vehicle possible actions or transitions """

import ev_controller.ev_states as ev_states
import ev_controller.ev_conditions as ev_conditions

class EvAction:
    def __init__(self, action):
        self.action = action

    def __str__(self):
        return self.action

    def __eq__(self, other):
        return self.action == other.action

    def __hash__(self):
        return hash(self.action)


class Leaves(EvAction):
    def __init__(self):
        pass


class Arrives(EvAction):
    def __init__(self):
        pass


class Charges(EvAction):
    def __init__(self):
        pass


class StopsCharging(EvAction):
    def __init__(self):
        pass



