import pygame

from main import IMAGE_SCALE_FACTOR


class PipeHalf(pygame.sprite.Sprite):

    def __init__(self, flip_y=False):
        super().__init__()
        self.image = pygame.transform.flip(
            pygame.transform.scale_by(
                pygame.image.load('images/pipe.png').convert_alpha(),
                IMAGE_SCALE_FACTOR
            ),
            False,
            flip_y
        )
        self.rect = self.image.get_rect()

    def move(self, speed):
        self.rect.move_ip(speed, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
