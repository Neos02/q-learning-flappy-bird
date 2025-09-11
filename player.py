import pygame

from main import RED, SCREEN_WIDTH, SCREEN_HEIGHT
from pygame.locals import *


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.gravity = 1400
        self.velocity_y = 0
        self.size = 20
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.jump_power = 550
        self.jump_cooldown_ms = 225
        self.last_jump_time = 0
        self.has_jumped = False

    def move(self, deltatime):
        pressed_keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()

        if pressed_keys[K_SPACE] and ticks - self.last_jump_time >= self.jump_cooldown_ms:
            self.velocity_y = -self.jump_power
            self.last_jump_time = ticks
            self.has_jumped = True

        if self.has_jumped:
            self.velocity_y += self.gravity * deltatime
            self.rect.top = max(0, self.rect.top + self.velocity_y * deltatime)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

    def is_off_screen(self):
        return self.rect.bottom > SCREEN_HEIGHT
