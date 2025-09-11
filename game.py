import math
import sys
import time

import pygame

from pygame.locals import *
from main import SCREEN_WIDTH, DISPLAYSURF, BLUE, CLOCK, FPS, PIPE_WIDTH, RED, SCREEN_HEIGHT, FONT_LARGE, WHITE
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
        self.pipe_gap = 200
        self.num_pipes = math.ceil(SCREEN_WIDTH / (self.pipe_gap + PIPE_WIDTH))
        self.pipes = [Pipe(i * (self.pipe_gap + PIPE_WIDTH) + SCREEN_WIDTH // 2, (SCREEN_HEIGHT - self.pipe_gap) // 2 if i == 0 else None) for i in range(self.num_pipes)]
        self.rightmost_pipe = self.pipes[self.num_pipes - 1]
        self.player = Player()

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

            DISPLAYSURF.fill(BLUE)
            self.player.draw(DISPLAYSURF)

            for pipe in self.pipes:
                pipe.draw(DISPLAYSURF)

            if self.is_player_dead():
                game_over()

            pygame.display.flip()
            self.deltatime = CLOCK.tick(FPS) / 1000

    def is_player_dead(self):
        for pipe in self.pipes:
            if pygame.sprite.spritecollideany(self.player, pipe):
                return True

        return self.player.is_off_screen()
