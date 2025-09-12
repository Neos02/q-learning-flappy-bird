import math
import sys
import time

import pygame

from pygame.locals import *
from main import SCREEN_WIDTH, DISPLAYSURF, BLUE, CLOCK, FPS, PIPE_WIDTH, RED, SCREEN_HEIGHT, FONT_LARGE, WHITE, \
    FONT_SMALL, GAME_STATE_SCALE_FACTOR, PIPE_GAP, IMAGE_SCALE_FACTOR
from player import Player
from pipe import Pipe


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

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            self.player.move(self.deltatime)

            if self.player.has_jumped:
                for pipe in self.pipes:
                    pipe.move(self.deltatime)

                    if pipe.is_off_screen():
                        pipe.set_left(self.rightmost_pipe.top_pipe.rect.right + self.pipe_gap)
                        self.rightmost_pipe = pipe

            if self.pipes[self.next_pipe].top_pipe.rect.right < self.player.rect.left:
                self.score += 1
                self.next_pipe = (self.next_pipe + 1) % self.num_pipes

            DISPLAYSURF.fill(BLUE)
            self.player.draw(DISPLAYSURF)

            for pipe in self.pipes:
                pipe.draw(DISPLAYSURF)

            score_text = FONT_SMALL.render(str(self.score), True, WHITE)
            DISPLAYSURF.blit(score_text, (SCREEN_WIDTH - 100, 10))

            if self.is_player_dead():
                game_over()

            pygame.display.flip()
            self.deltatime = CLOCK.tick(FPS) / 1000

    def get_state(self):
        pipe = self.pipes[self.next_pipe]
        pipe_center = ((pipe.top_pipe.rect.left + pipe.top_pipe.rect.right) / 2, pipe.top_pipe.rect.bottom + pipe.gap / 2)
        max_horizontal_distance = (PIPE_GAP // GAME_STATE_SCALE_FACTOR) - 1

        return (
            int(self.player.velocity_y < 0),  # moving up
            int(self.player.velocity_y > 0),  # moving down
            int(max(0, min((pipe_center[0] - self.player.rect.center[0]) // GAME_STATE_SCALE_FACTOR, max_horizontal_distance))),  # scaled horizontal distance from center of pipe
            int((pipe_center[1] - self.player.rect.center[1] + SCREEN_HEIGHT) // GAME_STATE_SCALE_FACTOR)  # scaled + shifted vertical distance from center of pipe
        )

    def step(self, action):
        reward = 15
        is_dead = False
        pipe = self.pipes[self.next_pipe]

        if action == 1:
            self.player.jump()

        self.player.move(self.deltatime)

        if self.player.has_jumped:
            for pipe in self.pipes:
                pipe.move(self.deltatime)

                if pipe.is_off_screen():
                    pipe.set_left(self.rightmost_pipe.top_pipe.rect.right + PIPE_GAP)
                    self.rightmost_pipe = pipe

        if pipe.top_pipe.rect.center < self.player.rect.center:
            self.score += 1
            self.next_pipe = (self.next_pipe + 1) % self.num_pipes

        DISPLAYSURF.fill(BLUE)
        self.player.draw(DISPLAYSURF)

        for pipe in self.pipes:
            pipe.draw(DISPLAYSURF)

        score_text = FONT_SMALL.render(str(self.score), True, WHITE)
        DISPLAYSURF.blit(score_text, (SCREEN_WIDTH - 100, 10))

        pygame.display.flip()

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
