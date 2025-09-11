import pygame
from pygame import DOUBLEBUF, SCALED

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 100, 50)
RED = (200, 50, 50)
BLUE = (120, 150, 250)

FPS = 60
CLOCK = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PIPE_WIDTH = 60

FONT_SMALL = pygame.font.SysFont("Verdana", 16)
FONT_LARGE = pygame.font.SysFont("Verdana", 60)

IMAGE_SCALE_FACTOR = 0.25

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCALED | DOUBLEBUF, vsync=1)
pygame.display.set_caption('Flappy Bird')

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])


if __name__ == '__main__':
    from game import Game

    game = Game()
    game.run()
