""" State Machine """

import ev_controller.ev_model as ev_model

class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.current_state.run()

    def run_all(self):
        self

class State:
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError


class CarIsGone():
    def __init__(self):
        pass

    def run(self):
        print('The car is gone')

    def next(self, inputs):
        if input


class CarIsPlugged(State):
    def __init__(self):
        pass


class CarCharging(State):
    def __init__(self):
        pass


class CarStopCharging(State):
    def __init__(self):
        pass
