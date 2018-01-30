""" State Machine """

import ev_controller.ev_actions as ev_actions
import ev_controller.ev_conditions as ev_conditions


class StateMachine:
    def __init__(self, initial_state):
        sellf.initial_state = initial_state
        self.current_state = initial_state
        self.current_state.run()

    def run_all(self):
        pass

    def reset(self):
        self.current_state = self.initial_state

class State:
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError


class Gone():
    def __init__(self):
        pass

    def run(self):
        print('The car is gone')

    def next(self, inputs):
        if input == EvAction.isplugged:
            return car_is_plugged
        return car_is_gone


class Plugged(State):
    def __init__(self):
        pass

    def run(self):
        print('The car is plugged')

    def next(self, inputs):
        if input == EvAction.isgone:
            return car_is_gone
        return car_is_plugged


class Charging(State):
    def __init__(self):
        self.soc = 0
        self.soc_max = 10

    def run(self):
        print('The car is charging')
        self.soc += 1

    def next(self, input):
        if self.soc == self.soc_max:
            return EvAction.stopcharging
        if input == EvAction.stopcharging:
            return
        return EvAction.charging


class StopingCharging(State):
    def __init__(self):
        pass

    def run(self):
        print('The car stopped charging')

    def next(self, input):
        if input == EvAction.charging:
            return input
        return EvAction.stopcharging


