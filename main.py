import pygame

BLACK = (0, 0, 0)
GREEN = (50, 100, 50)
RED = (200, 50, 50)
BLUE = (120, 150, 250)

FPS = 60
CLOCK = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PIPE_WIDTH = 60

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')


if __name__ == '__main__':
    from game import Game

    pygame.init()
    game = Game()
    game.run()
