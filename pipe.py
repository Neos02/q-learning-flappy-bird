import random
import pygame

from main import SCREEN_HEIGHT, PIPE_SPEED, IMAGE_SCALE_FACTOR
from pipe_half import PipeHalf

MIN_PIPE_HEIGHT = 100
PIPE_GAP_HEIGHT = 180
PIPE_IMAGE = pygame.transform.scale_by(pygame.image.load('images/pipe.png').convert_alpha(), IMAGE_SCALE_FACTOR)
PIPE_WIDTH = PIPE_IMAGE.get_width()


class Pipe(pygame.sprite.Group):

    def __init__(self, center=None):
        super().__init__()
        self.image = PIPE_IMAGE
        self.upper = PipeHalf()
        self.lower = PipeHalf(True)
        self.center = center
        self.add(self.upper, self.lower)

    def move(self, deltatime):
        self.center = (self.center[0] - PIPE_SPEED * deltatime, self.center[1])

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

        self.upper.rect.left = self._center[0] - self.image.get_width() / 2
        self.upper.rect.bottom = self._center[1] - PIPE_GAP_HEIGHT / 2

        self.lower.rect.left = self.upper.rect.left
        self.lower.rect.top = self.upper.rect.bottom + PIPE_GAP_HEIGHT

    @staticmethod
    def get_random_height():
        return random.randint(MIN_PIPE_HEIGHT, SCREEN_HEIGHT - PIPE_GAP_HEIGHT - MIN_PIPE_HEIGHT)
