import math
import sys
import time

import pygame

from pygame.locals import *
from main import SCREEN_WIDTH, DISPLAYSURF, BLUE, FPS, SCREEN_HEIGHT, WHITE, \
    FONT_NUMBERS, BLACK, load_image
from player import Player
from pipe import Pipe
from scrolling_image import ScrollingImage


class Game:

    world_speed = -200
    pipe_gap = 180
    state_distance_scale_factor = 10

    ground_image = ScrollingImage("images/ground.png")
    bush_image = ScrollingImage("images/bush.png", SCREEN_HEIGHT - ground_image.image.get_height())
    city_image = ScrollingImage("images/city.png", SCREEN_HEIGHT - ground_image.image.get_height() - bush_image.image.get_height() + 6)
    cloud_image = ScrollingImage("images/cloud.png", SCREEN_HEIGHT - ground_image.image.get_height() - bush_image.image.get_height() - city_image.image.get_height() + 6 + 26)
    game_over_image = load_image("images/game-over.png", 4)

    def __init__(self, is_agent=False):
        self.deltatime = 0
        self.num_pipes = math.ceil(SCREEN_WIDTH / (Game.pipe_gap + Pipe.width))
        self.pipes = [Pipe((SCREEN_WIDTH / 2 + i * (Game.pipe_gap + Pipe.width), SCREEN_HEIGHT // 2 if i == 0 else Pipe.get_random_height())) for i in range(self.num_pipes)]
        self.rightmost_pipe = self.pipes[self.num_pipes - 1]
        self.next_pipe = 0
        self.player = Player(is_agent)
        self.score = 0
        self.is_game_over = False

    def _move(self):
        self.player.move(self.deltatime)

        if self.player.has_jumped and not self.is_game_over:
            for pipe in self.pipes:
                pipe.move(Game.world_speed * self.deltatime)

                if pipe.is_off_screen_left():
                    pipe.center = (self.rightmost_pipe.center[0] + (Game.pipe_gap + Pipe.width), Pipe.get_random_height())
                    self.rightmost_pipe = pipe

            self.ground_image.move(Game.world_speed * self.deltatime)
            self.bush_image.move(Game.world_speed * self.deltatime)
            self.city_image.move(Game.world_speed * self.deltatime)
            self.cloud_image.move(Game.world_speed * self.deltatime)

        if self.pipes[self.next_pipe].upper.rect.right < self.player.rect.left:
            self.score += 1
            self.next_pipe = (self.next_pipe + 1) % self.num_pipes

    def _draw(self):
        DISPLAYSURF.fill(BLUE)
        Game.cloud_image.draw(DISPLAYSURF)
        Game.city_image.draw(DISPLAYSURF)
        Game.bush_image.draw(DISPLAYSURF)
        self.player.draw(DISPLAYSURF)

        for pipe in self.pipes:
            pipe.draw(DISPLAYSURF)

        Game.ground_image.draw(DISPLAYSURF)
        self._draw_score(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10, 3)

    def _draw_score(self, x, y, border_width=0):
        score_text_white = FONT_NUMBERS.render(str(self.score), True, WHITE)
        score_text_black = FONT_NUMBERS.render(str(self.score), True, BLACK)

        x -= score_text_white.get_width() / 2
        y -= score_text_white.get_height() / 2

        if border_width > 0:
            DISPLAYSURF.blit(score_text_black, (x - border_width, y - border_width))
            DISPLAYSURF.blit(score_text_black, (x - border_width, y + border_width))
            DISPLAYSURF.blit(score_text_black, (x + border_width, y - border_width))
            DISPLAYSURF.blit(score_text_black, (x + border_width, y + border_width))

        DISPLAYSURF.blit(score_text_white, (x, y))

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            self._move()
            self._draw()

            if self.is_player_dead() or self.is_game_over:
                self.game_over()

            pygame.display.flip()
            self.deltatime = pygame.time.Clock().tick(FPS) / 1000

    def get_state(self):
        pipe = self.pipes[self.next_pipe]
        pipe_right_center = (pipe.center[0] + Pipe.width / 2, pipe.center[1])

        # get the horizontal distance between the player's left edge and the pipe's right edge
        # if the distance is greater than half the pipe gap then treat that as one state, otherwise
        # scale distance down to create a new state for every N pixels
        max_horizontal_distance = (Game.pipe_gap + pipe.upper.rect.width) // 2
        horizontal_distance = min((pipe_right_center[0] - self.player.rect.left), max_horizontal_distance)

        # get the vertical distance between the player's center and the pipe's center
        # if the distance is greater than the pipe opening size then treat that as one state, otherwise
        # scale distance down to create a new state for every N pixels
        max_vertical_distance = Game.pipe_gap
        vertical_distance = max(-max_vertical_distance, min((pipe_right_center[1] - self.player.rect.center[1]), max_vertical_distance))
        game_state_vertical_distance = vertical_distance if vertical_distance >= 0 else max_vertical_distance - vertical_distance

        return (
            int(horizontal_distance // Game.state_distance_scale_factor),  # scaled horizontal distance from right of pipe
            int(game_state_vertical_distance // Game.state_distance_scale_factor)  # scaled + adjusted vertical distance from center of pipe
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
        if pygame.sprite.spritecollideany(self.player, self.pipes[self.next_pipe]):
            return True

        return self.player.rect.bottom > SCREEN_HEIGHT - self.ground_image.image.get_height()

    def is_player_off_screen(self):
        return self.player.rect.top > SCREEN_HEIGHT

    def game_over(self):
        DISPLAYSURF.blit(self.game_over_image, ((SCREEN_WIDTH - self.game_over_image.get_width()) / 2, (SCREEN_HEIGHT - self.game_over_image.get_height()) / 2))
        self.player.rotation_angle_deg = 180
        self.player.is_agent = True
        self.is_game_over = True

        if self.is_player_off_screen():
            time.sleep(2)
            pygame.quit()
            sys.exit()
