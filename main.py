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

DISPLAYSURF = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Flappy Bird')


if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(BLUE)

        pygame.display.update()
        CLOCK.tick(FPS)
