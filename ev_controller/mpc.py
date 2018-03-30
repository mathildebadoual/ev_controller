import matplotlib.pyplot as plt
import numpy as np
import math
import time
import cvxpy
import pandas as pd

NUM_CARS = 3
CONTROL_HORIZON = 24*4
SIMULATION_TIME = 24*4


def get_parameters():
    alpha = 10
    beta = 0.5
    gamma = 1
    return alpha, beta, gamma

def get_data():
    prices_day = np.array([1, 1, 1, 1, 8, 9, 8, 8, 6, 5, 4, 4, 5, 5, 6, 6, 7, 10, 12, 7, 5, 5, 3, 1])
    prices = prices_day
    for i in range(int(SIMULATION_TIME/len(prices_day))-1):
        prices = np.concatenate((prices, prices_day))
    prices = np.concatenate((prices, [0]))
    cars_presence = np.ones((SIMULATION_TIME, NUM_CARS))
    return prices, cars_presence

def simulation(x, u):
    A, B = get_model_matrix()
    return np.dot(A, x) + np.dot(B, u)

def mpc_control(x0):
    x = cvxpy.Variable(NUM_CARS, CONTROL_HORIZON+1)
    u = cvxpy.Variable(NUM_CARS, CONTROL_HORIZON)

    A, B = get_model_matrix()
    Q, R = get_cost_matrix()

    alpha, beta, gamma = get_parameters()

    cost = 0
    constraints = []

    for t in range(CONTROL_HORIZON):
        cost += cvxpy.quad_form((np.ones((NUM_CARS)) - x[:, t+1]), Q[:, :, t])
        cost += cvxpy.quad_form(u[:, t], R[:, :, t])
        constraints += [x[:, t+1] == A * x[:, t] +B * u[:, t]]
    constraints += [x[:, 0] == x0]

    prob = cvxpy.Problem(cvxpy.Minimize(cost), constraints)

    start = time.time()
    prob.solve(verbose=False)
    elapsed_time = time.time() - start
    print('calculation time: {0} [sec]'.format(elapsed_time))

    if prob.status == cvxpy.OPTIMAL:
        return x.value

def get_model_matrix():
    gamma = get_parameters()[2]
    A = np.eye(NUM_CARS)
    B = np.eye(NUM_CARS) * gamma
    return A, B

def get_cost_matrix():
    prices, cars_presence = get_data()
    alpha, beta = get_parameters()[:2]

    Q = np.zeros((NUM_CARS, NUM_CARS, SIMULATION_TIME))
    R = np.zeros((NUM_CARS, NUM_CARS, SIMULATION_TIME))

    for i in range(SIMULATION_TIME):
        R[:, :, i] = np.eye(NUM_CARS) * alpha * prices[i+1]**2
        Q[:, :, i] = np.eye(NUM_CARS) * beta

    return Q, R


if __name__ == '__main__':
    x = mpc_control(np.array([0.5, 0.2, 0]))
    prices, cars_presence  = get_data()
    print(x)
    plt.figure(figsize=(10, 7))
    for i in range(NUM_CARS):
        plt.plot(range(CONTROL_HORIZON+1), x[i, :].T, label='soc of car '+str(i))
    plt.plot(range(CONTROL_HORIZON), prices[:CONTROL_HORIZON]/max(prices), label='prices')
    plt.legend()
    plt.grid()
    plt.savefig('result_mpc.png')



