import pygame

from main import SCREEN_WIDTH, load_image, SCREEN_HEIGHT


class ScrollingImage(pygame.sprite.Sprite):

    def __init__(self, image_path, bottom=SCREEN_HEIGHT):
        super().__init__()
        self.image = load_image(image_path)
        self.rect = pygame.Rect(0, 0, 2 * SCREEN_WIDTH, self.image.get_height())
        self.rect.bottom = bottom

    def move(self, speed):
        self.rect.move_ip(speed, 0)

        while self.rect.left <= -self.image.get_width():
            self.rect.move_ip(self.image.get_width(), 0)

    def draw(self, screen):
        for i in range(2 * SCREEN_WIDTH // self.image.get_width()):
            screen.blit(
                self.image,
                pygame.Rect(
                    self.rect.left + i * self.image.get_width(),
                    self.rect.top,
                    self.image.get_width(),
                    self.image.get_height()
                )
            )
