import pygame

from main import GREEN, SCREEN_WIDTH


class PipeHalf(pygame.sprite.Sprite):

    def __init__(self, top, height):
        super().__init__()
        self.width = 60
        self.rect = pygame.Rect(SCREEN_WIDTH, top, self.width, height)

    def move(self, speed):
        self.rect.move_ip(speed, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)
