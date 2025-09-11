import pygame

from main import RED, SCREEN_WIDTH, SCREEN_HEIGHT
from pygame.locals import *


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.gravity = 0.5
        self.height = SCREEN_HEIGHT // 2
        self.velocity_y = 0
        self.size = 10
        self.jump_power = 10
        self.jump_cooldown_ms = 225
        self.last_jump_time = 0

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()

        if pressed_keys[K_SPACE] and ticks - self.last_jump_time >= self.jump_cooldown_ms:
            self.velocity_y = -self.jump_power
            self.last_jump_time = ticks

        self.velocity_y += self.gravity
        self.height += self.velocity_y

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (SCREEN_WIDTH // 4, self.height), self.size)
