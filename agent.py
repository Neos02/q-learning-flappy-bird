import random
import sys
import pickle
import numpy as np
import pygame

from game import Game
from pygame.locals import *

from main import CLOCK, FPS, GAME_STATE_SCALE_FACTOR, SCREEN_HEIGHT, PIPE_GAP


class Agent:

    def __init__(self):
        self.learning_rate = 0.01
        self.discount_factor = 0.95
        self.epsilon = 0
        self.epsilon_decay = 0.99
        self.epsilon_min = 0
        self.epochs = 10000
        self.table = np.zeros((PIPE_GAP // GAME_STATE_SCALE_FACTOR, SCREEN_HEIGHT // GAME_STATE_SCALE_FACTOR * 2, 2))
        self.game = None
        self.score = []

    def get_action(self, state):
        if not self.game.player.has_jumped:
            return 1

        if random.random() < self.epsilon:
            return random.choice([0, 1])

        return np.argmax(self.table[state])

    def train(self, epoch=1):
        if epoch != 1:
            self._load_model(epoch)

        for epoch in range(epoch, self.epochs + 1):
            self.game = Game()
            current_state = self.game.get_state()
            prev_state = None
            done = False
            is_checkpoint = (epoch <= 100 and epoch % 10 == 0) or (100 <= epoch < 1000 and epoch % 200 == 0) or (
                    epoch >= 1000 and epoch % 500 == 0)

            # decay epsilon
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

            # print updates
            if epoch % 25 == 0 and len(self.score) > 0:
                print(f'Epoch: {epoch}, Score: {np.mean(self.score)}, Epsilon: {self.epsilon}')
                self.score = []

            # occasionally save latest model
            if is_checkpoint:
                with open(f'models/bird_model_{epoch}.pickle', 'wb') as file:
                    # noinspection PyTypeChecker
                    pickle.dump(self.table, file)

            while not done:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                if self.game.get_state() != prev_state:
                    # get best action and take it
                    action = self.get_action(current_state)
                    new_state, reward, done = self.game.step(action)

                    # update table using Bellman equation
                    self.table[current_state][action] = (1 - self.learning_rate) * self.table[current_state][action]\
                        + self.learning_rate * (reward + self.discount_factor * np.max(self.table[new_state]))
                    current_state = new_state

                self.game.deltatime = CLOCK.tick(FPS) / 1000

            self.score.append(self.game.score)

    def _load_model(self, epoch):
        filename = f'models/bird_model_{epoch}.pickle'

        with open(filename, 'rb') as file:
            self.table = pickle.load(file)

        # calculate this epoch's epsilon value to prevent random actions
        self.epsilon = max(self.epsilon * self.epsilon_decay ** epoch, self.epsilon_min)
