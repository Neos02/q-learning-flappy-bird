import sys
import pickle
import numpy as np
import pygame

from game import Game
from pygame.locals import *

from main import FPS
from pipe import Pipe


def _handle_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


class Agent:

    def __init__(self, model_dir="models"):
        self.learning_rate = 0.01
        self.discount_factor = 0.95
        self.epochs = 10000
        self.game = Game(is_agent=True)
        self.table = np.zeros(((Game.pipe_gap + Pipe.width) // 2 // Game.state_distance_scale_factor + 1, 2 * Game.pipe_gap // Game.state_distance_scale_factor + 2, 2))
        self.score = []
        self.model_dir = model_dir

    def get_action(self, state):
        if not self.game.player.has_jumped:
            return 1

        return np.argmax(self.table[state])

    def train(self, epoch=1):
        if epoch != 1:
            self._load_model(epoch)

        for epoch in range(epoch, self.epochs + 1):
            self.game = Game(is_agent=True)
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
                with open(f'{self.model_dir}/bird_model_{epoch}.pickle', 'wb') as file:
                    # noinspection PyTypeChecker
                    pickle.dump(self.table, file)

            while not done:
                _handle_events()

                # get best action and take it
                action = 0 if current_state == prev_state else self.get_action(current_state)
                new_state, reward, done = self.game.step(action)
                prev_state = current_state

                # update table using Bellman equation
                self.table[current_state][action] = (1 - self.learning_rate) * self.table[current_state][action]\
                    + self.learning_rate * (reward + self.discount_factor * np.max(self.table[new_state]))
                current_state = new_state

                # prevent running infinitely
                if self.game.score > 100:
                    break

                self.game.deltatime = pygame.time.Clock().tick(FPS) / 1000

            self.score.append(self.game.score)

    def run_epoch(self, epoch):
        self._load_model(epoch)
        self.game = Game(is_agent=True)
        current_state = self.game.get_state()
        prev_state = None
        done = False

        while not done:
            _handle_events()

            # get best action and take it
            action = 0 if current_state == prev_state else self.get_action(current_state)
            new_state, reward, done = self.game.step(action)
            prev_state = current_state
            current_state = new_state
            self.game.deltatime = pygame.time.Clock().tick(FPS) / 1000

    def _load_model(self, epoch):
        filename = f'{self.model_dir}/bird_model_{epoch}.pickle'

        with open(filename, 'rb') as file:
            self.table = pickle.load(file)
