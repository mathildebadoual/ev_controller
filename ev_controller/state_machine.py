""" State Machine """

class Record:
    def __init__(self):
        self.y = []


class State:
    def __init__(self, charge_rate, name, car, transition_to):
        self.charge_rate = charge_rate
        self.name = name
        self.state_to_transit = None
        self.car = car
        self.transition_to = transition_to

    def check_transition_from(self):
        reachable_states = self.car.transition[self]
        for state in reachable_states:
            if state.check_transition_to(self.y_current):
                self.state_to_transit = state
                return True
        return False

    def check_transition_to(self, y):
        return self.transition_to(y, self.car)

    def run_step(self):
        return self.y_current + self.charge_rate

    def run_sim(self, y_init):
        self.y_current = y_init
        if self.name == 'gone':
            self.y_current = 0
        while not self.check_transition_from() and self.car.time < self.car.max_time:
            self.y_current = self.run_step()
            self.car.record.y.append(self.y_current)
            self.car.next_step()
        if self.car.time >= self.car.max_time:
            return "stop"
        return self.state_to_transit.run_sim(self.y_current)


def t_not_charge(y, car):
    if y == car.y_max and car.presence == 1:
        return True
    if car.control == 0 and car.presence == 1:
        return True
    return False

def t_charge(y, car):
    if car.control == 1 and car.presence == 1:
        return True
    return False

def t_gone(y, car):
    if car.presence == 0:
        return True
    return False


class Car:
    def __init__(self):
        self.record = Record()
        self.y_max = 1
        self.y_min = 0
        charge_rate = 0.005
        self.charge = State(charge_rate, 'charge', self, t_charge)
        self.not_charge = State(0, 'not charge', self, t_not_charge)
        self.gone = State(0, 'gone', self, t_gone)
        self.transition = {
                self.charge: [self.not_charge, self.gone],
                self.not_charge: [self.charge, self.gone],
                self.gone: [self.not_charge, self.charge]}
        self.time = 0
        self.control = 0
        self.presence = 1
        self.max_time = 60
        self.soc_init = 0

    def next_step(self):
        self.time += 1

    def run(self):
        if self.presence == 0:
            self.gone.run_sim(self.soc_init)
        if self.control == 0 and self.presence == 1:
            self.not_charge.run_sim(self.soc_init)
        if self.control == 1 and self.presence == 1:
            self.charge.run_sim(self.soc_init)
