import unittest
import numpy as np
import ev_controller.mpc as mpc

class TestMPC(unittest.TestCase):
    def setUp(self):
        self.num_cars = mpc.NUM_CARS
        self.control_horizon = mpc.CONTROL_HORIZON
        self.simulation_time = mpc.SIMULATION_TIME
        self.alpha, self.beta, self.gamma = mpc.get_parameters()

    def test_get_cost_matrix(self):
        Q, R = mpc.get_cost_matrix()
        self.assertEqual(R.shape, (self.num_cars, self.num_cars, self.simulation_time))
        self.assertEqual(R[0, 0, 0], 0.13**2*self.alpha)
        self.assertEqual(Q[0, 0, 0], self.beta)

    def test_get_model_matrix(self):
        A, B = mpc.get_model_matrix()
        self.assertEqual(A[0, 0], 1)
        self.assertEqual(B[0, 0], self.gamma)

    def test_mpc_control(self):
        x = mpc.mpc_control(np.zeros((self.num_cars)))
        self.assertIsNotNone(x)

