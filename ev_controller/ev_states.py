""" State Machine """

import ev_controller.ev_actions as ev_actions
import ev_controller.ev_conditions as ev_conditions

class StateMachine:
    def __init__(self, initial_state, condition_table):
        self.initial_state = initial_state
        self.current_state = initial_state

    def run_all(self, num_iter):
        while i < num_iter:
            self.current_state.run()
            self.current_state = self.current_state.next()
            i += 1

    def reset(self):
        self.current_state = self.initial_state


class State:
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError


class Gone(State):
    def __init__(self):
        super().__init__(self)
        self.has_to_come_back = ev_conditions.HasToComeBack()

    def run(self):
        print('The car is gone')

    def next(self):
        if self.has_to_come_back.test_is_true():
            return
        return self


class PluggedIn(State):
    def __init__(self):
        super().__init__(self)
        self.has_to_leave = ev_conditions.HasToLeave()

    def run(self):
        print('The car is plugged in')

    def next(self):
        if self.has_to_leave.test_is_true():
            return Gone()
        return self


class Charging(State):
    self.soc = 0

    def __init__(self):
        super().__init__(self)

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
        super().__init__(self)

    def run(self):
        print('The car stopped charging')

    def next(self, input):
        if input == EvAction.charging:
            return input
        return EvAction.stopcharging


