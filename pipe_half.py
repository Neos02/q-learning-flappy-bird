import pygame

from main import PIPE_WIDTH, IMAGE_SCALE_FACTOR


class PipeHalf(pygame.sprite.Sprite):

    def __init__(self, left, pipe_end_height, flip=False):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load('images/pipe.png').convert_alpha(), IMAGE_SCALE_FACTOR)
        self.width = PIPE_WIDTH
        self.rect = self.image.get_rect()

        if flip:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect()
            self.rect.top = pipe_end_height
        else:
            self.rect.bottom = pipe_end_height

        self.rect.left = left

    def move(self, speed):
        self.rect.move_ip(speed, 0)

    def draw(self, surface):
        # pygame.draw.rect(surface, GREEN, self.rect)
        surface.blit(self.image, self.rect)
