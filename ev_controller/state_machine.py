""" State Machine """

import random
import matplotlib.pyplot as plt
import numpy as np
import sys


MAX_TIME = 10


class Controller:
    def __init__(self, control_list, presence_list):
        self.time = 0
        self.control_list = control_list
        self.presence_list = presence_list
        self.control = control_list[0]
        self.presence = presence_list[0]

    def next_step(self):
        self.time += 1
        self.control = control_list[self.time]
        self.presence = presence_list[self.time]


class Record:
    def __init__(self):
        self.y = []


t_list = np.linspace(0, MAX_TIME, MAX_TIME+1)
presence_list = [1 for t in t_list]
control_list = [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
presence = Presence()
control = Control()
record = Record()
controller = Controller(control, presence, control_list, presence_list)
y_max = 10
y_min = 0
charge_rate = 1


class State:
    def __init__(self, charge_rate, name, controller, record, transition_to):
        self.charge_rate = charge_rate
        self.name = name
        self.state_to_transit = None
        self.controller = controller
        self.record = record
        self.transition_to = transition_to

    def check_transition_from(self):
        reachable_states = transition[self]
        for state in reachable_states:
            if state.check_transition_to(self.y_current):
                self.state_to_transit = state
                return True
        return False

    def check_transition_to(self, y):
        return self.transition_to(y, self.controller.control, self.controller.presence)

    def run_step(self):
        return self.y_current + self.charge_rate

    def run_sim(self, y_init):
        self.y_current = y_init
        if self.name == 'gone':
            self.y_current =
        while not self.check_transition_from() and self.controller.time < MAX_TIME:
            self.y_current = self.run_step()
            self.record.y.append(self.y_current)
            self.controller.next_step()
        if self.controller.time >= MAX_TIME:
            return "stop"
        return self.state_to_transit.run_sim(self.y_current)


def t_not_charge(y, control, presence):
    if y == y_max and presence == 1:
        return True
    if control == 0 and presence == 1:
        return True
    return False

def t_charge(y, control, presence):
    if control == 1 and presence == 1:
        return True
    return False

def t_gone(y, control, presence):
    if presence == 0:
        return True
    return False



charge = State(charge_rate, 'charge', controller, record, t_charge)
not_charge = State(0, 'not charge', controller, record, t_not_charge)
gone = State(0, 'gone', controller, record, t_gone)

transition = {
        charge: [not_charge, gone],
        not_charge: [charge, gone],
        gone: [not_charge, charge]}

y_init = 0
record.y.append(y_init)

print(charge.run_sim(y_init))

plt.figure(figsize=(15, 8))
plt.title('Simulation of 1 EV')
plt.xlabel('time')
plt.plot(t_list, record.y, label='soc')
plt.plot(t_list, control_list, label='control')
plt.plot(t_list, presence_list, label='presence')
plt.legend()
plt.grid()
plt.show()
