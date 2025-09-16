import pygame
from pygame.math import clamp

from main import SCREEN_WIDTH, SCREEN_HEIGHT, IMAGE_SCALE_FACTOR
from pygame.locals import *


class Player(pygame.sprite.Sprite):

    def __init__(self, is_agent=False):
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
        self.rotation_angle_deg = 30
        self.is_agent = is_agent

    def move(self, deltatime):
        if not self.is_agent:
            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_SPACE] and self.can_jump():
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
        rotated_image = pygame.transform.rotate(self.image, clamp(-self.velocity_y / 15, -self.rotation_angle_deg, self.rotation_angle_deg))
        surface.blit(rotated_image, self.rect)

    def can_jump(self):
        ticks = pygame.time.get_ticks()
        return ticks - self.last_jump_time >= self.jump_cooldown_ms

    def jump(self):
        ticks = pygame.time.get_ticks()
        self.velocity_y = -self.jump_power
        self.last_jump_time = ticks
        self.has_jumped = True
