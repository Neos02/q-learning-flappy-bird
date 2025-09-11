import pygame

from main import GREEN, PIPE_WIDTH, SCREEN_WIDTH


class PipeHalf(pygame.sprite.Sprite):

    def __init__(self, left, top, height):
        super().__init__()
        self.width = PIPE_WIDTH
        self.rect = pygame.Rect(left, top, self.width, height)

    def move(self, speed):
        self.rect.move_ip(speed, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)
