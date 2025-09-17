import random
import pygame

from main import SCREEN_HEIGHT
from pipe_half import PipeHalf


class Pipe(pygame.sprite.Group):

    width = PipeHalf.image.get_width()
    gap_height = 180
    min_height = 100

    def __init__(self, center=None):
        super().__init__()
        self.upper = PipeHalf()
        self.lower = PipeHalf(True)
        self.center = center
        self.add(self.upper, self.lower)

    def move(self, speed):
        self._center = (self.center[0] + speed, self.center[1])

        for sprite in self.sprites():
            sprite.move(speed)

    def draw(self, surface):
        for sprite in self.sprites():
            sprite.draw(surface)

    def is_off_screen(self):
        return self.upper.rect.right < 0

    def randomize_height(self):
        self.center = (self.center[0], Pipe.get_random_height())

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = (0, 0) if value is None else value

        self.upper.rect.left = self._center[0] - Pipe.width / 2
        self.upper.rect.bottom = self._center[1] - Pipe.gap_height / 2

        self.lower.rect.left = self.upper.rect.left
        self.lower.rect.top = self.upper.rect.bottom + Pipe.gap_height

    @staticmethod
    def get_random_height():
        return random.randint(Pipe.min_height, SCREEN_HEIGHT - Pipe.gap_height - Pipe.min_height)
