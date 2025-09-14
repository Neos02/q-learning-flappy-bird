import pygame
from pygame import DOUBLEBUF, SCALED

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (112, 197, 206)

FPS = 60
CLOCK = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PIPE_WIDTH = 60
PIPE_GAP = 180

FONT_SMALL = pygame.font.SysFont("Verdana", 16)
FONT_LARGE = pygame.font.SysFont("Verdana", 60)

IMAGE_SCALE_FACTOR = 2
GAME_STATE_SCALE_FACTOR = 10

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCALED | DOUBLEBUF, vsync=1)
pygame.display.set_caption('Flappy Bird')

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])


if __name__ == '__main__':
    from agent import Agent
    agent = Agent()
    agent.train(epoch=8000)
