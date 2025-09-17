import pygame

from main import load_image


class PipeHalf(pygame.sprite.Sprite):
    image = load_image('images/pipe.png')

    def __init__(self, flip_y=False):
        super().__init__()
        self.image = PipeHalf.image

        if flip_y:
            self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()

    def move(self, speed):
        self.rect.move_ip(speed, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
