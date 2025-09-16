import random
import pygame

from main import SCREEN_HEIGHT, PIPE_SPEED
from pipe_half import PipeHalf


class Pipe(pygame.sprite.Group):

    def __init__(self, left, height=None):
        super().__init__()
        self.gap = 180
        self.min_pipe_height = 50
        self.gap_top = 0
        self.left = left
        self.top_pipe = PipeHalf(self.left, self.gap_top)
        self.bottom_pipe = PipeHalf(self.left, self.gap + self.gap_top, True)
        self.set_height(height)
        self.add(self.top_pipe, self.bottom_pipe)

    def move(self, deltatime):
        self.top_pipe.move(-PIPE_SPEED * deltatime)
        self.bottom_pipe.move(-PIPE_SPEED * deltatime)

    def draw(self, surface):
        self.top_pipe.draw(surface)
        self.bottom_pipe.draw(surface)

    def is_off_screen(self):
        return self.top_pipe.rect.right < 0

    def set_left(self, left):
        self.left = left
        self.top_pipe.rect.left = left
        self.bottom_pipe.rect.left = left

    def set_height(self, height=None):
        self.gap_top = random.randint(self.min_pipe_height, SCREEN_HEIGHT - self.gap - self.min_pipe_height) if height is None else height
        self.top_pipe.rect.bottom = self.gap_top
        self.bottom_pipe.rect.top = self.gap + self.gap_top
