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
        self.add(self.upper, self.lower)
        self.center = center

    def move(self, speed):
        self._center = (round(self.center[0] + speed), self.center[1])

        for sprite in self.sprites():
            sprite.move(speed)

    def is_off_screen(self):
        return self.upper.rect.right < 0

    def randomize_height(self):
        self.center = (self.center[0], Pipe.get_random_height())

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = (0, 0) if value is None else (round(value[0]), round(value[1]))

        self.upper.rect.center = (self._center[0], self._center[1] - Pipe.gap_height / 2 - PipeHalf.image.get_height() / 2)
        self.lower.rect.center = (self._center[0], self._center[1] + Pipe.gap_height / 2 + PipeHalf.image.get_height() / 2)

    @staticmethod
    def get_random_height():
        return random.randint(Pipe.min_height, SCREEN_HEIGHT - Pipe.gap_height - Pipe.min_height)
