import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt


class Env:
    def __init__(self):
        self.num_cars = 3
        self.state_size = self.num_cars * 3 + 1
        self.action_size = self.num_cars
        self.state = np.zeros((self.state_size, 1))
        self.theta = 0.5
        self.lambd = 1
        self.ref_price_data = self.get_price_data()
        self.price_data = np.zeros(len(self.ref_price_data))
        self.update_price()
        self.price = 0
        self.time_simu = 24
        self.create_matrix_a()
        self.time = 1
        self.state[-1, 0] == self.price_data[0]
        self.energy_max = 10

    def create_matrix_a(self):
        identity = np.identity(self.num_cars)
        i_theta = identity*(1 - self.theta)
        z = np.zeros((self.num_cars, self.num_cars))
        z_h = np.zeros((1, self.num_cars))
        self.a = np.concatenate((
            np.concatenate((identity, z, identity, z_h.T), axis=1),
            np.concatenate((i_theta, self.theta*identity, z, z_h.T), axis=1),
            np.concatenate((z, z, z, z_h.T), axis=1),
            np.concatenate((z_h, z_h, z_h, [[0]]), axis=1)),
            axis=0)

    def step(self, action):
        print(action)
        self.previous_price = self.price

        if self.time < 24:
            self.price = self.price_data[self.time]
            self.time += 1
        if self.time == 24:
            self.update_price()
            self.time = 0

        for i in range(self.num_cars):
            if self.state[i, 0] == 0:
                action[i] = 0
        z_h = np.zeros((self.num_cars, 1))
        self.control = np.concatenate((action, z_h, z_h, [[0]]), axis=0)
        arrivals = self.create_arrival()
        update = np.concatenate((z_h, z_h, arrivals, [[self.price]]), axis=0)

        self.state = np.dot(self.a, self.state) - self.control + update
        reward = self.reward

        return self.state, reward, False

    def reset(self):
        return self.state

    def create_arrival(self):
        arrival = np.zeros((self.num_cars, 1))
        for i in range(self.num_cars):
            if self.state[i, 0] == 0:
                arrival[i, 0] = random.uniform(0, 1)*random.randint(0, 1)
            else:
                arrival[i, 0] = 0
            print(arrival[i, 0])
        return arrival

    def get_price_data(self):
        ref_price_data = pd.read_csv('prices_a10.csv')['prices_to_buy_summer'].values
        return ref_price_data

    def update_price(self):
        for i, price in enumerate(self.ref_price_data):
            self.price_data[i] = price + random.uniform(-1/10, 1/10)*price

    def reward(self):
        reward = self.previous_price*np.sum(self.control)
        + self.lambd*np.sum(self.state[self.sum_cars:2*self.num_cars, 0])
        + np.sum(np.log((self.control - self.state[:self.num_cars, 0])))
        + np.log(np.sum(self.control) - self.energy_max)
        return reward
