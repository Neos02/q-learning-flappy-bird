import random
import pygame

from main import SCREEN_HEIGHT
from pipe_half import PipeHalf


class Pipe(pygame.sprite.Group):

    def __init__(self, left, height=None):
        super().__init__()
        self.gap = 180
        self.speed = 200
        self.min_pipe_height = 50
        self.gap_top = random.randint(self.min_pipe_height, SCREEN_HEIGHT - self.gap - self.min_pipe_height) if height is None else height
        self.top_pipe = PipeHalf(left, self.gap_top)
        self.bottom_pipe = PipeHalf(left, self.gap + self.gap_top, True)
        self.add(self.top_pipe, self.bottom_pipe)

    def move(self, deltatime):
        self.top_pipe.move(-self.speed * deltatime)
        self.bottom_pipe.move(-self.speed * deltatime)

    def draw(self, surface):
        self.top_pipe.draw(surface)
        self.bottom_pipe.draw(surface)

    def is_off_screen(self):
        return self.top_pipe.rect.right < 0

    def set_left(self, left):
        self.top_pipe.rect.left = left
        self.bottom_pipe.rect.left = left
