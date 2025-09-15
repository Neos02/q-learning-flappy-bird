import math
import sys
import time

import pygame

from pygame.locals import *
from main import SCREEN_WIDTH, DISPLAYSURF, BLUE, CLOCK, FPS, PIPE_WIDTH, RED, SCREEN_HEIGHT, FONT_LARGE, WHITE, \
    FONT_SMALL, GAME_STATE_SCALE_FACTOR, PIPE_GAP, PIPE_SPEED
from player import Player
from pipe import Pipe
from scrolling_image import ScrollingImage


def game_over():
    game_over_text = FONT_LARGE.render("GAME OVER", True, WHITE)
    DISPLAYSURF.fill(RED)
    DISPLAYSURF.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) / 2, (SCREEN_HEIGHT - game_over_text.get_height()) / 2))

    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()


class Game:

    def __init__(self):
        self.deltatime = 0
        self.num_pipes = math.ceil(SCREEN_WIDTH / (PIPE_GAP + PIPE_WIDTH))
        self.pipes = [Pipe(i * (PIPE_GAP + PIPE_WIDTH) + SCREEN_WIDTH // 2, (SCREEN_HEIGHT - PIPE_GAP) // 2 if i == 0 else None) for i in range(self.num_pipes)]
        self.rightmost_pipe = self.pipes[self.num_pipes - 1]
        self.next_pipe = 0
        self.player = Player()
        self.score = 0

        # load ground image
        self.ground_image = ScrollingImage("images/ground.png")
        self.ground_image.rect.bottom = SCREEN_HEIGHT

        # load bush image
        self.bush_image = ScrollingImage("images/bush.png")
        self.bush_image.rect.bottom = SCREEN_HEIGHT - self.ground_image.image.get_height()

        # load city image
        self.city_image = ScrollingImage("images/city.png")
        self.city_image.rect.bottom = SCREEN_HEIGHT - self.ground_image.image.get_height() - self.bush_image.image.get_height() + 6

        # load cloud image
        self.cloud_image = ScrollingImage("images/cloud.png")
        self.cloud_image.rect.bottom = SCREEN_HEIGHT - self.ground_image.image.get_height() - self.bush_image.image.get_height() - self.city_image.image.get_height() + 6 + 26

    def _move(self):
        self.player.move(self.deltatime)

        if self.player.has_jumped:
            for pipe in self.pipes:
                pipe.move(self.deltatime)

                if pipe.is_off_screen():
                    pipe.set_left(self.rightmost_pipe.top_pipe.rect.right + PIPE_GAP)
                    self.rightmost_pipe = pipe

            self.ground_image.move(-PIPE_SPEED * self.deltatime)
            self.bush_image.move(-PIPE_SPEED * self.deltatime)
            self.city_image.move(-PIPE_SPEED * self.deltatime)
            self.cloud_image.move(-PIPE_SPEED * self.deltatime)

        if self.pipes[self.next_pipe].top_pipe.rect.right < self.player.rect.left:
            self.score += 1
            self.next_pipe = (self.next_pipe + 1) % self.num_pipes

    def _draw(self):
        DISPLAYSURF.fill(BLUE)
        self.cloud_image.draw(DISPLAYSURF)
        self.city_image.draw(DISPLAYSURF)
        self.bush_image.draw(DISPLAYSURF)
        self.player.draw(DISPLAYSURF)

        for pipe in self.pipes:
            pipe.draw(DISPLAYSURF)

        self.ground_image.draw(DISPLAYSURF)

        score_text = FONT_SMALL.render(str(self.score), True, WHITE)
        DISPLAYSURF.blit(score_text, (SCREEN_WIDTH - 100, 10))

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            self._move()
            self._draw()

            if self.is_player_dead():
                game_over()

            pygame.display.flip()
            self.deltatime = CLOCK.tick(FPS) / 1000

    def get_state(self):
        pipe = self.pipes[self.next_pipe]
        pipe_right_center = (pipe.top_pipe.rect.right, pipe.top_pipe.rect.bottom + pipe.gap / 2)
        max_horizontal_distance = (PIPE_GAP // GAME_STATE_SCALE_FACTOR) - 1
        horizontal_distance = min((pipe_right_center[0] - self.player.rect.left) // GAME_STATE_SCALE_FACTOR, max_horizontal_distance)

        return (
            int(horizontal_distance),  # scaled horizontal distance from center of pipe
            int(max(0, (pipe_right_center[1] - self.player.rect.center[1] + SCREEN_HEIGHT) // GAME_STATE_SCALE_FACTOR))  # scaled + shifted vertical distance from center of pipe
        )

    def step(self, action):
        reward = 15
        is_dead = False
        prev_score = self.score

        if action == 1:
            self.player.jump()

        self._move()
        self._draw()
        pygame.display.flip()

        if self.score > prev_score:
            reward = 100

        if self.is_player_dead():
            is_dead = True
            reward = -1000

        current_state = self.get_state()

        return current_state, reward, is_dead

    def is_player_dead(self):
        for pipe in self.pipes:
            if pygame.sprite.spritecollideany(self.player, pipe):
                return True

        return self.player.is_off_screen()
