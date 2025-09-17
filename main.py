import pygame
from pygame import DOUBLEBUF, SCALED
import argparse

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (112, 197, 206)

FPS = 60
CLOCK = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PIPE_GAP = 180
PIPE_SPEED = 200

FONT_NUMBERS = pygame.font.Font("fonts/flappy-numbers.ttf", 24)

IMAGE_SCALE_FACTOR = 2
GAME_STATE_SCALE_FACTOR = 10

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCALED | DOUBLEBUF, vsync=1)
pygame.display.set_caption('Flappy Bird')

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])


if __name__ == '__main__':
    from game import Game
    from agent import Agent

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', type=int, choices=[0, 1, 2, 3], default=0, help='0 - Play Snake, 1 - Train Agent from Scratch, 2 - Continue Training Agent from Existing Model, 3 - Run Existing Model')
    parser.add_argument('--epoch', '-e', type=int, help='Epoch number to load')
    parser.add_argument('--model-dir', '-d', type=str, help='Directory to save and load models', default='models')
    args = parser.parse_args()

    if args.mode == 0:
        game = Game()
        game.run()
    elif args.mode == 1:
        agent = Agent(model_dir=args.model_dir)
        agent.train()
    elif args.mode == 2:
        if args.epoch is None:
            parser.error('--epoch must be specified')

        agent = Agent(model_dir=args.model_dir)
        agent.train(args.epoch)
    elif args.mode == 3:
        if args.epoch is None:
            parser.error('--epoch must be specified')

        agent = Agent(model_dir=args.model_dir)
        agent.run_epoch(args.epoch)
