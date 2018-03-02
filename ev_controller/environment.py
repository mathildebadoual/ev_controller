import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import state_machine as state_machine

class Env:
    def __init__(self):
        self.num_cars = 3
        self.state_size = self.num_cars * 3 + 2
        self.action_size = 8
        self.state = np.zeros((self.state_size, 1))
        self.theta = 0.5
        self.lambd = 10
        self.get_price_data()
        self.time_simu = 24
        self.create_matrix_a()
        self.charge_rate = 0.005*60
        self.energy_max = 10
        self.create_cars()
        self.create_map_action()

    def create_map_action(self):
        self.map_action = {
                0: np.array([0, 0, 0]),
                1: np.array([1, 1, 1]),
                2: np.array([0, 0, 1]),
                3: np.array([0, 1, 0]),
                4: np.array([1, 0, 0]),
                5: np.array([1, 1, 0]),
                6: np.array([0, 1, 1]),
                7: np.array([1, 0, 1])}


    def create_cars(self):
        self.list_cars = []
        for i in range(self.num_cars):
            self.list_cars.append(state_machine.Car())

    def create_matrix_a(self):
        identity = np.identity(self.num_cars)
        z = np.zeros((self.num_cars, self.num_cars))
        z_h = np.zeros((1, self.num_cars))
        self.a = np.concatenate((
            np.concatenate((identity, z, identity, z_h.T, z_h.T), axis=1),
            np.concatenate((identity*(1 - self.theta), self.theta*identity, z, z_h.T, z_h.T), axis=1),
            np.concatenate((z, z, z, z_h.T, z_h.T), axis=1),
            np.concatenate((z_h, z_h, z_h, [[0]], [[0]]), axis=1),
            np.concatenate((z_h, z_h, z_h, [[0]], [[1]]), axis=1)),
            axis=0)

    def step(self, action):
        real_action = self.map_action[action]
        self.previous_price = self.update_price(self.state[-1, 0])
        self.price = self.update_price(self.state[-1, 0])
        control_sys = np.zeros((self.num_cars, 1))
        for i, car in enumerate(self.list_cars):
            car.control = real_action[i]
            car.presence = self.state[self.num_cars * 2 + i, 0]
            car.soc_init = 1 - self.state[i, 0]
            car.run()
            control_sys[i] = car.record.y[-1] - car.soc_init
        z_h = np.zeros((self.num_cars, 1))
        self.control = np.concatenate((control_sys, z_h, z_h, [[0]], [[0]]), axis=0)
        arrivals = self.create_arrival()
        update = np.concatenate((z_h, z_h, arrivals, self.price, [[0]]), axis=0)
        self.state = np.dot(self.a, self.state) - self.control + update
        reward = self.reward()
        return self.state, reward, False

    def reset(self):
        x = np.random.uniform(0, 1, size=(self.num_cars, 1))
        z = np.random.randint(2, size=(self.num_cars, 1))
        y = np.random.uniform(0, 1, size=(self.num_cars, 1))
        h = np.random.randint(23, size=(1, 1))
        p = self.update_price(h)
        self.state = np.concatenate((x, y, z, p, h), axis=0)
        return self.state

    def create_arrival(self):
        arrival = np.zeros((self.num_cars, 1))
        for i in range(self.num_cars):
            if int(self.state[self.num_cars*2 + i, 0]) == 0:
                arrival[i, 0] = random.uniform(0, 1)*random.randint(0, 1)
            else:
                arrival[i, 0] = 0
        return arrival

    def get_price_data(self):
        self.ref_price_data = pd.read_csv('prices_a10.csv')['prices_to_buy_summer'].values

    def update_price(self, time):
        return np.reshape(self.ref_price_data[int(time)]*(1 + random.uniform(-1/10, 1/10)), (1, 1))

    def reward(self):

        #TODO(Mathilde): Add weights of the consummer satisfaction depending on the hour of the day?

        reward = self.previous_price*self.charge_rate*np.sum(self.control) + self.lambd*np.sum(self.state[self.num_cars:2*self.num_cars, 0])
        return reward
