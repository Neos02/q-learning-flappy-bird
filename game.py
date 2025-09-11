import math
import sys
import pygame

from pygame.locals import *
from main import SCREEN_WIDTH, DISPLAYSURF, BLUE, CLOCK, FPS, PIPE_WIDTH
from player import Player
from pipe import Pipe


class Game:

    def __init__(self):
        self.pipe_gap = 200
        self.num_pipes = math.ceil(SCREEN_WIDTH / (self.pipe_gap + PIPE_WIDTH))
        self.pipes = [Pipe(i * (self.pipe_gap + PIPE_WIDTH)) for i in range(self.num_pipes)]
        self.rightmost_pipe = self.pipes[self.num_pipes - 1]
        self.player = Player()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            self.player.move()

            for pipe in self.pipes:
                pipe.move()

                if pipe.is_off_screen():
                    pipe.set_left(self.rightmost_pipe.top_pipe.rect.right + self.pipe_gap)
                    self.rightmost_pipe = pipe

            DISPLAYSURF.fill(BLUE)
            self.player.draw(DISPLAYSURF)

            for pipe in self.pipes:
                pipe.draw(DISPLAYSURF)

            pygame.display.update()
            CLOCK.tick(FPS)
