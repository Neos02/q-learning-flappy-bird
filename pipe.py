import pygame

from main import GREEN, SCREEN_WIDTH, SCREEN_HEIGHT


class Pipe(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.width = 60
        self.height = 350
        self.speed = 3
        self.rect = pygame.Rect(SCREEN_WIDTH, SCREEN_HEIGHT - self.height, self.width, self.height)

    def move(self):
        self.rect.move_ip(-self.speed, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)
