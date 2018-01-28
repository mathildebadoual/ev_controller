""" Electic Vehicle model """


class ElectricVehicle:
    def __init__(self, action):
        self.action = action

    def __str__(self):
        return self.action

    def __eq__(self, other):
        return self.action == other.action

    def __hash__(self):
        return hash(self.action)
