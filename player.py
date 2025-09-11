import pygame
from pygame.math import clamp

from main import SCREEN_WIDTH, SCREEN_HEIGHT, IMAGE_SCALE_FACTOR
from pygame.locals import *


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.bird_image = pygame.transform.scale_by(pygame.image.load('images/bird.png').convert_alpha(), IMAGE_SCALE_FACTOR)
        self.bird_flap_image = pygame.transform.scale_by(pygame.image.load('images/bird-flap.png').convert_alpha(), IMAGE_SCALE_FACTOR)
        self.image = self.bird_image
        self.gravity = 1400
        self.velocity_y = 0
        self.size = 20
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.jump_power = 550
        self.jump_cooldown_ms = 225
        self.last_jump_time = 0
        self.has_jumped = False

    def move(self, deltatime):
        pressed_keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()

        if pressed_keys[K_SPACE] and ticks - self.last_jump_time >= self.jump_cooldown_ms:
            self.jump()

        # show flap image when the bird is moving up
        if self.velocity_y < 0:
            self.image = self.bird_flap_image
        else:
            self.image = self.bird_image

        if self.has_jumped:
            self.velocity_y += self.gravity * deltatime
            self.rect.top = max(0, self.rect.top + self.velocity_y * deltatime)

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, clamp(-self.velocity_y / 20, -45, 45))
        surface.blit(rotated_image, self.rect)

    def is_off_screen(self):
        return self.rect.bottom > SCREEN_HEIGHT

    def jump(self):
        self.velocity_y = -self.jump_power
        self.last_jump_time = ticks
        self.has_jumped = True
