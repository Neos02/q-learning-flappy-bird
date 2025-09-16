import sys
import pickle
import numpy as np
import pygame

from game import Game
from pygame.locals import *

from main import CLOCK, FPS, GAME_STATE_SCALE_FACTOR, PIPE_GAP


class Agent:

    def __init__(self):
        self.learning_rate = 0.01
        self.discount_factor = 0.95
        self.epochs = 10000
        self.game = Game()
        self.table = np.zeros(((PIPE_GAP + self.game.pipes[0].top_pipe.rect.width) // 2 // GAME_STATE_SCALE_FACTOR + 1, 2 * self.game.pipes[0].gap // GAME_STATE_SCALE_FACTOR + 2, 2))
        self.score = []

    def get_action(self, state):
        if not self.game.player.has_jumped:
            return 1

        return np.argmax(self.table[state])

    def train(self, epoch=1):
        if epoch != 1:
            self._load_model(epoch)

        for epoch in range(epoch, self.epochs + 1):
            self.game = Game()
            current_state = self.game.get_state()
            prev_state = None
            done = False
            is_checkpoint = (epoch <= 100 and epoch % 10 == 0) or epoch % 100 == 0

            # print updates
            if epoch % 25 == 0 and len(self.score) > 0:
                print(f'Epoch: {epoch}, Score: {np.mean(self.score)}')
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

                # get best action and take it
                action = 0 if current_state == prev_state else self.get_action(current_state)
                new_state, reward, done = self.game.step(action)
                prev_state = current_state

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
