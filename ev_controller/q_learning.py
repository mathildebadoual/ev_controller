import random
import environment as environment
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

EPISODES = 1000

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def predict_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


if __name__ == "__main__":
    env = environment.Env()
    state_size = env.state_size
    action_size = env.action_size
    agent = DQNAgent(state_size, action_size)
    done = False
    batch_size = 32
    reward_list = []

    for e in range(EPISODES):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        action = agent.predict_action(state)
        next_state, reward, done = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        reward_list.append(reward[0][0])
        print("episode: {}/{}, reward: {}, e: {:.2}"
                .format(e, EPISODES, reward[0][0], agent.epsilon))
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

    plt.plot(reward_list)
    plt.show()


    state_list = np.zeros((23, state_size))
    state = env.init()
    state_list[0, :] = state[:, 0]
    for e in range(1, 23):
        state = np.reshape(state, [1, state_size])
        action = agent.predict_action(state)
        next_state, reward, done = env.step(action)
        state = next_state
        state_list[e, :] = state[:, 0].T

    print(state_list)
    print(state_list[:, 9])
    plt.figure(figsize=(16, 8))
    plt.plot(state_list[:, 0])
    plt.plot(state_list[:, 1])
    plt.plot(state_list[:, 2])
    plt.plot([10*element for element in state_list[:, 9]], label='price')
    plt.legend()
    plt.show()

