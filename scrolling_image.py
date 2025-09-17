import pygame

from main import SCREEN_WIDTH, load_image


class ScrollingImage(pygame.sprite.Sprite):

    def __init__(self, image_path):
        super().__init__()
        self.image = load_image(image_path)
        self.rect = self.image.get_rect()

    def move(self, speed):
        self.rect.move_ip(speed, 0)

        if self.rect.left <= -self.image.get_width():
            self.rect.left += self.image.get_width()

    def draw(self, screen):
        for i in range(SCREEN_WIDTH // self.image.get_width() + 2):
            screen.blit(
                self.image,
                pygame.Rect(
                    self.rect.left + i * self.image.get_width(),
                    self.rect.top,
                    self.image.get_width(),
                    self.image.get_height()
                )
            )
