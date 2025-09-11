import pygame
import sys

from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
GREEN = (50, 100, 50)
RED = (200, 50, 50)
BLUE = (120, 150, 250)

FPS = 60
CLOCK = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')


if __name__ == '__main__':
    from player import Player
    from pipe import Pipe

    player = Player()
    pipe = Pipe()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        player.move()
        pipe.move()

        DISPLAYSURF.fill(BLUE)
        player.draw(DISPLAYSURF)
        pipe.draw(DISPLAYSURF)

        pygame.display.update()
        CLOCK.tick(FPS)
